from app import app, respond, check_params
from app.models import User
from datetime import datetime
from flask import request
import time

ADMIN_SECRET_KEY="4F7F9C7078837F0EB296AF9E2AE4EFAE1C3F8F355D2CFD495C9F950A7227F1F1"

@app.route('/api/v1/admin/getUsers', methods=['POST'])
def v1_admin_getUsers():
	try:
		check_params(request, ['key'])

		if request.form['key'] != ADMIN_SECRET_KEY:
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

@app.route('/api/v1/admin/getUser', methods=['POST'])
def v1_admin_getUser():
	try:
		check_params(request, ['key', 'uid'])

		if request.form['key'] != ADMIN_SECRET_KEY:
			raise StandardError('Bad. Go away.')

		uid = request.form['uid']
	except StandardError as e:
		return respond(str(e), code=400), 400

	user = User.query.filter(User.id == uid).first()

	if not user:
		return respond("Unknown user", code=404)

	return_user = {
		'id': user.id,
		'username': user.username,
		'level': -1,
	}

	xp = 0
	for (skill, points) in user.getSkillPoints().iteritems():
		return_user[skill.lower()] = points
		xp += points

	return_user['xp'] = xp

	return respond("SUCCESS", data={'user': return_user})