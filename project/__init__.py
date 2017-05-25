from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/learn-auth'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'set a super secret key!' # bad practice in general, but we'll live with it for now
login_manager.login_view = "users.login"

bcrypt = Bcrypt(app) # shouldn't matter if you pass in app or not here. just create an instatnce here
modus = Modus(app)
db = SQLAlchemy(app)


from project.users.views import users_blueprint

app.register_blueprint(users_blueprint, url_prefix='/users')

from project.users.models import User

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
def root():
    return "learn-auth app, start at /users/"