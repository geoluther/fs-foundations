from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

association_table = Table('association', Base.metadata,
    Column('puppy', Integer, ForeignKey('puppy.id')),
    Column('adoptor', Integer, ForeignKey('adoptor.id'))
)


class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key = True)
    name =Column(String(80), nullable = False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)
    current_occupancy = Column(Integer, default=0)
    maximum_capacity = Column(Integer, default=50)

    def __repr__(self):
        return ( "<User(name='%s', current_occupancy='%s', maximum_capacity='%s')>" %
            (self.name, self.current_occupancy, self.maximum_capacity) )

class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(String(6), nullable = False)
    dateOfBirth = Column(Date)
    picture = Column(String)
    weight = Column(Numeric(10))

    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)

    # profile_id = Column(Integer, ForeignKey('profile.id'))
    profile = relationship("Profile", uselist=False, back_populates="puppy")

    adoptor = relationship(
        "Adoptor",
        secondary=association_table,
        backref="puppy")

    def __repr__(self):
        return "<User(name='%s', gender='%s', shelter='%s', dateOfBirth='%s')>" % (
            self.name, self.gender, self.shelter.name, self.dateOfBirth)


class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    description = Column(String)
    special_needs = Column(String)

    puppy_id = Column(Integer, ForeignKey('puppy.id'))
    puppy = relationship("Puppy", back_populates="profile")


class Adoptor(Base):
    __tablename__ = 'adoptor'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable = False)


engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.create_all(engine)