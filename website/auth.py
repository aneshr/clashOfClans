from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
import time
auth = Blueprint("auth",__name__,url_prefix='/')

@auth.route('login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('login')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash("Logged In!",category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Password Incorrect",category='error')
        else:
            flash('User Doesnot Exist',category='error')

    return render_template('login.html')

@auth.route('signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get("emailid")
        password_1 = request.form.get("signuppassword")
        password_2 = request.form.get("signuppassword2")

        emailExists = User.query.filter_by(email=email).first()
        if emailExists:
            flash(f"User with {email} already exists!!",category='error')
        elif password_1!=password_2:
            flash(f"Password doesn't Match, please try again!!",category='error')
        elif len(password_1) < 5:
            flash(f"Password is too small!, Min characters required are 5!",category='error')
        else:
            new_user = User(email=email,password=generate_password_hash(password_1,method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            flash('User Created! Please Login')
            return redirect(url_for('auth.login'))


    return render_template('signup.html')

@auth.route('logout')
def logout():
    '''
    Adding login method name here auth.login so that if the path changes it
    doesn't affect the working.
    '''
    return redirect(url_for('auth.login'))