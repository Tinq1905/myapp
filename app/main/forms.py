from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class NameForm(Form):
	name = StringField('Input your name please.', validators = [Required()])
	submit = SubmitField('Submit')