# database_setup.py

import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Shelter(Base):
	__tablename__ = 'shelter'

	name = Column(
		String(80), nullable=False)

	id = Column(Integer, primary_key=True)

	address = Column(String(100), nullable=False)
	city = Column(String(100), nullable=False)
	state = Column(String(100), nullable=False)
	zipcode = Column(Integer, nullable=False)
	website = Column(String(100), nullable=False)


class Puppy(Base):
	__tablename__ = 'puppy'

	id = Column(Integer,primary_key=True)
	name = Column(String(80),nullable=False)
	dateofbirth = Column(Date, nullable=False)
	gender = Column(String(10), nullable=False)
	weight = Column(Numeric, nullable=False)
	shelter_id = Column(Integer, ForeignKey('shelter.id'))
	shelter = relationship(Shelter)


### insert at end of file ##

engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.create_all(engine)



# for python cmd
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session  = DBSession()
# add an item
myFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFirstRestaurant)
session.commit()
'''


