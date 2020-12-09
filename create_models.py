from sqlalchemy import null
from sqlalchemy.orm import sessionmaker

from models import *

Session = sessionmaker(bind=engine)
session = Session()

user = User(id=8, username="Nanii", firstName="Omaewamou", lastName="Shindeiru", email="animeeee@gmail.com",
            password="pucpucpuc", phone="+380500783234")
user1 = User(id=0, username="Naruto77", firstName="Naruto", lastName="Uzumaki", email="hokage@gmail.com",
             password="q1w2e3r4t5y6", phone="+380665039186")
user2 = User(id=10, username="qwewetrt", firstName="oooo", lastName="arara", email="hokage@gmail.com",
             password="q1w2e3r4t5y6", phone="+380665039186")

event = Event(creatorId=user.id, eventid=3333, name="Meeting",
              content="Project meeting", tags="vazhno", date="09.12.2020")

event1 = Event(creatorId=user.id, eventid=7777, name="Go to the market",
               content="buy everything for cake",
               tags="", date="09.12.2020")
event2 = Event(creatorId=user2.id, eventid=6666, name="Meeting",
               content="Project meeting", tags="vazhno", date="09.12.2020")
connected_users1 = Connected_users(usersid=user.id, eventId=event2.eventid)
connected_users2 = Connected_users(usersid=user2.id, eventId=event1.eventid)

session.add(user)
session.add(user1)
session.add(user2)
session.add(event)
session.add(event1)
session.add(event2)
session.add(connected_users1)
session.add(connected_users2)
session.commit()

session.close()
