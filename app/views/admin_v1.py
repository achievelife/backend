from app import app
from app.models import User
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