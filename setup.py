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

	# Add Skills
	skills = [
		Skill("Intelligence"),
		Skill("Fitness"),
		Skill("Finance")
	]

	# Add Locations
	locations = [
		Location("UB Capen", 42.9994428, -78.7816213),
		Location("UB Student Union", 43.001161, -78.7884119),
	]

	for l in locations:
		db.session.add(l)

	# Add activities
	activities = []
	xp_vals = [x * 250 for x in xrange(7)]
	for i in xrange(6):
		for skill in skills:
			activities.append(Activity("Sample #{}".format(len(activities)+1), "TODO", skill, random.choice(locations), random.choice(xp_vals)))

	for a in activities:
		print("Created activity {} ({})".format(a.name, a.skill.name))
		db.session.add(a)

	print("\n")

	# Create ~20 users
	for i in xrange(20):
		hashpw = bcrypt.generate_password_hash("changeme")
		user = User("user{}".format(i+1), hashpw)
		db.session.add(user)

		print("User: {}".format(user.username))

		for a in activities:
			if bool(random.getrandbits(1)):
				print("Completed Activity: {} ({})".format(a.name, a.skill.name))
				db.session.add(Score(user, a))

		db.session.commit()

		print("\n")
except Exception as e:
	print("Error: %s" % (e))
