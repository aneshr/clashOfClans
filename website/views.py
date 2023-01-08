from flask import Blueprint, render_template
from flask_login import login_required
import requests
'''
A Blueprint is a way to organize a group of related views and other code.
Rather than registering views and other code directly with an application,
they are registered with a blueprint.
Then the blueprint is registered with the application when it is available in the factory function.
EX: bp = Blueprint('auth', __name__, url_prefix='/auth')

The url_prefix will be prepended to all the URLs associated with the blueprint.

'''
views = Blueprint("views",__name__,url_prefix='/')

token = ""


header = {
'Content-type' : 'application/json',
'Authorization' : f'Bearer {token}'
}
    

def clanData(tag):
    clanInfo = requests.get(f"https://api.clashofclans.com/v1/clans/{tag}",headers=header).json()
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

def userData(members):
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
        try:
            obj['league']=info['league']['name']
        except Exception:
            obj['league']='Not Found!!'
        obj['troops']=info['troops']
        obj['spells']=info['spells']
        userInfo.append(obj)
    return userInfo

@views.route('/')
@views.route('home')
@login_required
def home():
    data = clanData('%23PULPQUR8')
    return render_template('homepage.html',data=data)


