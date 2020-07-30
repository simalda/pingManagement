import pytest
import requests
import json
from DB import dataAccess
from BisnessLogic import BLogic
from datetime import datetime, timedelta, timezone
import subprocess
from config import Config
 
sortedData = {}

def setup_function(function):
    # subprocess.call(['py', 'Service.py', 'test'])
    global pingerService
    pingerService = subprocess.Popen(['py', 'Service.py', 'test'])
    config = Config("C:\\Users\\simal\\projects_git\\ping_management\\backend\\config_test.txt") 
    da = dataAccess('test', config)
    da.deleteAll()
    bl = BLogic(da, config)

def teardown_function(function):
    global pingerService
    pingerService.terminate()
 
def test_check_pinger_wrong():   
    out_url = "http://127.0.0.1:5002/pinger"
    out = {
            'hostname'  :   'DESKTOP-NIFA-TEST',
            'ping'      :   1456,
            'test_url'  :   "www.calorizator.ru",
            'delay'     :   30,
            'time'      :   datetime.now().strftime('%d/%m/%y %H:%M:%S')
        }

    request     =   requests.post(out_url,json=out)
    result      =   json.loads(request.text)
    assert  result['success'] == False

def test_check_pinger_correct():   
    out_url = "http://127.0.0.1:5002/pinger"
    out = {
            "hostname"  :   "DESKTOP-NIFA-TEST",
            "ping"      :   145.6,
            "test_url"  :   "www.calorizator.ru",
            "delay"     :   30,
            "time"      :   datetime.now().strftime('%d/%m/%y %H:%M:%S')
        }

    request     =   requests.post(out_url,json=out)
    result      =   json.loads(request.text)
    print(result)
    my_delay     =   result['delay']
    
    assert my_delay == 1000

def test_check_createChartData():
    out_url = "http://127.0.0.1:5002/pinger"
    out = {
                'hostname'  :   'DESKTOP-NIFA-TEST',
                'ping'      :   145.6,
                'test_url'  :   "www.calorizator.ru",
                'delay'     :   30,
                'time'      :   datetime.now().strftime('%d/%m/%y %H:%M:%S')
            }

    requests.post(out_url,json=out)
    res = requests.get("http://127.0.0.1:5002/createChartData")
    assert len( res.json()['TableData']) == 1

def test_check_delete():
    out_url = "http://127.0.0.1:5002/pinger"
    out = {
                'hostname'  :   'DESKTOP-NIFA-TEST',
                'ping'      :   145.6,
                'test_url'  :   "www.calorizator.ru",
                'delay'     :   30,
                'time'      :   datetime.now().strftime('%d/%m/%y %H:%M:%S')
            }

    request = requests.post(out_url,json=out)
    result = requests.get("http://127.0.0.1:5002/delete/DESKTOP-NIFA-TEST")
    assert    result.json()['success'] == True

  


 