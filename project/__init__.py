from flask import Flask
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

engine = create_engine('sqlite:///database.db', echo=True,connect_args={'check_same_thread': False})
Session = sessionmaker(bind=engine)
Session = scoped_session(Session)
