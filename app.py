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

# Account functionality
@app.route('/profile')
def profile():
    if session.get('_id') is not None:
        one_user = mongo.db.users.find_one({'_id': ObjectId(session['_id'])})
        users = mongo.db.users
        if users.admin:
            all_vacancies = mongo.db.vacancies.find()
            return render_template("profile.html", user=one_user, vacancies=all_vacancies)
        return render_template("profile.html", user=one_user)
    else:
        return redirect(url_for('home'))

@app.route('/profile_update', methods=['POST'])
def profile_update():
    users = mongo.db.users
    users.update_one({'_id' : ObjectId(session['_id'])}, {"$set":
        {'name' : request.form['name'], 
        'address' : request.form['address'], 
        'city' : request.form['city'], 
        'zipcode' : request.form['zipcode'],
        'country' : request.form['country']
    }})
    flash('Your information has been updated succesfully!')
    return redirect(url_for('profile'))

@app.route('/cv_update', methods=['POST'])
def cv_update():
    users = mongo.db.users
    cv_file = request.files['cv_file']
    mongo.save_file(cv_file.filename, cv_file)
    users.update_one({'_id' : ObjectId(session['_id'])}, {"$set":
        {'current_job' : request.form['current_job'],
        'cv_file' : cv_file.filename
    }})
    flash('Your information has been updated succesfully!')
    return redirect(url_for('profile'))

@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)

# Admin area

@app.route('/add_vacancy', methods=['POST'])
def add_vacancy():
    vacancy = mongo.db.vacancies
    vacancy.insert({'vacancy_title' : request.form['add_vacancy_title'], 'vacancy_description' : request.form['add_vacancy_description']})
    flash('Vacancy added to the database!')
    return redirect(url_for('profile'))

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