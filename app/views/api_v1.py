from app import app, respond
from datetime import datetime

@app.route('/api/v1/ping')
def v1_ping():
	return respond("PONG", data={'now': datetime.utcnow()})
