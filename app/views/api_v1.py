from app import app, respond
from datetime import datetime

@app.route('/api/v1/ping')
def v1_ping():
	return respond("PONG", data={'now': datetime.utcnow()})

@app.route('/api/v1/getUser')
def v1_getuser():
	return respond("SUCCESS", data={'uid': 1, 'username': 'sysop', 'session_id': 'abc123'})

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
	return respond("SUCCESS", data={
		'activities': [
			{
				'id': 1,
				'name': 'Sample Name',
				'start': 1476921600,
				'end': 1476923400,
				'points': 500
			},
			{
				'id': 2,
				'name': 'Sample Name 2',
				'start': 1477008000,
				'end': 1477009800,
				'points': 100
			},
			{
				'id': 3,
				'name': 'Sample Name 3',
				'start': 1477094400,
				'end': 1477096200,
				'points': 1000
			},
		]
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