 
from flask import Flask, jsonify, request, json
from datetime import datetime
from flask_cors import CORS
from urllib.parse import urlparse
from DB import *
import json
app = Flask(__name__)
app.debug = True
CORS(app) 

@app.route('/selectPings')
def get_pings():
    sqlQuery = SQL()
    return jsonify(sqlQuery.getPings())   



 

# @app.route('/createChartData')
# def create_chart_data():
#     sqlQuery = SQL()

#     return jsonify(sqlQuery.getCharData())

@app.route('/createChartData')
def create_chart_data():
    sqlQuery = SQL()
    TableData = sqlQuery.getTableData()
    TableDataInfo = []
    for item in TableData:
        status = sqlQuery.isAlive( item[1], item[3])
        print('status from creactcharData')
        print(status)
        
        # print(json.dumps(item[3]))
        singlePing = {
            "id": item[0],
            "name": item[1],
            "ping": item[2],
            "time": item[3],
            "status":  status
        }
        TableDataInfo.append(singlePing)
    GraphData = sqlQuery.getCharData()
    return jsonify({"TableData":TableDataInfo,
    "GraphData":GraphData})

@app.route('/pinger', methods=['POST'])
def pingercallback():
    data = json.loads(request.stream.read())
    sqlQuery = SQL()
    sqlQuery.addNewPings(data)
    print('PINGER:'+str(sqlQuery.delay_time))
    return jsonify({'delay': sqlQuery.delay_time})

# @app.route('/client/<user>', methods=['POST'])
# def add_ping(user):
#     data = json.loads(request.stream.read())
#     sqlQuery = SQL()
#     sqlQuery.addNewPings(data)
#     return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

@app.route('/delete/<path:name>')
def delete_comp(name):
    sqlQuery = SQL()
    print(name)
    if sqlQuery.deleteComp(name):   
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    return 



if __name__ == "__main__":
    app.run(port=5000)
 