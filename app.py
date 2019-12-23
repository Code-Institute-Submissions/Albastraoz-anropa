import os
from flask import Flask, render_template, redirect, session, request, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt

app = Flask(__name__)

# CONNECTION TO DATABASE
app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')

mongo = PyMongo(app)

# WEB PAGES
# Homepage
@app.route('/')
def home():
    session['tab'] = 'profile_tab'
    return render_template("index.html")

# About us
@app.route('/about_us')
def about_us():
    session['tab'] = 'profile_tab'
    return render_template("aboutus.html")

# VACANCY AREA
# All vacancies
@app.route('/vacancies')
def vacancies():
    session['tab'] = 'profile_tab'
    all_vacancies = mongo.db.vacancies.find()
    return render_template("vacancies.html", vacancies=all_vacancies)

# Full description a specific vacancy
@app.route('/vacancies/<vacancy_id>')
def view_vacancy(vacancy_id):
    if '_id' in session:
        one_user = mongo.db.users.find_one({'_id': ObjectId(session['_id'])})
    else:
        one_user = '0123456789'
    one_vacancies = mongo.db.vacancies.find_one({'_id': ObjectId(vacancy_id)})
    return render_template("vacancy.html", user=one_user, vacancy=one_vacancies)

# Delete a specific vacancy
@app.route('/delete_vacancy/<vacancy_id>')
def delete_vacancy(vacancy_id):
    mongo.db.vacancies.remove({'_id': ObjectId(vacancy_id)})
    return redirect(url_for('vacancies'))

# Edit a specific vacancy
@app.route('/vacancies/edit/<vacancy_id>')
def edit_vacancy(vacancy_id):
    one_user = mongo.db.users.find_one({'_id': ObjectId(session['_id'])})
    one_vacancies = mongo.db.vacancies.find_one({'_id': ObjectId(vacancy_id)})
    return render_template("edit_vacancy.html", user=one_user, vacancy=one_vacancies)

# Save changes of specific vacancy
@app.route('/vacancies/saved/<vacancy_id>', methods=['POST'])
def save_vacancy(vacancy_id):
    mongo.db.vacancies.update_one({'_id' : ObjectId(vacancy_id)}, {"$set":
        {'vacancy_title' : request.form['edit_vacancy_title'], 
        'vacancy_description' : request.form['edit_vacancy_description']
    }})
    return redirect(url_for('view_vacancy', vacancy_id=vacancy_id))

# Employees
@app.route('/employees')
def employees():
    session['tab'] = 'profile_tab'
    return render_template("employees.html")

# Employers
@app.route('/employers')
def employers():
    session['tab'] = 'profile_tab'
    return render_template("employers.html")

# Contact
@app.route('/contact')
def contact():
    session['tab'] = 'profile_tab'
    return render_template("contact.html")

# ACCOUNT FUNCTIONALITY
# Load profile page
@app.route('/profile/<user>')
def profile(user):
    if session['_id'] is not None:
        one_user = mongo.db.users.find_one({'_id': ObjectId(session['_id'])})
        all_users = mongo.db.users.find()
        return render_template("profile.html", tab=session['tab'], user=one_user, users=all_users)
    else:
        return redirect(url_for('home'))

# Save changes to profile
@app.route('/profile/updated/<user>', methods=['POST'])
def profile_update(user):
    session['tab'] = 'profile_tab'
    all_users = mongo.db.users.find()
    one_user = mongo.db.users.find_one({'_id': ObjectId(session['_id'])})
    # Update databse information
    mongo.db.users.update_one({'_id' : ObjectId(session['_id'])}, {"$set":
        {'name' : request.form['name'], 
        'address' : request.form['address'], 
        'city' : request.form['city'], 
        'zipcode' : request.form['zipcode'],
        'country' : request.form['country']
    }})
    flash('Your information has been updated succesfully!')
    return render_template("profile.html", tab=session['tab'], user=one_user, users=all_users)

# Update CV of profile
@app.route('/profile/cv_updated/<user>', methods=['POST'])
def cv_update(user):
    session['tab'] = 'cv_tab'
    all_users = mongo.db.users.find()
    one_user = mongo.db.users.find_one({'_id': ObjectId(session['_id'])})
    mongo.db.users.update_one({'_id' : ObjectId(session['_id'])}, {"$set":
        {'current_job' : request.form['current_job']}})
    # Check if file is chosen
    if 'cv_file' in request.files:
        cv_file = request.files['cv_file']
        # Check if filename is not empty
        if cv_file.filename != "":
            mongo.save_file(cv_file.filename, cv_file)
            mongo.db.users.update_one({'_id' : ObjectId(session['_id'])}, {"$set":
            {'cv_file' : cv_file.filename}})
    flash('Your information has been updated succesfully!')
    return render_template("profile.html", tab=session['tab'], user=one_user, users=all_users)

# Location to files
@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)

# ADMIN AREA
# Add vacancy
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
# Login user
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        # Check if entered email exists in database
        user_login = users.find_one({'email' : request.form['email']})
        # Continue if not
        if user_login:
            # Check if password is correct
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), user_login['password']) == user_login['password']:
                session['_id'] = str(user_login['_id'])
                session['tab'] = 'profile_tab'
                return redirect(url_for('profile', user=session['_id']))
        flash('Invalid username/password combination')
    return render_template("login.html")

# Signup new user
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        # Check if entered email already exists in database
        existing_user = users.find_one({'email' : request.form['email']})
        # If no match is found it will continue and create user
        if existing_user is None:
            # Hash password for security
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['name'], 'email' : request.form['email'], 'password' : hashpass, 'admin' : False})
            registered_user = users.find_one({'email' : request.form['email']})
            session['_id'] = str(registered_user['_id'])
            session['tab'] = 'profile_tab'
            return redirect(url_for('profile', user=session['_id']))
        flash('That email already exists!')
    return render_template("signup.html")

# Log user out from website
@app.route('/logout')
def logout():
    session.pop('_id', None)
    session.pop('name', None)
    session.pop('email', None)
    session.pop('tab', None)
    return redirect(url_for('home'))

# Run app
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)