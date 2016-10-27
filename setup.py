#!/usr/bin/env python
from app import bcrypt, db
from app.models import *

try:
	# Initalize DB
	db.drop_all()
	db.create_all()

	# Create the first user
	hashpw = bcrypt.generate_password_hash("admin")
	user = User("admin", hashpw)

	# Add an activity
	a1 = Activity("Sample #1", 500)
	a2 = Activity("Sample #2", 100)
	a3 = Activity("Sample #3", 1000)

	# Add some completed
	s1 = Score(user, a1)
	s2 = Score(user, a2)
	s3 = Score(user, a3)

	db.session.add(user)

	db.session.add(a1)
	db.session.add(a2)
	db.session.add(a3)

	db.session.add(s1)
	db.session.add(s2)
	db.session.add(s3)

	db.session.commit()

	print "AchieveLife\n"
	print "Username: admin\nPassword: admin\n"
except Exception as e:
	print "Error: %s" % (e)
