from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import uuid
from flask_login import LoginManager
from os import path
from flask_mail import Mail
db = SQLAlchemy()
DB_NAME = "cocDB.db"
app = Flask(__name__)

app.config['SECRET_KEY'] = '<SECRET-KEY>'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:hello@localhost:5433/clashOfClans?options=-c%20search_path=cocschema'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '<EMAIL-ID>'
app.config['MAIL_PASSWORD'] = '<APP PASSWORD>'
mail = Mail(app)
def create_app():
       
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