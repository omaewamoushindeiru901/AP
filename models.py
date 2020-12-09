from sqlalchemy import create_engine, Column, Integer, String, join
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column('id', Integer, unique=True)
    username = Column('username', String, primary_key=True)
    firstName = Column('firstName', String)
    lastName = Column('lastName', String)
    email = Column('email', String)
    password = Column('password', String)
    phone = Column('phone', String)


class Event(Base):
    __tablename__ = "event"
    creatorId = Column('creatorid', Integer, primary_key=True)
    #usersId = Column('usersid', Integer)
    eventid = Column('eventid', Integer)
    name = Column('name', String)
    content = Column('content', String)
    tags = Column('tags', String)
    date = Column('date', String)



class Connected_users(Base):
    __tablename__ = "connected_users"
    eventId = Column('eventid', Integer, primary_key=True, foreign_key='event.eventid')
    usersid = Column('usersid', Integer, autoincrement=True, foreign_key='user.id')


engine = create_engine('sqlite:///database.db', echo=True)
Base.metadata.create_all(bind=engine)
