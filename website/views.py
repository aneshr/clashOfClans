from flask import Blueprint

'''
A Blueprint is a way to organize a group of related views and other code.
Rather than registering views and other code directly with an application,
they are registered with a blueprint.
Then the blueprint is registered with the application when it is available in the factory function.
EX: bp = Blueprint('auth', __name__, url_prefix='/auth')

The url_prefix will be prepended to all the URLs associated with the blueprint.

'''
views = Blueprint("views",__name__,url_prefix='/')

@views.route('/')
@views.route('home')
def home():
    return "This is Home Page!<br> WELCOME"


