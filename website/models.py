from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):

    __tablename__= "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    timestamp = db.Column(db.DateTime(timezone=True),default=func.now())

    def __init__(self,name,username,email,password):
        self.name = name
        self.username = username
        self.email = email
        self.password = password