import os
import env
import random
import string
from flask import Flask, render_template, redirect, session, request, url_for, flash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt

app = Flask(__name__)

# MAIN FLASK SETTINGS
app.config["SERVER_NAME"] = os.environ.get('SERVER_NAME')
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')

# CONNECTION TO DATABASE
app.config["MONGO_DBNAME"] = os.environ.get('MONGO_DBNAME')
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

# EMAIL SERVICE SETTINGS
app.config["MAIL_SERVER"] = os.environ.get('MAIL_SERVER')
app.config["MAIL_PORT"] = os.environ.get('MAIL_PORT')
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.environ.get('MAIL_USERNAME')
app.config["MAIL_PASSWORD"] = os.environ.get('MAIL_PASSWORD')
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get('MAIL_DEFAULT_SENDER')
app.config["MAIL_MAX_EMAILS"] = 5
app.config["MAIL_ASCII_ATTACHMENTS"] = False

mongo = PyMongo(app)
mail = Mail(app)

st = URLSafeTimedSerializer(app.config['SECRET_KEY'])
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

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

# Full description of a specific vacancy
@app.route('/vacancies/<vacancy_id>', methods=["GET", "POST"])
def view_vacancy(vacancy_id):
    one_vacancies = mongo.db.vacancies.find_one({'_id': ObjectId(vacancy_id)})
    if request.method == 'POST':
        one_user = mongo.db.users.find_one({'_id': ObjectId(session['_id'])})
        msg = Message('Job application', sender=one_user["email"], recipients=['rkaal7@gmail.com'])
        msg.html = 'Applicants name:{}<br>Applicants email:{}<br>Vacancy:<br>{}'.format(one_user["name"], one_user["email"], one_vacancies["vacancy_title"])
        mail.send(msg)
        flash('Your application has been send!')
        return render_template("vacancy.html", user=one_user, vacancy=one_vacancies)
    if '_id' in session:
        one_user = mongo.db.users.find_one({'_id': ObjectId(session['_id'])})
    else:
        one_user = '0123456789'
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

# SEND EMAIL FROM CONTACT FORM
@app.route('/contact/send_email', methods=['POST'])
def send_email():
    contact_name = request.form.get('contact_name')
    contact_email = request.form.get('contact_email')
    contact_message = request.form.get('contact_message')
    msg = Message('website contact form', sender=contact_email, recipients=['rkaal7@gmail.com'])
    msg.html = 'Contact name:{}<br>Contact email:{}<br>Message:<br>{}'.format(contact_name, contact_email, contact_message)
    mail.send(msg)
    flash('Your email has been send!')
    return render_template("contact.html")

# ACCOUNT FUNCTIONALITY
# Check for secure files
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Location to files
@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)

# Load profile page
@app.route('/profile/<user>', methods=["GET", "POST"])
def profile(user):
    if request.method == 'POST':
        all_users = mongo.db.users.find()
        one_user = mongo.db.users.find_one({'_id': ObjectId(session['_id'])})
        # Check which form is used
        if 'name' in request.form:
            session['tab'] = 'profile_tab'
            mongo.db.users.update_one({'_id' : ObjectId(session['_id'])}, {"$set":
                {'name' : request.form['name'], 
                'phone' : request.form['phone'],
                'address' : request.form['address'], 
                'city' : request.form['city'], 
                'zipcode' : request.form['zipcode'],
                'country' : request.form['country']
            }})
            flash('Your information has been updated succesfully!')
            return redirect(url_for('profile', user=session['_id']))
        # Check which form is used
        elif 'current_job' in request.form:
            session['tab'] = 'cv_tab'
            mongo.db.users.update_one({'_id' : ObjectId(session['_id'])}, {"$set":
                {'current_job' : request.form['current_job']}})
            # Check if file is chosen
            if 'cv_file' in request.files:
                cv_file = request.files['cv_file']
                # Check if filename is not empty
                if cv_file.filename != "":
                    lettersAndDigits = string.ascii_letters + string.digits
                    filenamegen = ''.join(random.choice(lettersAndDigits) for i in range(40)) + cv_file.filename

                    mongo.save_file(filenamegen, cv_file)
                    mongo.db.users.update_one({'_id' : ObjectId(session['_id'])}, {"$push":
                    {'cv_file' : filenamegen}})
            flash('Your information has been updated succesfully!')
            return redirect(url_for('profile', user=session['_id']))
    if session['_id'] is not None:
        one_user = mongo.db.users.find_one({'_id': ObjectId(session['_id'])})
        all_users = mongo.db.users.find()
        return render_template("profile.html", tab=session['tab'], user=one_user, users=all_users)
    else:
        return redirect(url_for('home'))

# Delete a file
@app.route('/file/delete/<del_file>')
def delete_file(del_file):
    session['tab'] = 'cv_tab'
    # Find files_id to delete both in fs.files & fs.chunks
    chunks_id = mongo.db.fs.files.find_one({'filename': del_file})
    mongo.db.fs.chunks.delete_many({'files_id': ObjectId(chunks_id['_id'])})
    mongo.db.fs.files.delete_one({'filename': del_file})
    mongo.db.users.update_one({'_id' : ObjectId(session['_id'])}, {"$pull":
                    {'cv_file' : del_file}})
    flash('Your file has been removed!')
    return redirect(url_for('profile', user=session['_id']))

# ADMIN AREA
# Search for user
@app.route('/search-user', methods=['POST'])
def find_user():
    session['tab'] = 'users_tab'
    search = request.form['search']
    one_user = mongo.db.users.find_one({'_id': ObjectId(session['_id'])})
    all_users = mongo.db.users.find()
    search_user = mongo.db.users.find({'email': search })
    return render_template("profile.html", tab=session['tab'], user=one_user, users=all_users, result=search_user)

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
                if user_login['verified'] == True:
                    session['_id'] = str(user_login['_id'])
                    session['tab'] = 'profile_tab'
                    return redirect(url_for('profile', user=session['_id']))
                flash('Account is not verified! Please check your email or resend a confirmation email <a href="/request-activation">here</a>.')
        flash('Invalid username/password combination')
    return render_template("login.html")

# Request to reset password
@app.route('/request-password-reset', methods=['POST', 'GET'])
def request_password_reset():
    if request.method == 'POST':
        users = mongo.db.users
        email = request.form['email-password']
        # Check if entered email already exists in database
        existing_user = users.find_one({'email' : email})
        # If no match is found it will continue and send email to reset password
        if existing_user:
            # Create token for password reset
            token = st.dumps(email, salt='reset-password')

            # Send confirmation email
            msg = Message('Anropa Password Reset', recipients=[email])
            link = url_for('reset_password', token=token, _external=True)
            msg.html = 'You send in a request to reset your password.<br>If this was not you ignore this email.<br>If this was you, here is your recovery link (valid for 2 hours):<br> {}'.format(link)
            mail.send(msg)

            flash('Recovery link send to your email address.')
        flash('That email does not exists!')
    return render_template("password_reset.html")

# Reset password
@app.route('/reset/<token>', methods=['POST', 'GET'])
def reset_password(token):
    try:
        email = st.loads(token, salt='reset-password', max_age=7200)
    except SignatureExpired:
        return render_template("password_reset_denied.html")
    
    email = st.loads(token, salt='reset-password')
    if request.method == 'POST':
        if request.form['reset-password'] != request.form['reset-password2']:
            flash('Passwords are not the same!')
            return redirect(url_for('reset_password', token=token))

        # Hash password for security
        hashpass = bcrypt.hashpw(request.form['reset-password'].encode('utf-8'), bcrypt.gensalt())

        # Update password by finding user by email.
        mongo.db.users.update_one({'email' : email}, {"$set":
            {'password' : hashpass }})
        flash('Your password has been reset! You can <a href="/login">login here</a>.')
    return render_template("password_reset_form.html", token=token)

# Signup new user
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        # Check if entered email already exists in database
        existing_user = users.find_one({'email' : request.form['email']})
        # If no match is found it will continue and create user
        if existing_user is None:
            if request.form['password'] != request.form['password2']:
                flash('Passwords are not the same!')
                return render_template("signup.html")
                
            # Create token for email verification
            email = request.form['email']
            token = st.dumps(email, salt='confirm_email')

            # Hash password for security
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())

            # Insert user into database
            users.insert({'name' : request.form['name'], 'email' : email, 'verified' : False, 'password' : hashpass, 'admin' : False})

            # Send confirmation email
            msg = Message('Anropa Confirm Email', recipients=[email])
            link = url_for('confirm_email', token=token, _external=True)
            msg.html = 'You need to activate your account at Anropa.<br> Here is your confirmation link: {}'.format(link)
            mail.send(msg)

            return redirect(url_for('email_confirmation_page'))
        flash('That email already exists!')
    return render_template("signup.html")

# This page is rendered after you registered your account successfully
@app.route('/activate-account')
def email_confirmation_page():
    return render_template("email_confirm_send.html")

# Send a new activation link page
@app.route('/request-activation', methods=['POST', 'GET'])
def confirm_email_form():
    if request.method == 'POST':
        users = mongo.db.users
        email = request.form['email-link']
        # Check if entered email already exists in database
        existing_user = users.find_one({'email' : email})
        # If no match is found it will continue and create user
        if existing_user:
            if existing_user['verified'] == False:
                # Create token for email verification
                token = st.dumps(email, salt='confirm_email')

                # Send confirmation email
                msg = Message('Anropa Confirm Email', recipients=[email])
                link = url_for('confirm_email', token=token, _external=True)
                msg.html = 'You need to activate your account at Anropa.<br> Here is your confirmation link:<br> {}'.format(link)
                mail.send(msg)
                return redirect(url_for('email_confirmation_page'))
            flash('Your account has already been verified please <a href="/login">login here</a>.')
        flash('That email does not exists!')
    return render_template("email_confirm.html")

# Confirm email address
@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = st.loads(token, salt='confirm_email', max_age=86400)
    except SignatureExpired:
        return render_template("email_confirmation_denied.html")
    
    email = st.loads(token, salt='confirm_email')
    mongo.db.users.update_one({'email' : email}, {"$set":
        {'verified' : True }})
    return render_template("email_confirmation_success.html")

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
    app.run()

# host=os.environ.get('IP'), port=int(os.environ.get('PORT')), debug=True