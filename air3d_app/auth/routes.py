from flask import Blueprint, request, render_template, redirect, url_for, flash
# from flask_login import login_user, logout_user, login_required, current_user
import firebase_admin
import pyrebase
import json
from firebase_admin import credentials

from air3d_app.models import User
from air3d_app.auth.forms import SignUpForm, LoginForm
from air3d_app import bcrypt

# Import app and db from events_app package so that we can run app
from air3d_app import app, db

auth = Blueprint("auth", __name__)

#Connect to firebase
cred = credentials.Certificate('./firebaseAdminConfig.json')
firebase = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(json.load(open('./firebase_config.json')))

#Data source
users = [{'uid': 1, 'name': 'Noah Schairer'}]

#API route to get users
@auth.route('/api/userinfo')
def userinfo():
    return {'data': users}, 200

#API route to sign up a new user
@auth.route('/api/signup')
def signup():
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or password is None:
        return {'message': 'Error missing email or password'},400
    try:
        user = firebase_admin.auth.create_user(
               email=email,
               password=password
        )
        return {'message': f'Successfully created user {user.uid}'},200
    except:
        return {'message': 'Error creating user'},400

#API route to get a new token for a valid user
@auth.route('/api/token')
def token():
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = pb.auth().sign_in_with_email_and_password(email, password)
        jwt = user['idToken']
        return {'token': jwt}, 200
    except:
        return {'message': 'There was an error logging in'},400

# @auth.route('/signup', methods=['GET', 'POST'])
# def signup():
#     form = SignUpForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user = User(
#             username=form.username.data,
#             password=hashed_password
#         )
#         db.session.add(user)
#         db.session.commit()
#         flash('Account Created.')
#         return redirect(url_for('auth.login'))
#     print(form.errors)
#     return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=True)
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('main.homepage'))
    print(form.errors)
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))
