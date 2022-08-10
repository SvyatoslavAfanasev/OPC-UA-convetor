import UA_Server
import xml.etree.ElementTree as ET
from log.LOGS import LOGS
import dictdiffer
import time
def get_config(configFile='cfg.xml'):
    tree = ET.parse(configFile)
    root = tree.getroot()
    res = {}
    for child in root:
        res[child.tag] = child.text

    return res


config = get_config(configFile='cfg.xml')
ua_serv = UA_Server.UA_SERVER(config['UA_HOST'], config['UA_SERVER_NAME'], config['UA_ROOT_NAMESPACE'])

try:
    ua_serv.start()

    print('In the work ...')
    while True:

        ua_serv.update_tags()
        time.sleep(int(config['UPDATE_RATE'])/1000)

except OSError as err:
    print('Error: ', err)


# pyinstaller.exe --onefile --icon="C:\Users\svyat\OPC_DA_Allan Bredly\Для установщика\Gazprom-symbol.ico" --hidden-import win32timezone "C:\Users\svyat\PycharmProjects\UA_Server\Convertor_DA_UA.py"
