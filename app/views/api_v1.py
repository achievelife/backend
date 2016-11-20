from app import bcrypt, db
from app.models import User, Score, Session, Location, Activity
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

@api_v1.route('/checkin', methods=['POST'])
def v1_checkin():
	try:
		check_params(request, ['session', 'lat', 'lng'])
		user = validate_session(request.form['session'])
	except StandardError as e:
		return respond(str(e), code=400), 400

	user.lat = request.form['lat']
	user.lng = request.form['lng']
	db.session.commit()

	return respond("SUCCESS")

@api_v1.route('/nearby', methods=['POST'])
def v1_nearby():
	try:
		check_params(request, ['session'])
		user = validate_session(request.form['session'])
	except StandardError as e:
		return respond(str(e), code=400), 400

	return respond("SUCCESS", data={'nearby': [{}]})

@api_v1.route('/location', methods=['POST'])
def v1_location():
	try:
		check_params(request, ['session', 'id'])
		user = validate_session(request.form['session'])
	except StandardError as e:
		return respond(str(e), code=400), 400

	location = Location.query.filter(Location.id == request.form['id']).first()
	if location == None:
		return respond("Unknown location", code=103), 500

	loc = {
		'name': location.name,
		'lat': location.lat,
		'lng': location.lng,
	}

	activities = Activity.query.filter(Activity.location == location).all()
	acts = []
	for a in activities:
		acts.append({
			'name': a.name,
			'desc': a.desc,
			'points': a.points
		})

	return respond("SUCCESS", data={'location': loc, 'activities': acts})

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
			'skill': score.activity.skill.name,
			'completed': score.completed
		})

	return respond("SUCCESS", data={
		'activities': activities
	})

@api_v1.route('/activity/complete', methods=['POST'])
def v1_activity_complete():
	try:
		check_params(request, ['session', 'id'])
		user = validate_session(request.form['session'])
	except StandardError as e:
		return respond(str(e), code=400), 400

	score = Score.query.filter(Score.id == request.form['id']).first()
	if score == None:
		return respond("Unknown score", code=104), 400

	if score.user.id != user.id:
		return respond("Stop haxing", code=999), 400

	if score.completed:
		return respond("Activity already completed!", code=105), 400

	score.end = datetime.utcnow()
	score.completed = True
	db.session.commit()

	return respond("Completed!", data={'xp_gained': score.activity.points})

@api_v1.route('/activity/start', methods=['POST'])
def v1_activity_start():
	try:
		check_params(request, ['session', 'id'])
		user = validate_session(request.form['session'])
	except StandardError as e:
		return respond(str(e), code=400), 400

	activity = Activity.query.filter(Activity.id == request.form['id']).first()
	if activity == None:
		return respond("Unknown activity", code=105), 400

	score = Score(user, activity)

	db.session.add(score)
	db.session.commit()

	return respond("Completed!", data={'id': score.id})

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