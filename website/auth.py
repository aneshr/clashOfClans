from flask import Blueprint, render_template, redirect, url_for

auth = Blueprint("auth",__name__,url_prefix='/')

@auth.route('login')
def login():
    return render_template('login.html')

@auth.route('signup', methods=['GET','POST'])
def signup():
    return render_template('signup.html')

@auth.route('logout')
def logout():
    '''
    Adding login method name here auth.login so that if the path changes it
    doesn't affect the working.
    '''
    return redirect(url_for('auth.login'))