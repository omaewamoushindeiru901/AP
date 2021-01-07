from sqlalchemy.orm import sessionmaker
from project import engine

Session = sessionmaker(bind=engine)
session = Session()


session.close()
