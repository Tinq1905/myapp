#all the imports
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bang bang bang'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

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
        user=User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('signin'))
    return render_template('signin.html', form = form, name = session.get('name'), known=session.get('known',False))

@app.route('/contact')
def contact():
	flash('Please check our contact twice to ensure correctly sending.')
	return render_template('contact.html')

class NameForm(Form):
	name = StringField('Input your name please.', validators = [Required()])
	submit = SubmitField('Submit')

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


if __name__ == '__main__':
	manager.run()
	#app.run()
	
	
