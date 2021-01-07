from sqlalchemy import Column, Integer, String, Table, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from flask_bcrypt import generate_password_hash, check_password_hash
from project import *

Base = declarative_base()


def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')


class tag_to_event(Base):
    __tablename__ = 'tag_to_event'
    eventid = Column('eventid', ForeignKey('event.eventid'), primary_key=True)
    tag = Column('tag', ForeignKey('tags.tag'), primary_key=True)


class event_to_user(Base):
    __tablename__ = 'event_to_user'
    eventid = Column('eventid', ForeignKey('event.eventid'), primary_key=True)
    usersid = Column('usersid', ForeignKey('user.id'), primary_key=True)


class User(Base):
    __tablename__ = "user"
    id = Column('id', Integer, unique=True, autoincrement=True)
    username = Column('username', String, primary_key=True)
    firstName = Column('firstName', String)
    lastName = Column('lastName', String)
    email = Column('email', String)
    password = Column('password', String)
    phone = Column('phone', String)


class Event(Base):
    __tablename__ = "event"
    creatorid = Column('creatorid', Integer)
    eventid = Column('eventid', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(50))
    content = Column('content', String)
    date = Column('date', String)


class Tags(Base):
    __tablename__ = 'tags'
    eventid = Column('eventid', Integer, primary_key=True)
    tag = Column('tag', String)
