from flask import Flask
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
api=Api(app)
bcrypt = Bcrypt(app)
auth = HTTPBasicAuth()


engine = create_engine('sqlite:///database.db', echo=True,connect_args={'check_same_thread': False})
Session = sessionmaker(bind=engine)
Session = scoped_session(Session)
