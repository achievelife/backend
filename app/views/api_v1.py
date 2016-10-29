from app import bcrypt, db
from app.models import User, Score, Session
from app.utils import check_params, respond, validate_session, delete_session
from binascii import hexlify
from datetime import datetime
from flask import Blueprint, request
from os import urandom
import time

api_v1 = Blueprint('api_v1', __name__)

@api_v1.route('/ping', methods=['POST'])
def v1_ping():
	try:
		check_params(request, ['session'])
		user = validate_session(request.form['session'])
	except StandardError as e:
		return respond(str(e), code=400), 400

	return respond("PONG", data={'now': datetime.utcnow()})

@api_v1.route('/getUser', methods=['POST'])
def v1_getuser():
	try:
		check_params(request, ['session'])
		user = validate_session(request.form['session'])
	except StandardError as e:
		return respond(str(e), code=400), 400

	return respond("SUCCESS", data={'user': user.getDict()})

@api_v1.route('/friends', methods=['POST'])
def v1_friends():
	try:
		check_params(request, ['session'])
		user = validate_session(request.form['session'])
	except StandardError as e:
		return respond(str(e), code=400), 400

	return respond("SUCCESS", data={'friends': []})

@api_v1.route('/nearby', methods=['POST'])
def v1_nearby():
	try:
		check_params(request, ['session'])
		user = validate_session(request.form['session'])
	except StandardError as e:
		return respond(str(e), code=400), 400

	return respond("SUCCESS", data={'nearby': [{}]})

@api_v1.route('/activity/history', methods=['POST'])
def v1_activity_history():
	try:
		check_params(request, ['session'])
		user = validate_session(request.form['session'])
	except StandardError as e:
		return respond(str(e), code=400), 400

	scores = Score.query.filter(Score.user == user).all()
	activities = []

	for score in scores:
		activities.append({
			'id': score.id,
			'name': score.activity.name,
			'start': time.mktime(score.start.timetuple()),
			'end': time.mktime(score.end.timetuple()),
			'points': score.activity.points,
			'skill': score.activity.skill.name
		})

	return respond("SUCCESS", data={
		'activities': activities
	})

@api_v1.route('/activity/complete', methods=['POST'])
def v1_activity_complete():
	try:
		check_params(request, ['session'])
		user = validate_session(request.form['session'])
	except StandardError as e:
		return respond(str(e), code=400), 400

	return respond("TODO")

@api_v1.route('/activity/start', methods=['POST'])
def v1_activity_start():
	try:
		check_params(request, ['session'])
		user = validate_session(request.form['session'])
	except StandardError as e:
		return respond(str(e), code=400), 400

	return respond("TODO")

@api_v1.route('/activity/end', methods=['POST'])
def v1_activity_end():
	try:
		check_params(request, ['session'])
		user = validate_session(request.form['session'])
	except StandardError as e:
		return respond(str(e), code=400), 400

	return respond("TODO")

@api_v1.route('/login', methods=['POST'])
def v1_login():
	try:
		check_params(request, ['user', 'pass'])
	except StandardError as e:
		return respond(str(e), code=400), 400

	username = str(request.form['user'])
	password = str(request.form['pass'])

	user = User.query.filter(User.username == username).first()
	if user == None or not bcrypt.check_password_hash(user.password, password):
		return respond("Unknown or invalid username/password", code=400), 400

	# Create a session
	session = Session(hexlify(urandom(50)), user)
	try:
		db.session.add(session)
		db.session.commit()
	except:
		db.session.rollback()
		return respond("Internal server error has occured", code=101), 500

	return respond("SUCCESS", data={'session': session.session})

@api_v1.route('/logout', methods=['POST'])
def v1_logout():
	try:
		check_params(request, ['session'])
		user = validate_session(request.form['session'])
	except StandardError as e:
		return respond(str(e), code=400), 400

	delete_session(request.form['session'])

	return respond("SUCCESS")