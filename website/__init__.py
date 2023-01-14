from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import uuid
from flask_login import LoginManager
from os import path

db = SQLAlchemy()
DB_NAME = "cocDB.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '6fa459ea-ee8a-3ca4-894e-db77e160355e'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:hello@localhost:5433/clashOfClans?options=-c%20search_path=cocschema'

    db.init_app(app)
    
    from .models import User

    loginManager = LoginManager()
    loginManager.login_view = "auth.login"

    loginManager.init_app(app)

    @loginManager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from .views import views
    from .auth import auth
    app.register_blueprint(views)
    app.register_blueprint(auth)
    return app