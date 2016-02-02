#all the imports

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bang bang bang'

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500


@app.route('/')
def index():
	return render_template('index.html', current_time = datetime.utcnow())

@app.route('/user/<name>')
def user(name):
	return render_template('user.html', name = name)

@app.route('/signin',methods = ['POST','GET'])
def signin():
	form = NameForm()
	if form.validate_on_submit():
		session['name'] = form.name.data
		return redirect(url_for('signin'))
	return render_template('signin.html', form = form, name = session.get('name'))

@app.route('/contact')
def contact():
	flash('Please check our contact twice to ensure correctly sending.')
	return render_template('contact.html')

class NameForm(Form):
	name = StringField('Input your name please.', validators = [Required()])
	submit = SubmitField('Submit')



if __name__ == '__main__':
	manager.run()
	#app.run()
	
	
