import os
from flask import Flask, render_template, redirect, session, request, url_for
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'anropa'
app.config["MONGO_URI"] = 'mongodb://127.0.0.1:27017/anropa'

mongo = PyMongo(app)

# WEB PAGES

@app.route('/')
def home():
    if 'name' in session:
        return 'You are logged in as' + session['name']
    return render_template("index.html")

@app.route('/about_us')
def about_us():
    return render_template("aboutus.html")

@app.route('/vacancies')
def vacancies():
    return render_template("vacancies.html")

@app.route('/employees')
def employees():
    return render_template("employees.html")

@app.route('/employers')
def employers():
    return render_template("employers.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

# AUTH

@app.route('/login')
def login():
    return render_template("login.html")

#@app.rout('/login', methods=['POST'])
#def login_post():
    #return

#@app.route('/signup')
#def signup():
    #return render_template("signup.html")

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'email' : request.form['email']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['name'], 'email' : request.form['email'], 'password' : hashpass})
            session['name'] = request.form['name']
            return redirect(url_for('home'))
        
        return 'That username already exists!'

    return render_template("signup.html")

@app.route('/logout')
def logout():
    return redirect(url_for('home'))

app.secret_key = 'mysecret'
app.run(debug=True)