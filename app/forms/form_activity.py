from typing import Optional
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import InputRequired, Optional

class ActivityForm (FlaskForm):
    
    name = StringField('Name :', validators=[InputRequired()])

    description = StringField('Description (optional):')

    date = DateField('Date (format DD/MM/YYYY optional) :', format='%d/%m/%Y', validators=[Optional()])
    
    interval = DateField('Date (format DD/MM/YYYY optional) :', format='%d/%m/%Y', validators=[Optional()])

    submit = SubmitField('Send')