 
from flask import Flask, jsonify, request, json
from datetime import datetime
from flask_cors import CORS
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
    print(TableData) 
    TableDataInfo = []
    for item in TableData:
        status = sqlQuery.isAlive( item[1], item[3])
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
    print(jsonify({'delay': sqlQuery.delay_time})
)
    return jsonify({'delay': sqlQuery.delay_time})

# @app.route('/client/<user>', methods=['POST'])
# def add_ping(user):
#     data = json.loads(request.stream.read())
#     sqlQuery = SQL()
#     sqlQuery.addNewPings(data)
#     return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

@app.route('/delete/<name>')
def delete_comp(name):
    sqlQuery = SQL()
    sqlQuery.deleteComp(name)   
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


# @app.route('/login/<user>/<password>')
# def check_user(user, password):
#     sqlQuery = SQL()
#     return jsonify(sqlQuery.checkUser(user, password))


# @app.route('/signUp/<user>/<password>')
# def create_user(user, password):
#     sqlQuery = SQL()
#     return jsonify(sqlQuery.createUser(user, password))





# @app.route('/selectQuestions/<lang>/<numOfQuestions>')
# def get_questions(lang, numOfQuestions):
#     sqlQuery = SQL()
#     innerInfo = sqlQuery.SelectQuestionsforQuiz(lang, numOfQuestions)
#     questionInfo = []
#     for c in innerInfo:
#         singleQuestion = {
#             "question": c['question'],
#             "correctAnswer": c['correctAnswer'],
#             "answerOptions": [[c['answer1'][0], c['answer1'][1]], [c['answer2'][0], c['answer2'][1]], [c['answer3'][0], c['answer3'][1]], [c['answer4'][0], c['answer4'][1]]],
#             "questionId": c['questionId'],
#             "chosenAnswer": ""
#         }
#         questionInfo.append(singleQuestion)
#     return jsonify(questionInfo)


if __name__ == "__main__":
    app.run(port=5000)
 