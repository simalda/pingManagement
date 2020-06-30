from flask import Flask, jsonify, request, json
from datetime import datetime
from flask_cors import CORS
from urllib.parse import urlparse
import config as conf
from DB import *
from BisnessLogic import *
import json
app = Flask(__name__)
app.debug = True
CORS(app) 

# @app.route('/selectPings')
# def get_pings():
#     sqlQuery = dataAccess()
#     return jsonify(sqlQuery.getPings())   

# @app.route('/createChartData')
# def create_chart_data():
#     sqlQuery = dataAccess()
#     TableData = sqlQuery.getTableData()
#     TableDataInfo = []
    
#     for item in TableData:
#         status = sqlQuery.isAlive( item[1], item[3])
        
#         singlePing = {
#             "id": item[0],
#             "name": item[1],
#             "ping": item[2],
#             "time": item[3],
#             "status":  status
#         }
#         TableDataInfo.append(singlePing)
#     GraphData = sqlQuery.getChartData()
#     return jsonify({"TableData":TableDataInfo,
#     "GraphData":GraphData})

@app.route('/createChartData')
def create_chart_data():
    blItem = BLogic()
    data = blItem.createDataTableAndGraph()
    return jsonify({"TableData":data["TableData"],  "GraphData":data["GraphData"]})

@app.route('/pinger', methods=['POST'])
def pingercallback():
    data = json.loads(request.stream.read())
    sqlQuery = dataAccess()
    sqlQuery.addNewPings(data)
    return jsonify({'delay': conf.delay_time})

@app.route('/delete/<path:name>')
def delete_comp(name):
    sqlQuery = dataAccess()
    if sqlQuery.deleteComp(name):   
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    return False

if __name__ == "__main__":
    app.run(port=5000)
 