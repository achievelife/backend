import os
import thread
import sys

from flask import Flask
from flask_jsonpify import jsonify
#from flask.ext.sqlalchemy import SQLAlchemy
#from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
#app.config.from_object('config')

# Setup extensions
#bcrypt = Bcrypt(app)
#db = SQLAlchemy(app)

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

# Grab all the views
from app.views.main import *
from app.views.api_v1 import *