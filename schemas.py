from models import *
from marshmallow import Schema


class UserSchema(Schema):
    class Meta:
        model = User
        fields = ("id", "username", "firstName", "lastName", "email", "password", "phone")


class EventSchema(Schema):
    class Meta:
        model = Event
        fields = ("creatorid", "eventid", "name", "content", "date")


class TagSchema(Schema):
    class Meta:
        model = Tags
        fields = ("eventid", "tag")


class ConnectedSchema(Schema):
    class Meta:
        model = event_to_user
        fields = ("eventid", "usersid")
