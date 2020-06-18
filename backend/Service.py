 
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
     



 

# @app.route('/stat/<user>', methods=['POST'])
# def add_quiz(user):
#     data = json.loads(request.stream.read())
#     sqlQuery = SQL()
#     sqlQuery.addQuizToUSer(user, data)
#     return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


# @app.route('/login/<user>/<password>')
# def check_user(user, password):
#     sqlQuery = SQL()
#     return jsonify(sqlQuery.checkUser(user, password))


# @app.route('/signUp/<user>/<password>')
# def create_user(user, password):
#     sqlQuery = SQL()
#     return jsonify(sqlQuery.createUser(user, password))


# @app.route('/stat/<user>')
# def get_stat(user):
#     sqlQuery = SQL()
#     innerInfo = sqlQuery.getStatistic(user)
#     questionInfo = []
#     for c in innerInfo:
#         singleQuestion = {
#             "QuizId": c['QuizId'],
#             "Question": c['Question'],
#             "correctAnswer": c['correctAnswer'],
#             "ChosenAnswerId": c['ChosenAnswerId'],
#         }
#         questionInfo.append(singleQuestion)
#     return jsonify(questionInfo)


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
 