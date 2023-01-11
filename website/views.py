from flask import Blueprint, render_template, request
from flask_login import login_required
import requests
import pymongo
'''
A Blueprint is a way to organize a group of related views and other code.
Rather than registering views and other code directly with an application,
they are registered with a blueprint.
Then the blueprint is registered with the application when it is available in the factory function.
EX: bp = Blueprint('auth', __name__, url_prefix='/auth')

The url_prefix will be prepended to all the URLs associated with the blueprint.

'''
views = Blueprint("views",__name__,url_prefix='/')

client = pymongo.MongoClient('mongodb://localhost:27017/')

db = client['clashofclans']
collection = db['members']

@views.route('/', methods=['GET','POST'])
@views.route('home', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        playerName = request.form.get("member")
        userData = collection.find_one({"name":f"{playerName}"})

        return render_template('userpage.html',userData=userData)
    data = collection.find({},{"name":1,"_id":0})

    return render_template('homepage.html',data=data)