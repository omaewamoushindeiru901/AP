from os import abort
from flask import request, jsonify, abort, make_response
from flask_restful import reqparse, fields, Resource, marshal_with
from models import User, Event, bcrypt, hash_password
from schemas import UserSchema, EventSchema, TagSchema, tag_to_event, event_to_user, ConnectedSchema
from project import *

'''user_schema = UserSchema()
event_schema = EventSchema()
tag_schema = TagSchema()


# USER
# GET
@app.route('/user/<user_name>/', methods=['GET'])
def get_user_by_username(user_name):
    session = Session()
    try:
        user = session.query(User).filter_by(username=user_name).one()
    except:
        abort(404, description="User not found")
    return UserSchema().dump(user)


@app.route('/user/', methods=['GET'])
def get_all_users():
    session = Session()
    all_users = session.query(User).all()
    return jsonify(UserSchema(many=True).dump(all_users))


# POST
@app.route('/user/', methods=['POST'])
def create_user():
    session = Session()
    data = request.get_json()
    try:
        user = User(**data)
    except:
        return jsonify({"Message": "Invalid input"}), 405
    user.hash_password()
    session.add(user)
    session.commit()
    return jsonify({"Success": "User has been created"}), 200


# PUT
@app.route('/user/<int:user_id>/', methods=['PUT'])
def update_user(user_id):
    session = Session()
    try:
        user = session.query(User).filter_by(id=int(user_id)).one()
    except:
        abort(404, description="User not found")
    data = request.get_json()
    try:
        if data.get('firstName', None):
            user.firstName = data['firstName']
        if data.get('lastName', None):
            user.lastName = data['lastName']
        if data.get('username', None):
            user.username = data['username']
        if data.get('password', None):
            user.password = data['password']
            user.hash_password()
        if data.get('email', None):
            user.email = data['email']
        if data.get('phone', None):
            user.phone = data['phone']
    except:
        abort(405, description="Invalid input")
    session.commit()
    return jsonify({"Success": "User has been updated"}), 200


# DELETE
@app.route('/user/<int:user_id>/', methods=['DELETE'])
def delete_user(user_id):
    session = Session()
    try:
        user = session.query(User).filter_by(id=int(user_id)).one()
    except:
        abort(404, description="User not found")
    try:
        events = session.query(Event).filter_by(creatorid=int(user_id)).all()
    except:
        events = []

    session.delete(user)
    for event in events:
        session.delete(event)
    session.commit()
    return jsonify({"Success": "User has been deleted"}), 200


# EVENT
# POST
@app.route('/event/', methods=['POST'])
def create_event():
    session = Session()
    data = request.get_json()
    try:
        event = Event(**data)
    except:
        return jsonify({"Message": "Invalid input"}), 405
    session.add(event)
    session.commit()
    return jsonify({"Success": "Event has been created"}), 200


# GET
@app.route('/event/<int:eventid>/', methods=['GET'])
def get_event_by_id(eventid):
    session = Session()
    try:
        event = session.query(Event).filter_by(eventid=int(eventid)).one()
    except:
        abort(404, description="Event not found")
    return EventSchema().dump(event)


@app.route('/event/', methods=['GET'])
def get_all_events():
    session = Session()
    all_events = session.query(Event).all()
    return jsonify(EventSchema(many=True).dump(all_events))


@app.route('/event/<tags>/', methods=['GET'])
def get_event_by_tag(tags):
    session = Session()
    try:
        event = session.query(tag_to_event).filter_by(tag=tags).all()
    except:
        abort(404, description="Event not found")
    return jsonify(TagSchema(many=True).dump(event))


# DELETE

@app.route('/event/<int:eventid>/', methods=['DELETE'])
def delete_event(eventid):
    session = Session()
    try:
        event = session.query(Event).filter_by(eventid=int(eventid)).one()
    except:
        abort(404, description="Event not found")

    session.delete(event)
    session.commit()

    return jsonify({"Success": "Event has been deleted"}), 200


# PUT
@app.route('/event/<int:eventid>/', methods=['PUT'])
def update_event(eventid):
    session = Session()
    try:
        event = session.query(Event).filter_by(eventid=int(eventid)).one()
    except:
        abort(404, description="Event not found")
    data = request.get_json()
    try:
        if data.get('name', None):
            event.name = data['name']
        if data.get('content', None):
            event.content = data['content']
    except:
        abort(405, description="Invalid input")
    session.commit()
    return jsonify({"Success": "Event has been updated"}), 200


# TAG
# POST
@app.route('/event/tags/', methods=['POST'])
def create_tag():
    session = Session()
    data = request.get_json()
    try:
        tag = tag_to_event(**data)
    except:
        return jsonify({"Message": "Invalid input"}), 405
    session.add(tag)
    session.commit()
    return jsonify({"Success": "Tag has been created"}), 200


# GET
@app.route('/event/tags/', methods=['GET'])
def get_all_tags():
    session = Session()
    all_tags = session.query(tag_to_event).all()
    return jsonify(TagSchema(many=True).dump(all_tags))


# DELETE
@app.route('/event/tags/<int:event_id>/<tag>/', methods=['DELETE'])
def delete_tag(event_id, tag):
    session = Session()
    try:
        tag = session.query(tag_to_event).filter_by(eventid=event_id, tag=tag).first()
    except:
        abort(404, description="Tag not found")

    session.delete(tag)
    session.commit()

    return jsonify({"Success": "Tag has been deleted"}), 200


# CONNECTED USERS
# GET
@app.route('/user/connected/', methods=['GET'])
def get_all_connected():
    session = Session()
    all_connected = session.query(event_to_user).all()
    return jsonify(ConnectedSchema(many=True).dump(all_connected))


@app.route('/user/connected/<int:event_id>/<int:users_id>', methods=['GET'])
def get_connected_by_ids(event_id, users_id):
    session = Session()
    try:
        event = session.query(event_to_user).filter_by(eventid=event_id, usersid=users_id).first()
    except:
        abort(404, description="Event not found")
    return ConnectedSchema().dump(event)


# POST
@app.route('/user/connected/', methods=['POST'])
def create_connected():
    session = Session()
    data = request.get_json()
    try:
        connected = event_to_user(**data)
    except:
        return jsonify({"Invalid input"}), 405
    session.add(connected)
    session.commit()
    return jsonify({"Success": "User has been connected"}), 200


# DELETE
@app.route('/user/connected/<int:event_id>/<int:users_id>/', methods=['DELETE'])
def delete_connected(event_id, users_id):
    session = Session()
    try:
        event = session.query(event_to_user).filter_by(eventid=event_id, usersid=users_id).first()
    except:
        abort(404, description="User or id not found")
    session.delete(event)
    session.commit()

    return jsonify({"Success": "User has been deleted from event"}), 200'''


@auth.verify_password
def verify_user(username, password):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return user


user_put_args = reqparse.RequestParser()
user_put_args.add_argument("username", type=str, required=True)
user_put_args.add_argument("password", type=str, required=True)
user_put_args.add_argument("firstName", type=str, required=True)
user_put_args.add_argument("lastName", type=str, required=True)
user_put_args.add_argument("email", type=str, required=True)
user_put_args.add_argument("phone", type=str, required=True)

user_update_args = reqparse.RequestParser()
user_update_args.add_argument("id", type=int)
user_update_args.add_argument("username", type=str)
user_update_args.add_argument("password", type=str)
user_update_args.add_argument("firstName", type=str)
user_update_args.add_argument("lastName", type=str)
user_update_args.add_argument("email", type=str)
user_update_args.add_argument("phone", type=str)

user_resource_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'password': fields.String,
    'firstName': fields.String,
    'lastName': fields.String,
    'email': fields.String,
    'phone': fields.String
}


class UserApi(Resource):
    @auth.login_required
    @marshal_with(user_resource_fields)
    def get(self):
        session = Session()
        result = session.query(User).all()
        if not result:
            abort(404, message="No one user in database")
        return result

    @marshal_with(user_resource_fields)
    def post(self):
        session = Session()
        args = user_put_args.parse_args()
        result = User(username=args['username'], password=hash_password(args['password']),
                      firstName=args['firstName'], lastName=args['lastName'], email=args['email'], phone=args['phone'])
        session.add(result)
        session.commit()
        return result, 201

    @auth.login_required
    @marshal_with(user_resource_fields)
    def put(self):
        session = Session()
        args = user_update_args.parse_args()
        # result = session.query(User).filter_by(id=user_id).first()
        result = auth.current_user()
        if not result:
            abort(404, message="User doesn't exist, cannot update")
        if args['username']:
            result.username = args['username']
        if args['password']:
            result.password = hash_password(args['password'])
        if args['firstName']:
            result.firstName = args['firstName']
        if args['lastName']:
            result.lastName = args['lastName']
        if args['email']:
            result.email = args['email']
        if args['phone']:
            result.phone = args['phone']
        result = session.merge(result)
        session.add(result)
        session.commit()

        return result

    @auth.login_required
    def delete(self, user_id):
        session = Session()
        # result = session.query(User).filter_by(id=user_id).first()
        result = auth.current_user()
        if not result:
            abort(500, message="User doesn't exist, cannot delete")
        result = session.merge(result)
        session.delete(result)
        session.commit()
        return "User deleted", 204


class UseridApi(Resource):
    @auth.login_required
    @marshal_with(user_resource_fields)
    def get(self, user_id):
        session = Session()
        result = session.query(User).filter_by(id=user_id).first()
        if not result:
            abort(404, message="Couldn`t find user with that id")
        return result


event_put_args = reqparse.RequestParser()
event_put_args.add_argument("name", type=str, required=True)
event_put_args.add_argument("content", type=str, required=True)
event_put_args.add_argument("date", type=str, required=True)
event_put_args.add_argument("creatorid", type=int)

event_update_args = reqparse.RequestParser()
event_update_args.add_argument("name", type=str)
event_update_args.add_argument("content", type=str)
event_update_args.add_argument("date", type=str)

event_resource_fields = {
    'eventid': fields.Integer,
    'name': fields.String,
    'content': fields.String,
    'date': fields.String,
    'creatorid': fields.Integer
}


class EventApi(Resource):
    @auth.login_required
    @marshal_with(event_resource_fields)
    def get(self):
        session = Session()
        user = auth.current_user()
        creatorid = user.id
        result = session.query(Event).filter_by(creatorid=creatorid).all()
        if not result:
            abort(404, message="No event in database")

        return result

    @auth.login_required
    @marshal_with(event_resource_fields)
    def post(self):
        session = Session()
        args = event_put_args.parse_args()
        user = auth.current_user()
        creatorid = user.id
        event = Event(name=args['name'], content=args['content'], creatorid=creatorid, date=args['date'])
        session.add(event)
        session.commit()
        return event, 200


class EventidApi(Resource):
    @auth.login_required
    @marshal_with(event_resource_fields)
    def get(self, event_id):
        session = Session()
        result = session.query(Event).filter_by(eventid=event_id).first()
        usr = auth.current_user()
        if not result:
            abort(404, message="Couldn`t find event with that id")
        if result.creatorid != usr.id:
            abort(401, message="no access")
        return result, 200

    @auth.login_required
    @marshal_with(event_resource_fields)
    def put(self, event_id):
        session = Session()
        args = event_update_args.parse_args()
        result = session.query(Event).filter_by(eventid=event_id).first()
        user = auth.current_user()
        if not result.creatorid == user.id:
            abort(401, message="no access")
        if not result:
            abort(404, message="Event doesn't exist, cannot update")

        if args['name']:
            result.name = args['name']
        if args['content']:
            result.content = args['content']
        if args['date']:
            result.date = args['date']

        result = session.merge(result)

        session.add(result)
        session.commit()

        return result

    @auth.login_required
    def delete(self, event_id):
        session = Session()
        result = session.query(Event).filter_by(eventid=event_id).first()
        user = auth.current_user()
        if result.creatorid != user.id:
            abort(401, message="no access")
        if not result:
            abort(500, message="Event doesn't exist, cannot delete")
        result = session.merge(result)

        session.delete(result)
        session.commit()
        return "Event deleted", 205


tag_put_args = reqparse.RequestParser()
tag_put_args.add_argument("eventid", type=int, required=True)
tag_put_args.add_argument("tag", type=str, required=True)

tag_resource_fields = {
    'eventid': fields.Integer,
    'tag': fields.String
}


class TagApi(Resource):
    @auth.login_required
    @marshal_with(tag_resource_fields)
    def get(self, eventid):
        session = Session()
        result = session.query(tag_to_event).filter_by(eventid=eventid).all()

        if not result:
            abort(404, message="No tags in database")

        return result

    @auth.login_required
    @marshal_with(tag_resource_fields)
    def post(self):
        session = Session()
        args = tag_put_args.parse_args()
        tag = tag_to_event(eventid=args['eventid'], tag=args['tag'])
        session.add(tag)
        session.commit()
        return tag, 200


class TagidApi(Resource):
    @auth.login_required
    def delete(self, event_id, tag):
        session = Session()
        result = session.query(tag_to_event).filter_by(eventid=event_id, tag=tag).first()
        if not result:
            abort(500, message="Tag doesn't exist, can`t delete")
        result = session.merge(result)

        session.delete(result)
        session.commit()
        return "Tag deleted", 200


connected_put_args = reqparse.RequestParser()
connected_put_args.add_argument("eventid", type=int)
connected_put_args.add_argument("usersid", type=int, required=True)

connected_resource_fields = {
    'eventid': fields.Integer,
    'usersid': fields.Integer
}


class ConnectedApi(Resource):
    @auth.login_required
    @marshal_with(connected_resource_fields)
    def get(self, eventid):
        session = Session()
        result = session.query(event_to_user).filter_by(eventid=eventid).all()
        event=session.query(Event).filter_by(eventid=eventid).first()
        user=auth.current_user()
        if event.creatorid != user.id:
            abort(401, message=" no access")
        if not result:
            abort(404, message="No connected users in database")

        return result

    @auth.login_required
    @marshal_with(connected_resource_fields)
    def post(self, eventid):
        session = Session()
        args = connected_put_args.parse_args()
        event = session.query(Event).filter_by(eventid=eventid).first()
        user = auth.current_user()
        if event.creatorid != user.id:
            abort(401, message=" no access")
        connected = event_to_user(eventid=eventid, usersid=args['usersid'])
        session.add(connected)
        session.commit()
        return connected, 200


class ConnectedidApi(Resource):
    @auth.login_required
    def delete(self, event_id, users_id):
        session = Session()
        event = session.query(Event).filter_by(eventid=event_id).first()
        user = auth.current_user()
        if event.creatorid != user.id:
            abort(401, message=" no access")
        result = session.query(event_to_user).filter_by(eventid=event_id, usersid=users_id).first()
        if not result:
            abort(500, message="Connected user doesn't exist, can`t delete")
        result = session.merge(result)

        session.delete(result)
        session.commit()
        return "Connected user deleted", 200


api.add_resource(UseridApi, "/user/<int:user_id>")
api.add_resource(UserApi, "/user")

api.add_resource(EventidApi, "/event/<int:event_id>")
api.add_resource(EventApi, "/event")

api.add_resource(TagApi, "/event/tags/<int:eventid>")
api.add_resource(TagidApi, "/event/tags/<int:event_id>/<tag>")

api.add_resource(ConnectedApi, "/event/connected/<int:eventid>")
api.add_resource(ConnectedidApi, "/event/connected/<int:event_id>/<int:users_id>")

if __name__ == "__main__":
    app.run(debug=True)
# serve(app, host='0.0.0.0', port=5000)
