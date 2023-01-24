from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user
from .models import User
from . import db
from . import app, mail
from werkzeug.security import generate_password_hash, check_password_hash
import time
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Message

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
        name = request.form.get('name')
        username = request.form.get('username')
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
            new_user = User(name=name,username=username,email=email,password=generate_password_hash(password_1,method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            flash('User Created! Please Login')
            return redirect(url_for('auth.login'))


    return render_template('signup.html')

@auth.route('logout',methods=['POST'])
def logout():
    '''
    Adding login method name here auth.login so that if the path changes it
    doesn't affect the working.
    '''
    logout_user()
    return redirect(url_for('auth.login'))

def getToken(email):
    serial = Serializer(app.config['SECRET_KEY'],expires_in=300)
    return serial.dumps({'email':f'{email}'}).decode('utf-8')

def verifyToken(token):
    serial = Serializer(app.config['SECRET_KEY'])
    try:
        e_mail = serial.loads(token)['email']
    except:
        return None
    return User.query.filter_by(email=e_mail).first()

def send_mail(e_mail):
    token = getToken(e_mail)
    msg = Message('Password Reset request',recipients=[e_mail],sender='noreply@coc.com')
    msg.body=f'''
    To reset your password, please follow the link below:
    {url_for('auth.resetPassword',token= token)}
    Please ignore if this not done by you.
    '''
    mail.send(msg)

@auth.route('/forget', methods=['GET','POST'])
def forgotPassword():
    if request.method == 'POST':
        email = request.form.get('email')
        emailExist = User.query.filter_by(email=email).first()
        if emailExist:
            send_mail(email)
            
        else:
            flash('Email Id doesn\'t exist in the system!!')

    return render_template('ForgetPassword.html')

@auth.route('/resetPassword/<token>',methods=['GET','POST'])
def resetPassword(token):
    user = verifyToken(token)
    if user is None:
        flash('That is invalid/Expired Token!!','warning')
        return redirect(url_for('forget'))
    
    if request.method == 'POST':
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if password1 != password2:
            flash(f"Password doesn't Match, please try again!!",category='error')
        elif len(password1) < 5:
            flash(f"Password too small, please try again!!",category='error')

        hashed_password = generate_password_hash(password1,method="sha256")
        user.password = hashed_password
        db.session.commit()
        flash('Password Changed!!','success')
        return redirect(url_for('auth.login'))

    return render_template('changePassword.html')
    