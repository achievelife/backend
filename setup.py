#!/usr/bin/env python
from __future__ import print_function
import random

from faker import Faker

from app import bcrypt, db
from app.models import *

try:
	# Faker pls
	fake = Faker()

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
	locations = [Location(fake.street_name(), fake.latitude(), fake.longitude()) for x in xrange(8)]
	locations.append(Location("UB Capen", 42.9994428, -78.7816213))
	locations.append(Location("UB Student Union", 43.001161, -78.7884119))

	for l in locations:
		print("Created location {} ({} / {})".format(l.name, l.lat, l.lng))
		db.session.add(l)

	print("\n")

	# Add activities
	activities = []
	xp_vals = [x * 250 for x in xrange(1, 7)]
	for i in xrange(6):
		for skill in skills:
			activities.append(Activity("Sample #{}".format(len(activities)+1), fake.text(), skill, random.choice(locations), random.choice(xp_vals)))

	for a in activities:
		print("Created activity {} ({})".format(a.name, a.skill.name))
		db.session.add(a)

	print("\n")

	# Create ~20 users
	for i in xrange(20):
		hashpw = bcrypt.generate_password_hash("changeme")
		user = User(fake.user_name(), hashpw, lat=fake.latitude(), lng=fake.longitude())
		db.session.add(user)

		print("User: {}".format(user.username))

		for a in activities:
			if fake.boolean(chance_of_getting_true=30):
				print("Completed Activity: {} ({})".format(a.name, a.skill.name))
				db.session.add(Score(user, a, completed=True))

		db.session.commit()

		print("\n")
except Exception as e:
	print("Error: %s" % (e))
