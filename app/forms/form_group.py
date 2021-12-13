from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList,FormField
from wtforms.validators import InputRequired,Length

class invitedForm (FlaskForm):
    username = StringField('Username :', validators=[InputRequired(), Length(min=2, max=15,\
    message='Username length must be between %(min)d and %(max)d characters')])

class newGroup (FlaskForm):

    name = StringField('Name :', validators=[InputRequired()])

    invited = FieldList(FormField(invitedForm), min_entries=1)

    submit = SubmitField('Send')


