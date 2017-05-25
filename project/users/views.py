from flask import redirect, render_template, request, url_for, Blueprint, flash #, session
from project.users.forms import UserForm, UserEditForm
from project.users.models import User
from project import db, bcrypt
from functools import wraps
from flask_login import login_user, logout_user, current_user, login_required
from IPython import embed

from sqlalchemy.exc import IntegrityError

users_blueprint = Blueprint(
    'users',
    __name__,
    template_folder='templates'
)

# def ensure_logged_in(fn):
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#         if not session.get('user_id'):
#             flash("Please log in first")
#             return redirect(url_for('users.login'))
#         return fn(*args, **kwargs)
#     return wrapper

def ensure_correct_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if kwargs.get('id') != current_user.id:
            flash("Not Authorized")
            return redirect(url_for('users.index'))
        return fn(*args, **kwargs)
    return wrapper

@users_blueprint.route('/')
def index():
    return render_template('index.html', user=User.query.first())

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
        flash("User created! Welcome.")
        return redirect(url_for('users.show', id=new_user.id))
    return render_template('signup.html', form=form)

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.data['username']).first()
        if user and bcrypt.check_password_hash(user.password, form.data['password']):
            flash("You have successfully logged in!")
            # session['user_id'] = user.id
            login_user(user)
            return redirect(url_for('users.show', id=user.id))
        flash("Invalid credentials.")
    return render_template('login.html', form=form)

@users_blueprint.route('/logout')
@login_required
def logout():
	# session.pop('user_id', None)
    logout_user()
    flash('You have been signed out.')
    return redirect(url_for('users.login'))

# @users_blueprint.route('/welcome') # not used anymore
# @login_required # @ensure_logged_in
# def welcome():
#     return render_template('welcome.html')

@users_blueprint.route('/<int:id>/edit')
@login_required
@ensure_correct_user
def edit(id):
    form = UserEditForm()
    return render_template('edit.html', user=User.query.get(id), form=form)

@users_blueprint.route('/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
@login_required
@ensure_correct_user
def show(id):
    found_user = User.query.get(id)
    if request.method == b"DELETE":
        db.session.delete(found_user)
        db.session.commit()
        logout_user()
        return redirect(url_for('users.index'))
    if request.method == b"PATCH":
        form = UserEditForm(request.form)
        if form.validate():
            found_user.username = form.data['username']
            if bcrypt.check_password_hash(found_user.password, form.data['old_password']):
                if form.data['new_password'] == form.data['confirm']:
                    found_user.password = form.data['new_password']
                else:
                    found_user.password = form.data['old_password']
            db.session.add(found_user)
            db.session.commit()
            return redirect(url_for('users.show', id=found_user.id))
        return render_template('edit.html', user=found_user, form=form)
    return render_template('show.html', user=found_user)
