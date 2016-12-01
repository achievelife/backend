from app import app
from app.models import User, Session, Score
from app.utils import respond, check_params
from datetime import datetime
from flask import Blueprint, request
import time

admin_v1 = Blueprint('admin_v1', __name__)

@admin_v1.route('/getUsers', methods=['POST'])
def v1_admin_getUsers():
	try:
		check_params(request, ['key'])

		if request.form['key'] != app.config['ADMIN_SECRET_KEY']:
			raise StandardError('Bad. Go away.')
	except StandardError as e:
		return respond(str(e), code=400), 400

	users = []
	for u in User.query.all():
		users.append({
			'id': u.id,
			'username': u.username
		})

	return respond("SUCCESS", data={'users': users, 'count': len(users)})

@admin_v1.route('/getUser', methods=['POST'])
def v1_admin_getUser():
	try:
		check_params(request, ['key', 'uid'])

		if request.form['key'] != app.config['ADMIN_SECRET_KEY']:
			raise StandardError('Bad. Go away.')

		uid = request.form['uid']
	except StandardError as e:
		return respond(str(e), code=400), 400

	user = User.query.filter(User.id == uid).first()

	if not user:
		return respond("Unknown user", code=404)

	return respond("SUCCESS", data={'user': user.getDict()})

@admin_v1.route('/getUserActivityHistory', methods=['POST'])
def v1_admin_getUserActivityHistory():
	try:
		check_params(request, ['key', 'uid'])
		
		if request.form['key'] != app.config['ADMIN_SECRET_KEY']:
			raise StandardError('Bad. Go away.')

		uid = request.form['uid']
	except StandardError as e:
		return respond(str(e), code=400), 400

	user = User.query.filter(User.id == uid).first()

	if not user:
		return respond("Unknown user", code=404)

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

@admin_v1.route('/getAllSessions', methods=['POST'])
def v1_admin_getAllSessions():
	try:
		check_params(request, ['key'])

		if request.form['key'] != app.config['ADMIN_SECRET_KEY']:
			raise StandardError('Bad. Go away.')

	except StandardError as e:
		return respond(str(e), code=400), 400

	sessions = []

	for s in Session.query.all():
		sessions.append({
			#do nothing for now
			})

	return respond("SUCCESS", data={'sessions': user.getDict()})

@admin_v1.route('/banUser', methods=['POST'])
def v1_admin_banUser():
	try:
		check_params(request, ['key', 'uid'])

		if request.form['key'] != app.config['ADMIN_SECRET_KEY']:
			raise StandardError('Bad. Go away.')

		uid = request.form['uid']
	except StandardError as e:
		return respond(str(e), code=400), 400

	user = User.query.filter(User.id == uid).first()

	if not user:
		return respond("Unknown user", code=404)

	#banUser

	return respond("SUCCESS")