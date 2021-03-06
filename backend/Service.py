import sys
import logging
import logging.handlers
from concurrent_log_handler import ConcurrentRotatingFileHandler

from flask import Flask, jsonify, request, json
from datetime import datetime
from flask_cors import CORS
from urllib.parse import urlparse

from DB import dataAccess
from BisnessLogic import BLogic
from config import Config

app = Flask(__name__)
app.debug = True
CORS(app) 

handler = ConcurrentRotatingFileHandler('Log/log', maxBytes=10*1024*1024, backupCount=5)
logging.basicConfig( level=logging.DEBUG, handlers=[handler],format='%(asctime)s %(name)-12s %(levelname)-8s %(message)-3000s',
                    datefmt='%d-%m-%y %H:%M')

logger = logging.getLogger(__name__)



@app.route('/createChartData')
def create_chart_data( ):
    try:   
        global blItem
        data = blItem.createDataTableAndGraph( )
        logger.info('%s how data looks  before you send it to front: %.3000s\n', '/createChartData', data)
        jsonData = jsonify({"TableData":data["TableData"],  "GraphData":data["GraphData"]})
        return jsonData
    except Exception as ex:
        logger.error('%s the following exeption  appeared: %s\n', '/createChartData',ex )
        raise

@app.route('/pinger', methods=['POST'])
def pingercallback():
    try:
        global config
        global da
        data = json.loads(request.stream.read())
        if not __isPingerValid(data):
            logger.error('pinger validation failed for %s', data)
            return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}
        logger.info('%s how data looks  when it comes from client:%s\n', '/pinger', data)
        da.addNewPings(data)
        logger.info('%s how delay_time looks before it  back to client: %s\n', '/pinger',config.get_delay_time())
        return jsonify({'delay':  config.get_delay_time()})
    except Exception as ex:
        logger.error('%s the following exeption  appeared: %s\n', '/pinger',ex )
        raise

@app.route('/delete/<path:name>')
def delete_comp(name):
    global da
    logger.info('%s how data looks  before you send it to db to delete:%s\n', '/delete', name )
    if da.deleteComp(name):   
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

def __isPingerValid(data):
    return data['ping'] and  type(data['ping']) == float and data['hostname'] and \
        type (data['hostname']) == str 

def DI(config_path, portNum):
    global config
    global da
    global blItem
    config = Config(config_path)
    da  = dataAccess(mode, config)
    blItem = BLogic(da, config )
    app.run(port=portNum)

if __name__ == "__main__":     
    global mode    
    
    if len(sys.argv)==1:
        mode = 'production'
    else:
        mode =   sys.argv[1]
    if mode =='production':
        DI("C:\\Users\\simal\\projects_git\\ping_management\\backend\\config_production.txt", 5000)
    elif mode == 'test':
        DI("C:\\Users\\simal\\projects_git\\ping_management\\backend\\config_test.txt", 5002)
        
    
