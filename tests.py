from sqlalchemy.util import b64encode
from models import Base
from main import *
from flask_testing import TestCase

engine = create_engine('sqlite:///database.db', echo=True, connect_args={'check_same_thread': False})
Session = sessionmaker(bind=engine)
Base.metadata.bind = engine


class Tests(TestCase):
    app.config['TESTING'] = True
    app.config['LIVESERVER_PORT'] = 5000

    def create_app(self):
        return app

    def setUp(self):
        session = Session()
        Base.metadata.drop_all()
        Base.metadata.create_all()
        user = User(id=0, username="Nanii", firstName="Omaewamou", lastName="Shindeiru", email="animeeee@gmail.com",
                    password="$2b$12$JocZlwrAvWHczuyydKjUjeTuYkuPmRJfKE3llexSEkha7c1v5ofVq", phone="+380500783234")
        user1 = User(id=1, username="Naruto77", firstName="Naruto", lastName="Uzumaki", email="hokage@gmail.com",
                     password="$2b$12$JocZlwrAvWHczuyydKjUjeTuYkuPmRJfKE3llexSEkha7c1v5ofVq", phone="+380665039186")
        user2 = User(id=2, username="qwewetrt", firstName="oooo", lastName="arara", email="hokage@gmail.com",
                     password="q1w2e3r4t5y6", phone="+380665039186")
        event = Event(creatorid=user.id, eventid=0, name="Meeting",
                      content="Project meeting", date="09.12.2020")
        event1 = Event(creatorid=user.id, eventid=1, name="Go to the market",
                       content="buy everything for cake", date="09.12.2020")
        event2 = Event(creatorid=user2.id, eventid=2, name="Meeting2",
                       content="Project meeting2", date="09.12.2020")
        connected1 = event_to_user(eventid=0, usersid=2)
        connected2 = event_to_user(eventid=2, usersid=0)

        tag1 = tag_to_event(eventid=0, tag="vazhno")
        tag2 = tag_to_event(eventid=2, tag="pf")

        session.add(user)
        session.add(user1)
        session.add(user2)
        session.add(event)
        session.add(event1)
        session.add(event2)
        session.add(connected1)
        session.add(connected2)
        session.add(tag1)
        session.add(tag2)
        session.commit()


class Tests_Controller(Tests):
    def test_getallusers(self):
        res = self.client.get("/user")
        assert res.status_code == 200

    def test_postuser(self):
        res = self.client.post("/user",
                               data={"id": 4, "username": "Nika", "firstName": "Nicole", "lastName": "Kazionnikova",
                                     "email": "nika777@gmail.com", "password": "1234", "phone": "+380665039186"})
        print(res.data)
        self.assertEqual(201, res.status_code)

    def test_putuser(self):
        credentials = b64encode(b"Nanii:1234")
        res = self.client.put("/user", headers={"Authorization": f"Basic {credentials}"},
                              data={"username": "Nanii777"})
        print(res.data)
        assert res.status_code == 200

    def test_getuserbyid(self):
        credentials = b64encode(b"Nanii:1234")
        res = self.client.get("/user/1", headers={"Authorization": f"Basic {credentials}"})
        assert res.status_code == 200

    def test_getuserbyidwrong(self):
        credentials = b64encode(b"Nanii:1234")
        res = self.client.get("/user/100", headers={"Authorization": f"Basic {credentials}"})
        assert res.status_code == 404

    def test_deleteuser(self):
        credentials = b64encode(b"Nanii:1234")
        res = self.client.delete("/user", headers={"Authorization": f"Basic {credentials}"})
        assert res.status_code == 200

    def test_deleteuserwrong(self):
        credentials = b64encode(b"Naniiii:1234")
        res = self.client.delete("/user", headers={"Authorization": f"Basic {credentials}"})
        assert res.status_code == 401

    def test_getallusersevents(self):
        credentials = b64encode(b"Nanii:1234")
        res = self.client.get("/event", headers={"Authorization": f"Basic {credentials}"})
        print(res.data)
        assert res.status_code == 200

    def test_geteventsnotusers(self):
        credentials = b64encode(b"Naniii:1234")
        res = self.client.get("/event", headers={"Authorization": f"Basic {credentials}"})
        print(res.data)
        assert res.status_code == 401

    def test_geteventswrong(self):
        credentials = b64encode(b"Naruto77:1234")
        res = self.client.get("/event", headers={"Authorization": f"Basic {credentials}"})
        print(res.data)
        assert res.status_code == 404

    def test_postevent(self):
        credentials = b64encode(b"Nanii:1234")
        res = self.client.post("/event", headers={"Authorization": f"Basic {credentials}"},
                               data={"content": "todo todo", "creatorid": 0, "date": "15.12.2021", "eventid": 0,
                                     "name": "Zakaz"})
        print(res.data)
        assert res.status_code == 200

    def test_posteventwrong(self):
        credentials = b64encode(b"Nanii:12345")
        res = self.client.post("/event", headers={"Authorization": f"Basic {credentials}"},
                               data={"content": "todo todo", "creatorid": 0, "date": "15.12.2021", "eventid": 0,
                                     "name": "Zakaz"})
        print(res.data)
        assert res.status_code == 401

    def test_geteventbyid(self):
        credentials = b64encode(b"Nanii:1234")
        res = self.client.get("/event/0", headers={"Authorization": f"Basic {credentials}"})
        print(res.data)
        assert res.status_code == 200

    def test_geteventbyidwrong(self):
        credentials = b64encode(b"Nanii:1234")
        res = self.client.get("/event/10", headers={"Authorization": f"Basic {credentials}"})
        print(res.data)
        assert res.status_code == 404

    def test_geteventbyidnotusers(self):
        credentials = b64encode(b"Nanii:1234")
        res = self.client.get("/event/2", headers={"Authorization": f"Basic {credentials}"})
        print(res.data)
        assert res.status_code == 401

    def test_deleteevent(self):
        credentials = b64encode(b"Nanii:1234")
        res = self.client.delete("/event/0", headers={"Authorization": f"Basic {credentials}"})
        print(res.status_code)
        assert res.status_code == 200

    def test_deleteeventwrong(self):
        credentials = b64encode(b"Nanii:1234")
        res = self.client.delete("/event/10", headers={"Authorization": f"Basic {credentials}"})
        print(res.status_code)
        assert res.status_code == 404

    def test_deleteeventnotusers(self):
        credentials = b64encode(b"Nanii:1234")
        res = self.client.delete("/event/2", headers={"Authorization": f"Basic {credentials}"})
        print(res.status_code)
        assert res.status_code == 401

    def test_putevent(self):
        credentials = b64encode(b"Nanii:1234")
        res = self.client.put("/event/0", headers={"Authorization": f"Basic {credentials}"},
                              data={"content": "asasasass"})
        print(res.data)
        assert res.status_code == 200

    def test_puteventwrong(self):
        credentials = b64encode(b"Nanii:1234")
        res = self.client.put("/event/100", headers={"Authorization": f"Basic {credentials}"},
                              data={"content": "asasasass"})
        print(res.data)
        assert res.status_code == 404

    def test_puteventnotusers(self):
        credentials = b64encode(b"Nanii:1234")
        res = self.client.put("/event/2", headers={"Authorization": f"Basic {credentials}"},
                              data={"content": "asasasass"})
        print(res.data)
        assert res.status_code == 401

    def test_getconnected(self):
        credentials = b64encode(b"Nanii:1234")
        res = self.client.get("/event/connected/0", headers={"Authorization": f"Basic {credentials}"})
        print(res.data)
        assert res.status_code == 200

    def test_getconnectedwrong(self):
        credentials = b64encode(b"Nanii:1234")
        res = self.client.get("/event/connected/10", headers={"Authorization": f"Basic {credentials}"})
        print(res.data)
        assert res.status_code == 404

    def test_postconnected(self):
        credentials = b64encode(b"Nanii:1234")
        res = self.client.post("/event/connected/0", headers={"Authorization": f"Basic {credentials}"},
                               data={"usersid": 1})
        print(res.data)
        assert res.status_code == 200

    def test_postconnectedwrong(self):
        credentials = b64encode(b"Nanii:qwerty")
        res = self.client.post("/event/connected/10", headers={"Authorization": f"Basic {credentials}"},
                               data={"usersid": 1})
        print(res.data)
        assert res.status_code == 401

    def test_deleteconnected(self):
        credentials = b64encode(b"Nanii:1234")
        res = self.client.delete("/event/connected/0/2", headers={"Authorization": f"Basic {credentials}"})
        print(res.status_code)
        assert res.status_code == 200

    def test_deleteconnectedwrong(self):
        credentials = b64encode(b"Nanii:1234")
        res = self.client.delete("/event/connected/0/10", headers={"Authorization": f"Basic {credentials}"})
        print(res.status_code)
        assert res.status_code == 404

    def test_deleteconnectedwrong(self):
        credentials = b64encode(b"Nanii:1234")
        res = self.client.delete("/event/connected/2/0", headers={"Authorization": f"Basic {credentials}"})
        print(res.status_code)
        assert res.status_code == 401

    def test_gettags(self):
        credentials = b64encode(b"Nanii:1234")
        res = self.client.get("/event/tags/0", headers={"Authorization": f"Basic {credentials}"})
        print(res.data)
        assert res.status_code == 200

    def test_gettagswrong(self):
        credentials = b64encode(b"Nanii:1234")
        res = self.client.get("/event/tags/10", headers={"Authorization": f"Basic {credentials}"})
        print(res.data)
        assert res.status_code == 404

    def test_posttag(self):
        credentials = b64encode(b"Nanii:1234")
        res = self.client.post("/event/tags/0", headers={"Authorization": f"Basic {credentials}"},
                               data={"tag": "pf"})
        print(res.data)
        assert res.status_code == 200

    def test_posttagwrong(self):
        credentials = b64encode(b"Nanii:qwerty")
        res = self.client.post("/event/tags/10", headers={"Authorization": f"Basic {credentials}"},
                               data={"tag": "pf"})
        print(res.data)
        assert res.status_code == 401

    def test_deletetag(self):
        credentials = b64encode(b"Nanii:1234")
        res = self.client.delete("/event/tags/0/vazhno", headers={"Authorization": f"Basic {credentials}"})
        print(res.status_code)
        assert res.status_code == 200

    def test_deletetagwrong(self):
        credentials = b64encode(b"Nanii:1234")
        res = self.client.delete("/event/tags/0/aaa", headers={"Authorization": f"Basic {credentials}"})
        print(res.status_code)
        assert res.status_code == 404

    def test_deletetagnotusers(self):
        credentials = b64encode(b"Nanii:1234")
        res = self.client.delete("/event/tags/2/pf", headers={"Authorization": f"Basic {credentials}"})
        print(res.status_code)
        assert res.status_code == 401
