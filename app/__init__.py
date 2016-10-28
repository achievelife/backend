import os
import thread
import sys

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from flask import Flask
from flask_jsonpify import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///achievelife.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Setup scheduler
scheduler = BackgroundScheduler()

# Setup extensions
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

# Add all the models
from app import models

##########################
# Utility function to    #
# return a JSON Response #
##########################
def respond(message, data={}, code=200):
	response = {
		'code': code,
		'message': message
	}

	if data:
		response.update(data)

	return jsonify(response)

##########################
# Utility function to    #
# return check all POST  #
# params                 #
##########################
def check_params(request, params):
	missing = []
	for param in params:
		if param not in request.form.keys():
			missing.append(param)

	if missing:
		raise StandardError("You are missing the following paramaters: %s" % ', '.join(missing))

##########################
# Utility function to    #
# validate a session     #
##########################
def validate_session(session):
	session = models.Session.query.filter(models.Session.session == session).first()

	if not session:
		raise StandardError("Invalid or expired session!")

	# Update last activity because we're MAGIC
	session.last_activity = datetime.utcnow()
	db.session.commit()

	return session.user

##########################
# Utility function to    #
# delete a session       #
##########################
def delete_session(session):
	session = models.Session.query.filter(models.Session.session == session).first()

	if not session:
		return

	db.session.delete(session)
	db.session.commit()

##########################
# Clear out all sessions #
# every 30 minutes that  #
# are 24 hours old       #
##########################
@scheduler.scheduled_job('cron', id='cleanup_sessions', second=0, minute=30)
def cleanup_sessions():
	print "[CRON] Cleaning up sessions..."
	try:
		ago = datetime.utcnow() - timedelta(hours=24)

		num = models.Session.query.filter(models.Session.time < ago).delete()
		db.session.commit()

		print "[CRON] Cleaned up %d old sessions" % (num)
	except Exception as e:
		print e
		db.session.rollback()

		print "[CRON] Failure - rollback triggered"

# Grab all the views
from app.views.main import *

# v1 Admin
from app.views.admin_v1 import admin_v1
app.register_blueprint(admin_v1, url_prefix='/admin/v1')

# v1 API
from app.views.api_v1 import api_v1
app.register_blueprint(api_v1, url_prefix='/api/v1')