from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField
from wtforms.validators import EqualTo, InputRequired, ValidationError, Length, Optional
from flask_wtf.file import FileField, FileRequired, FileAllowed
from app.models.user import User

class RegistrationForm (FlaskForm):

  username = StringField('Username:', validators=[InputRequired(), Length(min=2, max=15,\
    message='Username length must be between %(min)d and %(max)d characters')])
  
  firstname = StringField('Firstname:', validators=[InputRequired(), Length(min=2, max=15,\
      message='Firstname length must be between %(min)d and %(max)d characters')])
   
  lastname = StringField('Lastname:', validators=[InputRequired(), Length(min=2, max=15,\
      message='Lastname length must be between %(min)d and %(max)d characters')])
   
  date = DateField('Date of Birth (format DD/MM/YYYY)', format='%d/%m/%Y')

  photo = FileField('Photo:', validators=[FileAllowed(['jfif','png','jpg']) ])

  email = StringField('Email :')

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

class ModifyForm (FlaskForm):
  
  username = StringField('Username:')
  
  firstname = StringField('Firstname:')
   
  lastname = StringField('Lastname:')
   
  date = DateField('Date of Birth (format DD/MM/YYYY)')

  photo = FileField('Photo:')

  email = StringField('Email :')

  password = PasswordField(label= ('Password'))
  
  submit = SubmitField('Change')

# username = StringField('Username:', validators=[Optional(), Length(min=2, max=15,\
#     message='Username length must be between %(min)d and %(max)d characters')])
  
#   firstname = StringField('Firstname:', validators=[Optional(), Length(min=2, max=15,\
#       message='Firstname length must be between %(min)d and %(max)d characters')])
   
#   lastname = StringField('Lastname:', validators=[Optional(), Length(min=2, max=15,\
#       message='Lastname length must be between %(min)d and %(max)d characters')])
   
#   date = DateField('Date of Birth (format DD/MM/YYYY)', format='%d/%m/%Y', validators = [Optional()])

#   photo = FileField('Photo:', validators=[Optional(),FileAllowed(['jfif','png','jpg']) ])

#   email = StringField('Email :')

#   password = PasswordField(label= ('Password'), validators=[Optional(),\
#       Length(min=2, message='Password should be at least %(min)d characters long')])
  