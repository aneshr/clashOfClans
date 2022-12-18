from flask import Blueprint

auth = Blueprint("auth",__name__,url_prefix='/')

@auth.route('login')
def home():
    return "This is Login Page!<br> WELCOME"


