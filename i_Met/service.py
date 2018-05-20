from bcrypt import hashpw
from flask import request, jsonify, Flask, json
import datetime

from flask_pymongo import PyMongo

# from i_Met import app
# from i_Met import mongo

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

app.config['MONGO_DBNAME'] = 'i-met'
app.config['MONGO_URI'] = 'mongodb://Olga:olichka121@ds121289.mlab.com:21289/i-met'

mongo = PyMongo(app)
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']

now = datetime.datetime.now()
curr_day = now.day
curr_month = now.month
curr_year = now.year


@app.route('/check_user', methods=['GET'])
def check_user():
    users = mongo.db.users
    query_parameters = request.args

    email = query_parameters.get('email')
    password = query_parameters.get('password')

    user = users.find_one({'email': email})
    if user:
        if hashpw(query_parameters.get('password').encode(encoding='utf-8', errors='strict'),
                  user['password']) == \
                user['password']:
            return True
        else:
            return False
    return 'Cannot find this email'


@app.route('/get_data', methods=['GET'])
def get_data():
    users = mongo.db.users
    query_parameters = request.args

    email = query_parameters.get('email')
    type = query_parameters.get('type')
    counter = query_parameters.get('counter')
    user = users.find_one({'email': email})
    if query_parameters.get('week'):
        month = user['account_num']['type'][type][counter]['date'][str(curr_year)][str(curr_month)]
        if curr_day < 7:
            last_month = user['account_num']['type'][type][counter]['date'][str(curr_year)][str(curr_month - 1)]
            month = user['account_num']['type'][type][counter]['date'][str(curr_year)][str(curr_month)]
            week = [(day, last_month[str(day)]) for day in range(len(last_month) - 7 + curr_day, len(last_month))]
            for day in range(1, curr_day + 1):
                week.append((day, month[str(day)]))
            return json.dumps(dict(week), sort_keys=False)
        else:
            week = {day: month[str(day)] for day in range(curr_day - 6, curr_day + 1)}
            return jsonify(week)
    elif query_parameters.get('month'):
        month = {day: user['account_num']['type'][type][counter]['date'][str(curr_year)][str(curr_month)][str(day)] for
                 day in user['account_num']['type'][type][counter]['date'][str(curr_year)][str(curr_month)] if
                 str(day) != 'month'}
        return jsonify(month)
    elif query_parameters.get('year'):
        year = user['account_num']['type'][type][counter]['date'][str(curr_year)]
        month = {month: year[str(month)]['month'] for month in year}
        return jsonify(month)
    return jsonify('Error')


@app.route('/update_data', methods=['PUT'])
def update_data():
    users = mongo.db.users
    query_parameters = request.args

    email = query_parameters.get('email')
    user = users.find_one({'email': email})
    return True


if __name__ == '__main__':
    app.run(debug=True)
