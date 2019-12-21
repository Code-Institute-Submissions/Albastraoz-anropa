import os
from flask import Flask, render_template, redirect, session, request, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'anropa'
app.config["MONGO_URI"] = 'mongodb://localhost/anropa'
app.secret_key = 'mysecret'

mongo = PyMongo(app)

# WEB PAGES

@app.route('/')
def home():
    session['tab'] = 'profile_tab'
    return render_template("index.html")

@app.route('/about_us')
def about_us():
    session['tab'] = 'profile_tab'
    return render_template("aboutus.html")


@app.route('/vacancies')
def vacancies():
    session['tab'] = 'profile_tab'
    all_vacancies = mongo.db.vacancies.find()
    return render_template("vacancies.html", vacancies=all_vacancies)

@app.route('/vacancies/<vacancy_id>')
def view_vacancy(vacancy_id):
    if '_id' in session:
        one_user = mongo.db.users.find_one({'_id': ObjectId(session['_id'])})
    else:
        one_user = '0123456789'
    one_vacancies = mongo.db.vacancies.find_one({'_id': ObjectId(vacancy_id)})
    return render_template("vacancy.html", user=one_user, vacancy=one_vacancies)

@app.route('/delete_vacancy/<vacancy_id>')
def delete_vacancy(vacancy_id):
    mongo.db.vacancies.remove({'_id': ObjectId(vacancy_id)})
    return redirect(url_for('vacancies'))

@app.route('/vacancies/edit/<vacancy_id>')
def edit_vacancy(vacancy_id):
    one_user = mongo.db.users.find_one({'_id': ObjectId(session['_id'])})
    one_vacancies = mongo.db.vacancies.find_one({'_id': ObjectId(vacancy_id)})
    return render_template("edit_vacancy.html", user=one_user, vacancy=one_vacancies)

@app.route('/vacancies/saved/<vacancy_id>', methods=['POST'])
def save_vacancy(vacancy_id):
    mongo.db.vacancies.update_one({'_id' : ObjectId(vacancy_id)}, {"$set":
        {'vacancy_title' : request.form['edit_vacancy_title'], 
        'vacancy_description' : request.form['edit_vacancy_description']
    }})
    return redirect(url_for('view_vacancy', vacancy_id=vacancy_id))


@app.route('/employees')
def employees():
    session['tab'] = 'profile_tab'
    return render_template("employees.html")

@app.route('/employers')
def employers():
    session['tab'] = 'profile_tab'
    return render_template("employers.html")

@app.route('/contact')
def contact():
    session['tab'] = 'profile_tab'
    return render_template("contact.html")

# Account functionality
@app.route('/profile/<user>')
def profile(user):
    if session['_id'] is not None:
        one_user = mongo.db.users.find_one({'_id': ObjectId(session['_id'])})
        all_users = mongo.db.users.find()
        return render_template("profile.html", tab=session['tab'], user=one_user, users=all_users)
    else:
        return redirect(url_for('home'))

@app.route('/profile/updated/<user>', methods=['POST'])
def profile_update(user):
    session['tab'] = 'profile_tab'
    all_users = mongo.db.users.find()
    one_user = mongo.db.users.find_one({'_id': ObjectId(session['_id'])})
    mongo.db.users.update_one({'_id' : ObjectId(session['_id'])}, {"$set":
        {'name' : request.form['name'], 
        'address' : request.form['address'], 
        'city' : request.form['city'], 
        'zipcode' : request.form['zipcode'],
        'country' : request.form['country']
    }})
    flash('Your information has been updated succesfully!')
    return render_template("profile.html", tab=session['tab'], user=one_user, users=all_users)

@app.route('/profile/cv_updated/<user>', methods=['POST'])
def cv_update(user):
    session['tab'] = 'cv_tab'
    all_users = mongo.db.users.find()
    one_user = mongo.db.users.find_one({'_id': ObjectId(session['_id'])})
    mongo.db.users.update_one({'_id' : ObjectId(session['_id'])}, {"$set":
        {'current_job' : request.form['current_job']}})
    if 'cv_file' in request.files:
        cv_file = request.files['cv_file']
        if cv_file.filename is not "":

            #file_object = mongo.db.fs.files.find_one({'filename': str(one_user.cv_file)})
            #file_id = file_object.get('_id')
            #mongo.db.fs.chunks.remove({'files_id': ObjectId(file_id)})
            #mongo.db.fs.files.remove({'_id': ObjectId(file_id)})

            mongo.save_file(cv_file.filename, cv_file)
            mongo.db.users.update_one({'_id' : ObjectId(session['_id'])}, {"$set":
            {'cv_file' : cv_file.filename}})
    flash('Your information has been updated succesfully!')
    return render_template("profile.html", tab=session['tab'], user=one_user, users=all_users)

@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)

# Admin area

@app.route('/add_vacancy', methods=['POST'])
def add_vacancy():
    session['tab'] = 'vacancy_tab'
    vacancy = mongo.db.vacancies
    all_users = mongo.db.users.find()
    one_user = mongo.db.users.find_one({'_id': ObjectId(session['_id'])})
    vacancy.insert({'vacancy_title' : request.form['add_vacancy_title'], 'vacancy_description' : request.form['add_vacancy_description']})
    flash('Vacancy added to the database!')
    return render_template("profile.html", tab=session['tab'], user=one_user, users=all_users)

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
                session['tab'] = 'profile_tab'
                return redirect(url_for('profile', user=session['_id']))
        flash('Invalid username/password combination')

    return render_template("login.html")

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'email' : request.form['email']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['name'], 'email' : request.form['email'], 'password' : hashpass, 'admin' : False})
            registered_user = users.find_one({'email' : request.form['email']})
            session['_id'] = str(registered_user['_id'])
            session['name'] = registered_user['name']
            session['email'] = registered_user['email']
            session['tab'] = 'profile_tab'
            return redirect(url_for('profile', user=session['_id']))
        
        flash('That email already exists!')

    return render_template("signup.html")

@app.route('/logout')
def logout():
    session.pop('_id', None)
    session.pop('name', None)
    session.pop('email', None)
    session.pop('tab', None)
    return redirect(url_for('home'))

app.run(debug=True)