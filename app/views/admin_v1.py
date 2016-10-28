from app import app, respond
from app.models import User
from datetime import datetime
import time

@app.route('/api/v1/admin/getUsers')
def v1_admin_getUsers():
	users = []
	for u in User.query.all():
		users.append({
			'id': u.id,
			'username': u.username
		})

	return respond("SUCCESS", data={'users': users, 'count': len(users)})

@app.route('/api/v1/admin/getUser/<uid>')
def v1_admin_getUser(uid):
	user = User.query.filter(User.id == uid).first()

	if not user:
		return respond("Unknown user", code=404)

	return respond("SUCCESS", data={'user': {
		'id': user.id,
		'username': user.username,
		'xp': -1,
		'level': -1,
		'intelligence': -1,
		'fitness': -1,
		'finance': -1,
	}})