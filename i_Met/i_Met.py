from flask import Flask, redirect, url_for, request, render_template, session, flash
from flask_pymongo import PyMongo
import bcrypt
from pymongo import MongoClient

app = Flask(__name__)
# client = MongoClient('localhost', 27017)    #Configure the connection to the database
# db = client.i_Met


app.config['MONGO_DBNAME'] = 'i-met'
app.config['MONGO_URI'] = 'mongodb://Olga:olichka121@ds121289.mlab.com:21289/i-met'

mongo = PyMongo(app)


@app.route('/')
def index():
    if 'user' in session:
        return render_template('index.html', url=url_for('user_cabinet'), name='Кабінет')
    return render_template('index.html', url=url_for('login'), name='Увійти')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'user' in session:
        return redirect(url_for('user_cabinet'))
        # return 'You are logged as ' + session['username']
    if request.method == 'POST':
        user = mongo.db.users
        login_user = user.find_one({'email': request.form['email']})
        if login_user:
            if bcrypt.hashpw(request.form['password'].encode(encoding='UTF-8', errors='strict'),
                             login_user['password']) == \
                    login_user['password']:
                session['user'] = request.form['email']
                return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'email': request.form['email']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert(
                {'email': request.form['email'], 'password': hashpass, 'name_surname': request.form['name_surname'],
                 'account_num': {'3663434534': {'type': 'water',
                                                'date': {'22,04,18': '100', '23,04,18': '150', '24,04,18': '200',
                                                         '25,04,18': '280'}}}})
            return redirect(url_for('index'))

        return 'That email already exists'

    return render_template('register.html')


@app.route('/user')
def user():
    return render_template('user.html')


@app.route('/user_cabinet')
def user_cabinet():
    return render_template('user-cabinet.html')


@app.route('/gas')
def gas():
    return render_template('gas.html')


@app.route('/water')
def water():
    # if 'user' in session:
        values = []
        labels = []
        users = mongo.db.users.find_one({'email': 'olichka121kr76@gmail.com'})
        for dt in users['account_num']['3663434534']['date']:
            labels.append(dt)
        for dates in users['account_num']['3663434534']['date']:
            values.append(users['account_num']['3663434534']['date'][dates])
        return render_template('water.html', values=values, labels=labels)
    # return render_template('water.html', values="", labels="")


@app.context_processor
def utility_processor():
    def logout():
        return session.pop('user', None)

    return dict(logout=logout)


@app.route('/chart')
def chart():
    if 'user' in session:
        users = mongo.db.users
        user = users.find_one({'email': 'user'})
        labels = user['days']
        values = user['days']
        return render_template('chart.html', values=values, labels=labels)


if __name__ == '__main__':
    app.secret_key = 'Smart_foolish_counter'
    app.run(debug=True)
