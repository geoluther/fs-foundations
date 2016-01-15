# puppy queries


"""
1. Query all of the puppies and return the results in ascending alphabetical order

2. Query all of the puppies that are less than 6 months old organized by the youngest first

3. Query all puppies by ascending weight

4. Query all puppies grouped by the shelter in which they are staying
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from puppies import Base, Shelter, Puppy, Profile
#from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
import datetime
import random

engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def CreateRandomAge():
	today = datetime.date.today()
	days_old = randint(0,540)
	birthday = today - datetime.timedelta(days = days_old)
	return birthday

#This method will create a random weight between 1.0-40.0 pounds (or whatever unit of measure you prefer)
def CreateRandomWeight():
	return random.uniform(1.0, 40.0)


def queryAll():
	"""1. Query all of the puppies and return the
	results in ascending alphabetical order
	"""
	names = session.query(Puppy).order_by(Puppy.name).all()

	# for name in names:
	# 	print name.name
	print "running query 1"
	return names


def lessThanSixMo():
	"""2. Query all of the puppies that are less than
	6 months old organized by the youngest first
	"""

	# calculatie 6 months
	today = datetime.date.today()
	sixmonths = datetime.timedelta(weeks = 26)
	cutoff = today - sixmonths

	result = session.query(Puppy).filter(Puppy.dateOfBirth > cutoff).order_by(Puppy.dateOfBirth.desc()).all()

	print "running query 2"
	return result


def puppiesByWeight():
	"""3. Query all puppies by ascending weight"""
	pups = session.query(Puppy).order_by(Puppy.weight).all()
	print "running query 3"
	return pups


def pupsGroupByShelter():
	"""4. Query all puppies grouped by the shelter
	in which they are staying
	"""
	pups = session.query(Puppy).order_by(Puppy.shelter_id).all()
	print "running query 4"
	return pups

def add_puppy(puppy_name, shelterid):
	# puppy: must be
	shelter = session.query(Shelter).filter_by(id=shelterid).first()
	print "tyring to add to '%s' " % (shelter.name)
	print "current_occupancy: ", shelter.current_occupancy
	print "maximum_capacity: ", shelter.maximum_capacity

	# if shelter has capacity, add puppy
	if shelter.current_occupancy < shelter.maximum_capacity:
		new_puppy = Puppy(name = puppy_name, gender = "male", dateOfBirth = CreateRandomAge(),picture="http://foo.com", shelter_id=shelterid, weight= CreateRandomWeight())
		session.add(new_puppy)
		shelter.current_occupancy = shelter.current_occupancy + 1
		session.commit()
		print "puppy named '%s' added" % (puppy_name)
	else:
		print "sorry, the '%s' is full, try a different one" % (shelter.name)



if __name__ == '__main__':
	# puppies = queryAll()
	# lessThanSixMo()
	# puppiesByWeight()
	# pupsGroupByShelter()
	add_puppy("fluffy", 3)


