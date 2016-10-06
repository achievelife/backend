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

@app.route('/api/v1/login', methods=['POST'])
def v1_login():
	return respond("TODO")

@app.route('/api/v1/logout', methods=['POST'])
def v1_logout():
	return respond("TODO")