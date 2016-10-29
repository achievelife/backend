from app import db
from datetime import datetime
from json import dumps
from math import sqrt

class Activity(db.Model):
	__tablename__ = 'activities'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255))
	points = db.Column(db.Integer)
	required_xp = db.Column(db.Integer)

	""" Link to the skill table """
	skillID = db.Column(db.Integer, db.ForeignKey('skills.id'))
	skill = db.relationship('Skill', 
		backref=db.backref('activities', lazy='dynamic'))

	def __init__(self, name, skill, points, required_xp=0):
		self.name = name
		self.skill = skill
		self.points = points
		self.required_xp = required_xp

class Skill(db.Model):
	__tablename__ = 'skills'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255))

	def __init__(self, name):
		self.name = name

class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(255), unique=True)
	password = db.Column(db.String(255))
	create_date = db.Column(db.DateTime)

	def __init__(self, username, password, created=datetime.utcnow()):
		self.username = username
		self.password = password
		self.create_date = created

	def getSkillPoints(self):
		# This is literally fire
		query = "SELECT skills.name, SUM(points) AS points " \
				"FROM users " \
				"LEFT JOIN scores ON scores.userID = users.id " \
				"LEFT JOIN activities ON activities.id = scores.activityID " \
				"LEFT JOIN skills ON skills.id = activities.skillID " \
				"WHERE users.id = {} " \
				"GROUP BY skills.id".format(self.id)

		result = db.engine.execute(query)
		skills = {}

		for res in result.fetchall():
			(name, points) = res
			skills[name] = points

		return skills

	def getDict(self):
		return_user = {
			'id': self.id,
			'username': self.username,
		}

		xp = 0
		for (skill, points) in self.getSkillPoints().iteritems():
			return_user[skill.lower()] = points
			xp += points

		return_user['xp'] = xp
		return_user['level'] = self.xp2level(xp)

		return return_user

	def xp2level(self, xp, whole=True):
		level = (0.04 * sqrt(xp))

		return (int(round(level)) if whole else level)

class Location(db.Model):
	__tablename__ = 'locations'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255))
	lat = db.Column(db.Float)
	lng = db.Column(db.Float)

	def __init__(self, name, lat, lng):
		self.name = name
		self.lat = lat
		self.lng = lng

class Score(db.Model):
	__tablename__ = 'scores'

	id = db.Column(db.Integer, primary_key=True)
	start = db.Column(db.DateTime)
	end = db.Column(db.DateTime)

	""" Link to the account table """
	activityID = db.Column(db.Integer, db.ForeignKey('activities.id'))
	activity = db.relationship('Activity', 
		backref=db.backref('scores', lazy='dynamic')) #foreign_keys=[activityID])

	""" Link to the user table """
	userID = db.Column(db.Integer, db.ForeignKey('users.id'))
	user = db.relationship('User', 
		backref=db.backref('scores', lazy='dynamic')) #foreign_keys=[activityID])

	def __init__(self, user, activity, start=datetime.utcnow(), end=datetime.utcnow()):
		self.user = user
		self.activity = activity
		self.start = start
		self.end = end

class Session(db.Model):
	__tablename__ = 'sessions'

	id = db.Column(db.Integer, primary_key=True)

	""" Allow a user to have many sessions """
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	user = db.relationship('User', 
		backref=db.backref('sessions', lazy='dynamic'))

	session = db.Column(db.String(100), unique=True)
	time = db.Column(db.DateTime)
	last_activity = db.Column(db.DateTime)

	def __init__(self, session, user):
		self.session = session
		self.user = user
		self.time = datetime.utcnow()
		self.last_activity = datetime.utcnow()