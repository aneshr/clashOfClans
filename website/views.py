from flask import Blueprint, render_template, request,redirect, url_for
from flask_login import login_required, current_user
import requests
from .models import User
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
collection = db['userdatamap']

def clanData(tag,token,header):
    clanInfo = requests.get(f"https://api.clashofclans.com/v1/clans/{tag}",headers=header).json()
    #print(clanInfo)
    clanName = clanInfo['name']
    clanLevel = clanInfo['clanLevel']
    totalMembers = clanInfo['members']
    description = clanInfo['description']
    memberData = []
    for member in clanInfo['memberList']:
        obj = {}
        obj['playerTag']=member['tag']
        obj['name']=member['name']
        memberData.append(obj)
    clanData = {
        "name": clanName,"level":clanLevel,"TotalMembers":totalMembers,"Description":description,"member-data":memberData
    }
    return clanData



def userData(members,token,header):
    userInfo = []
    for data in members:
        tag = data['playerTag'].replace('#',"%23")
        info = requests.get(f"https://api.clashofclans.com/v1/players/{tag}",headers=header).json()
        obj = {}
        obj['name'] = info['name']
        obj['THLevel'] = info['townHallLevel']
        obj['exp'] = info['expLevel']
        obj['trophy'] = info['trophies']
        obj['role']=info['role']
        obj['heroes']=info['heroes']
        try:
            obj['league']=info['league']['name']
        except Exception:
            obj['league']='Not Found!!'
        obj['troops']=info['troops']
        obj['spells']=info['spells']
        userInfo.append(obj)
    return userInfo


@views.route('/', methods=['GET','POST'])
@views.route('home', methods=['GET','POST'])
@login_required
def home():
    db = client['clashofclans']
    collection = db['userdatamap']
    current_user_data = User.query.filter_by(id=current_user.id).first()
    mail = current_user_data.email
    if request.method == 'POST':
        playerName = request.form.get("member")
        userData = collection.find_one({"usermail":f"{mail}"})['data']
        print(playerName, userData)
        
        res=""
        for user in userData:
            if user['name'] == playerName:
                res = user
                break
        return render_template('userpage.html',userData=res)
    
    
    data = collection.find_one({"usermail":f"{mail}"})['data']    
    
    return render_template('homepage.html',data=data)

@views.route('/getToken', methods=['GET','POST'])
@login_required
def getToken():
    if request.method == 'POST':
        token = request.form.get('token')
        clanTag = request.form.get('clantag')
        header = {
        'Content-type' : 'application/json',
        'Authorization' : f'Bearer {token}'
        }
        current_user_data = User.query.filter_by(id=current_user.id).first()
        mail = current_user_data.email
        db = client['clashofclans']
        collection = db['userdatamap']
        checkuser = collection.find_one({"usermail":f"{mail}"})
        try:
            clan_data = clanData(clanTag.replace('#',"%23"),token,header)
            usersdata = userData(clan_data['member-data'],token,header)
        except Exception as e:
            return f"Invalid Token or Ip Address not whitelisted!! {e}"
        message = ""
        if checkuser == None:
            #Need to get data in Mongo DB
            collection.insert_one(
                                {"usermail":f"{mail}",
                                "data":usersdata}
                                )
        else:
            collection.update_one(
                {"usermail":f"{mail}"},
                {
                    "$set": {
                    "usermail":f"{mail}",
                    "data":usersdata
                }
                })
            
        return redirect(url_for('views.home'))
    return render_template('token.html')
        

