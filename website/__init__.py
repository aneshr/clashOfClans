from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import uuid
db = SQLAlchemy()
DB_NAME = "cocDB.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '6fa459ea-ee8a-3ca4-894e-db77e160355e'
    app.config['SQL_ALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)
    
    from .views import views
    from .auth import auth
    app.register_blueprint(views)
    app.register_blueprint(auth)
    return app


