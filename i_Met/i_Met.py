from flask import Flask, redirect, url_for, request, render_template, session, flash, Response
from flask_pymongo import PyMongo
import bcrypt
from authy.api import AuthyApiClient
from pymongo import MongoClient

app = Flask(__name__)
# client = MongoClient('localhost', 27017)    #Configure the connection to the database
# db = client.i_Met


app.config['MONGO_DBNAME'] = 'i-met'
app.config['MONGO_URI'] = 'mongodb://Olga:olichka121@ds121289.mlab.com:21289/i-met'

mongo = PyMongo(app)
app.config.from_object('config')
api = AuthyApiClient(app.config['AUTHY_API_KEY'])
app.secret_key = app.config['SECRET_KEY']


@app.route('/phone', methods=["GET", "POST"])
def phone():
    if request.method == "POST":
        country_code = request.form.get("country_code")
        phone_number = request.form.get("phone_number")

        session['country_code'] = country_code
        session['phone_number'] = phone_number

        api.phones.verification_start(phone_number, country_code, via='sms')

        return redirect(url_for("verify"))
    return render_template('phone.html')


@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        token = request.form.get("token")

        phone_number = session.get("phone_number")
        country_code = session.get("country_code")

        verification = api.phones.verification_check(phone_number,
                                                     country_code,
                                                     token)

        if verification.ok():
            return Response("<h1>Success!</h1>")

    return render_template("verify.html")


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
                # hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
                # user.insert({'email': request.form['email'], 'password': hashpass,
                #              'account_num': {'type': {'gas': {'3663434534': {
                #                  'date': {'18': {'04': {'22': '100', '23': '150', '24': '200',
                #                                         '25': '280'}}}}},
                #                  'water': {'3663434534': {
                #                      'date': {'18': {'04': {'22': '150', '23': '100', '24': '180',
                #                                             '25': '140'}}}}}}}})
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
    types = []
    values = []
    labels = []
    users = mongo.db.users.find_one({'email': 'olichka121@ukr.net'})
    for type in users['account_num']['type']:
        types.append(type)
    gas = users['account_num']['type'][types]['gas']
    water = users['account_num']['type'][types]['water']
    for dt in users['account_num']['3663434534']['date']:
        labels.append(dt)
    for dates in users['account_num']['3663434534']['date']:
        values.append(users['account_num']['3663434534']['date'][dates])
    return render_template('user-cabinet.html', values=values, labels=labels)
    # return render_template('user-cabinet.html')


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
    app.run(debug=True)
