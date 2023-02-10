import os 
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

login_manager = LoginManager()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
UPLOAD_FOLDER= r'C:\Users\JDTGaming\Desktop\devMountain\Specialization\Unit 6\Capstone\myproject\static\images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy()

def connect_to_db(flask_app):

    flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['POSTGRES_URI']
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = flask_app
    db.init_app(flask_app)
login_manager.init_app(app)
login_manager.login_view = 'login'