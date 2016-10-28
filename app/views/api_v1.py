from app import app, respond
from app.models import User, Score
from datetime import datetime
import time

@app.route('/api/v1/ping')
def v1_ping():
	return respond("PONG", data={'now': datetime.utcnow()})

@app.route('/api/v1/getUser')
def v1_getuser():
	user = User.query.filter(User.username == "user1").first()

	return respond("SUCCESS", data={'uid': user.id, 'username': user.username, 'session_id': 'TODO'})

@app.route('/api/v1/friends')
def v1_friends():
	return respond("SUCCESS", data={'friends': [{'uid': 2, 'username': 'dev1'}]})

@app.route('/api/v1/checkin', methods=['POST'])
def v1_checkin():
	return respond("TODO")

@app.route('/api/v1/nearby')
def v1_nearby():
	return respond("SUCCESS", data={'nearby': [{}]})

@app.route('/api/v1/activity/history')
def v1_activity_history():
	user = User.query.filter(User.username == "user1").first()
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

@app.route('/api/v1/activity/complete', methods=['POST'])
def v1_activity_complete():
	return respond("TODO")

@app.route('/api/v1/activity/start', methods=['POST'])
def v1_activity_start():
	return respond("TODO")

@app.route('/api/v1/activity/end', methods=['POST'])
def v1_activity_end():
	return respond("TODO")

@app.route('/api/v1/login', methods=['POST'])
def v1_login():
	return respond("TODO")

@app.route('/api/v1/logout', methods=['POST'])
def v1_logout():
	return respond("TODO")