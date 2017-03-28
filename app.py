from flask import Flask, render_template, url_for, redirect, request, session, flash, g
from flask_apscheduler import APScheduler
from flask_restful import Resource, Api, reqparse
from functools import wraps
from flask.ext.mysql import MySQL
from flask.ext.bcrypt import Bcrypt
import logging

from models import *
from tasks import *

app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)
app.secret_key = 'alldefdigital'

logging.basicConfig()

# internal functions #
def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('You need to login first.')
		return redirect(url_for('login'))
	return wrap

# context processors #

@app.context_processor
def my_utility_processor():
	def foo():
		print "Bullshit."

	def get_date(a):
		query = get_last_date(a)
		return query[0]

	return dict(foo=foo, get_date=get_date)

# views #
# logout method #
@app.route('/logout', methods=['GET'])
@login_required
def logout():
	session['logged_in'] = False
	flash('You were just logged out!')
	return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
	return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
   	
   	page = 'Login'

		# begin Login function #

	error = None

	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		x = get_login_credentials(username, password)
		if x == True:
			session['logged_in'] = True
			session['username'] = username
			flash('You were just logged in.')
			return redirect(url_for('add'))
		else:
			error = "Invalid Credentials. Please try again."

	return render_template('login.html', error=error, page=page)

# add #
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
	error = None
	page = 'Add'

	return render_template('add.html', page=page, error=error)

# all #
@app.route('/all')
@login_required
def all():
	error = None
	page = 'All Repos'

	data = get_distinct_Repos()
	print data

	return render_template('all.html', page=page, error=error, data=data)

@app.route('/settings')
@login_required
def settings():
	error = None
	page = 'Settings'

	data = get_Settings_data()
	atid = data[1]
	atsk = data[2]
	buf = data[3]
	print buf
	backups = data[4]

	return render_template('settings.html', page=page, error=error, atid=atid, atsk=atsk, buf=buf, backups=backups)

######## HARD API ############

class AddRepo(Resource):
	def post(self):

		parser = reqparse.RequestParser()
		parser.add_argument('at', type=str, help='AT of the Repo...')
		parser.add_argument('url', type=str, help='Url of the Repo...')
		parser.add_argument('name', type=str, help='Name of the Repo...')
		args = parser.parse_args()

		_at = args['at']
		_url = args['url']
		_name = args['name']

		x = clone_repo(_at, _url, _name)

		return x

class Setts(Resource):
	def post(self):

		parser = reqparse.RequestParser()
		parser.add_argument('atid', type=str, help='Access Token ID of your AWS account.')
		parser.add_argument('atsk', type=str, help='Access Token Secret Key of your AWS account.')
		parser.add_argument('buf', type=str, help='Backup Frequency of all your Github Repos.')
		parser.add_argument('backups', type=str, help='Switch backups on or off.')
		parser.add_argument('type', type=str, help='Type of request (backend).')
		args = parser.parse_args()

		print args

		_atid = args['atid']
		_atsk = args['atsk']
		_buf = args['buf']
		_backups = args['backups']
		_type = args['type']

		return action_Settings(_atid, _atsk, _buf, _backups)

api.add_resource(AddRepo, '/api/repo')
api.add_resource(Setts, '/api/settings')

if __name__ == '__main__':
	app.config.from_object(Config())

	scheduler = APScheduler()
	scheduler.init_app(app)
	scheduler.start()

	app.run(host='0.0.0.0')
