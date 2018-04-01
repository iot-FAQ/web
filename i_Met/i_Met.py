from flask import Flask, redirect, url_for, request, render_template, session
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'i-met'
app.config['MONGO_URI'] = 'mongodb://Olga:olichka121@ds121289.mlab.com:21289/i-met'

mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'username' in session:
        return redirect(url_for('logout'))
        # return 'You are logged as ' + session['username']
    if request.method == 'POST':
        user = mongo.db.users
        login_user = user.find_one({'name': request.form['username']})

        if login_user:
            if bcrypt.hashpw(request.form['pass'].encode('utf-8'),
                             login_user['password']) == login_user['password']:
                session['username'] = request.form['username']
                return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.pop('username', None)
        return redirect(url_for('index'))
    return render_template('logout.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name': request.form['username'], 'password': hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'That email already exists'

    return render_template('register.html')


@app.route('/')
def logged_in():
    if 'username' in session:
        return 'You are logged in as ' + session['username']
    return render_template('index.html')


if __name__ == '__main__':
    app.secret_key = 'secret'
    app.run(debug=True)
