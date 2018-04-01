from flask import Flask
from flask.ext.pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'i-met'
app.config['MONGO_URI'] = 'mongodb://<dbuser>:<dbpassword>@ds121289.mlab.com:21289/i-met'

mongo = PyMongo(app)


@app.route('/add')
def add():
    user = mongo.db.users
    user.insert({'name' : 'Olga'})
    return 'Added user'

