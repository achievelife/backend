#!/usr/bin/env python
from __future__ import print_function
import random

from app import bcrypt, db
from app.models import *

try:
	# Initalize DB
	db.drop_all()
	db.create_all()

	print("AchieveLife\n")

	# Add activities
	activities = [
		Activity("Sample #1", 500),
		Activity("Sample #2", 1000),
		Activity("Sample #3", 1500),
		Activity("Sample #4", 250),
		Activity("Sample #5", 750),
		Activity("Sample #6", 500),
		Activity("Sample #7", 1000),
		Activity("Sample #8", 500),
		Activity("Sample #9", 1250),
		Activity("Sample #10", 500)
	]

	for a in activities:
		db.session.add(a)

	# Create ~20 users
	for i in xrange(20):
		hashpw = bcrypt.generate_password_hash("changeme")
		user = User("user{}".format(i), hashpw)
		db.session.add(user)

		print("User: {}".format(user.username))

		for a in activities:
			if bool(random.getrandbits(1)):
				print("Completed Activity: {}".format(a.name))
				db.session.add(Score(user, a))

		db.session.commit()

		print("\n")
except Exception as e:
	print("Error: %s" % (e))
