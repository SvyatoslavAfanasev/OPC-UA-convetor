import sys

sys.path.insert(0, "..")
from opcua import ua, Server, Client
from opcua.ua import NodeIdType, NodeId
from log.LOGS import LOGS
from threading import Timer


def get_ua_type(tag):
    if tag['type_value'] == 'float' or tag['type_value'] == 'Single':
        return [float(tag['value']), ua.uatypes.VariantType.Float]
    elif 'Int' in tag['type_value']:
        return [int(tag['value']), ua.uatypes.VariantType.Int32]
    elif tag['type_value'] == 'boolean':
        return [bool(tag['value']), ua.uatypes.VariantType.Boolean]
    elif tag['type_value'] == 'string':
        return [tag['value'], ua.uatypes.VariantType.String]
    else:
        return [tag['value'],None]

    # if '.' in value:
    #     return [float(value), ua.uatypes.VariantType.Float]
    # else:
    #     try:
    #         try:
    #             value = int(value)
    #             return [value, ua.uatypes.VariantType.Int32]
    #         except:
    #             value = bool(value)
    #             return [value, ua.uatypes.VariantType.Boolean]
    #     except TypeError:
    #         return [value, ua.uatypes.VariantType.String]


class UA_SERVER:
    def __init__(self, endpoint='opc.tcp://127.0.0.1:4850', name='GAZAUTO_DA_to_UA_converter',
                 namespace='GAZAUTO_DA_to_UA_converter'):
        print('UA server initialization...')
        self.endpoint = endpoint
        self.server_name = name

        self.server = Server()
        self.server.set_endpoint(endpoint)
        self.server.set_server_name(name)

        self.nmspc = self.server.register_namespace(namespace)
        self.objects = self.server.get_objects_node()
        # Добавление мигающего бита (True/False) проверка работы сервера
        self.signal_point = self.objects.add_object(self.nmspc, 'Signal')
        self.Data = self.objects.add_object(self.nmspc, 'Data')
        self.signal_point_value = self.signal_point.add_variable(self.nmspc, "Status", True)
        self.MonitorList = {}
        self.client = Client(self.endpoint)

    def read_file(self):
        file = open("tagsAll.txt", "r")
        tags = file.readlines()
        tags.sort()
        tree = {}

        for i_tag in tags:
            i_tag_info = i_tag.split(';')
            i_tag_info[0] = i_tag_info[0].replace(':', '.')
            i_tag_info[1] = i_tag_info[1].replace(',', '.').split(';')
            value = i_tag_info[1][0]
            tree[i_tag_info[0]] = {'value': value,
                                   'type_value': i_tag_info[2]}
        return tree

    def add_value_from_txt(self):
        self.MonitorList = self.read_file()
        # Проход по всем тегам
        for tag_name in self.MonitorList.keys():
            tag_information = self.MonitorList[tag_name]
            # Определяем каким должен быть индификатор тега
            nodeID = NodeId(identifier=tag_name, namespaceidx=self.nmspc, nodeidtype=NodeIdType.String)
            # Добавдение тэга, его значения и тип в папку Data
            type_tag = get_ua_type(tag_information)
            self.Data.add_variable(nodeID,
                                   bname=tag_name,
                                   val=type_tag[0],
                                   varianttype=type_tag[1]
                                   )
        LOGS('UA_Server.add_value_from_txt', 'Adding tags in opc ua server', 'INFO')

    def update_tags(self):

        self.MonitorList = self.read_file()  # Чтение файна и создание словаря

        for tag_name in self.MonitorList:
            tag_information = self.MonitorList[tag_name]
            node = 'ns=2; s={}'.format(tag_name)  # получение nodes

            var = self.server.get_node(node)
            type_tag = get_ua_type(tag_information)
            var.set_value(type_tag[0])  # обновление тэгов

    def signal(self):
        # Минающий бит каждые 20 секунд обновление
        if self.signal_point_value.get_value():
            self.signal_point_value.set_value(False)
        else:
            self.signal_point_value.set_value(True)
        t = Timer(20, self.signal)
        t.start()

    def stop(self):
        LOGS('UA_SERVER', 'Stopping UA SERVER! UA_HOST: {}'.format(self.endpoint), 'INFO')
        self.server.stop()

    def start(self):
        self.signal()
        LOGS('UA_SERVER', 'Start UA SERVER! UA_HOST: {}'.format(self.endpoint), 'INFO')
        try:
            self.add_value_from_txt()
            self.server.start()

        except OSError as err:
            print('Error: ', err)
            LOGS('UA_SERVER', 'Error: Another converter may be working, or there is a problem with the port', 'ERROR')
            sys.exit()
