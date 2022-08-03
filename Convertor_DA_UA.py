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

except:
    print('Error')


