from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
bcrypt = Bcrypt(app) # shouldn't matter if you pass in app or not here. just create an instatnce here
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/learn-auth'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'set a super secret key!' # bad practice in general, but we'll live with it for now
db = SQLAlchemy(app)

from project.users.views import users_blueprint

app.register_blueprint(users_blueprint, url_prefix='/users')
