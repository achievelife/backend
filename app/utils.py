from app import db, models
from datetime import datetime
from flask_jsonpify import jsonify

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
	"""
	Ok, for sprint 3 we're not going to actually validate sessions.  It'll
	always be good for the first user (user1).  THIS WILL BE REMOVED BY SPRINT 4
	"""
	return models.User.query.filter(models.User.id == 1).first()

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