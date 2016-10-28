import os
import thread
import sys

from flask import Flask
from flask_jsonpify import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///achievelife.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

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

# Grab all the views
from app.views.main import *
from app.views.api_v1 import *
from app.views.admin_v1 import *