import os
from flask import Flask, render_template, redirect, session, request, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'anropa'
app.config["MONGO_URI"] = 'mongodb://127.0.0.1:27017/anropa'
app.secret_key = 'mysecret'

mongo = PyMongo(app)

# WEB PAGES

@app.route('/')
def home():
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

@app.route('/profile', methods=['POST', 'GET'])
def profile():
    if session.get('_id') is not None:
        if request.method == 'POST':
            users = mongo.db.users
            users.update({'_id' : ObjectId(session['_id'])}, {"$set":
                {'name' : request.form['name'], 
                'email' : session['email'],
                'address' : request.form['address'], 
                'city' : request.form['city'], 
                'zipcode' : request.form['zipcode'], 
                'current_job' : request.form['current_job']
            }})
            flash('Your information has been updated succesfully!')

        return render_template("profile.html", user=mongo.db.users.find_one({'_id': ObjectId(session['_id'])}))
    else:
        return redirect(url_for('home'))

# AUTH

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        user_login = users.find_one({'email' : request.form['email']})

        if user_login:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), user_login['password']) == user_login['password']:
                session['_id'] = str(user_login['_id'])
                session['name'] = user_login['name']
                session['email'] = user_login['email']
                return redirect(url_for('profile'))
        flash('Invalid username/password combination')

    return render_template("login.html")

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'email' : request.form['email']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['name'], 'email' : request.form['email'], 'password' : hashpass})
            registered_user = users.find_one({'email' : request.form['email']})
            session['_id'] = str(registered_user['_id'])
            session['name'] = registered_user['name']
            session['email'] = registered_user['email']
            return redirect(url_for('profile'))
        
        flash('That email already exists!')

    return render_template("signup.html")

@app.route('/logout')
def logout():
    session.pop('_id', None)
    session.pop('name', None)
    session.pop('email', None)
    return redirect(url_for('home'))

app.run(debug=True)