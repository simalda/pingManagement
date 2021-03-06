import requests
import time
from threading import Thread
import socket
from tcp_latency import measure_latency
import json
from datetime import datetime

out_url = "http://127.0.0.1:5000/pinger"
test_url = "www.calorizator.ru"
my_delay = 50

while True:
    try:
        out = {
            'hostname'  :   socket.gethostname(),
            'ping'      :   measure_latency(host=test_url,timeout=2.5)[0],
            'test_url'  :   test_url,
            'delay'     :   my_delay,
            'time'      :   datetime.now().strftime('%d/%m/%y %H:%M:%S')
        }

        request     =   requests.post(out_url,json=out)
        result      =   json.loads(request.text)
        my_delay     =   result['delay']
        # test_url    =   result['test_url']
        print('sent')
    except Exception as e:
        print('failed')
        pass         
    time.sleep(my_delay)