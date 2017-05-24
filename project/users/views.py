from flask import redirect, render_template, request, url_for, Blueprint, flash
from project.users.forms import UserForm
from project.users.models import User
from project import db, bcrypt

from sqlalchemy.exc import IntegrityError

users_blueprint = Blueprint(
    'users',
    __name__,
    template_folder='templates'
)

@users_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserForm(request.form) # create a form instance using UserForm
    if form.validate_on_submit(): # check the form method and if it's a POST/validate...
        try: # w/o try-except block, server would crash
            new_user = User(form.data['username'], form.data['password'])
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError as e: # error-type in sql-alchemy if something goes wrong
            flash("Username already taken.")
            return render_template('signup.html', form=form)
        flash("User created! Please log in to continue.")
        return redirect(url_for('users.login'))
    return render_template('signup.html', form=form)

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.data['username']).first()
        if user and bcrypt.check_password_hash(user.password, form.data['password']):
            flash("You have successfully logged in!")
            return redirect(url_for('users.welcome'))
        flash("Invalid credentials.")
    return render_template('login.html', form=form)

@users_blueprint.route('/welcome')
def welcome():
    return render_template('welcome.html')

@users_blueprint.route('/')
def root():
    return "Please start at /users/welcome, for now" # note to self, for now
