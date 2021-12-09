from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import EqualTo, InputRequired, ValidationError, Length
from models.user import User


class RegistrationForm (FlaskForm):

  username = StringField('Username:', validators=[InputRequired(), Length(min=2, max=15,\
    message='Username length must be between %(min)d and %(max)d characters')])
  
  password = PasswordField(label= ('Password'), validators=[InputRequired(),\
      Length(min=2, message='Password should be at least %(min)d characters long')])
  
  confirmPassword = PasswordField(label= ('Confirm Password'), validators=[InputRequired(message='*Required'),\
    EqualTo('password', message='Both password fields must be equal !')])
  
  submit = SubmitField('Register')

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user is not None:
      raise ValidationError('Please use a different username.')

class LoginForm (FlaskForm):
  
  username = StringField('Username :', validators=[InputRequired(), Length(min=2, max=15,\
    message='Username length must be between %(min)d and %(max)d characters')])
   
  password = PasswordField(label= ('Password'), validators=[InputRequired(),\
    Length(min=2, message='Password should be at least %(min)d characters long')])
   
  submit = SubmitField('Login')
