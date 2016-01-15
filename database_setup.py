# database_setup.py

import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Restaurant(Base):
	__tablename__ = 'restaurant'

	name = Column(
		String(80), nullable=False)

	id = Column(
		Integer, primary_key=True)


class MenuItem(Base):
	__tablename__ = 'menu_item'

	name = Column(String(80),
		nullable=False)

	id = Column(Integer,
		primary_key=True)

	course = Column(String(250))
	description = Column(String(250))
	price = Column(String(8))
	restaurant_id = Column(Integer,
		ForeignKey('restaurant.id'))

	restaurant = relationship(Restaurant)




### insert at end of file ##

engine = create_engine('sqlite:///restaurantmenu.db')

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


