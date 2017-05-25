from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class UserEditForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    old_password = PasswordField('old password', validators=[DataRequired()])
    new_password = PasswordField('new password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='passwords must match')
    ])
    confirm = PasswordField('confirm new password')
