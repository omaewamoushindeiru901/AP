from os import abort
from flask import request, jsonify, abort
from sqlalchemy import and_

from models import User, Event, Tags
from schemas import UserSchema, EventSchema, TagSchema, tag_to_event, event_to_user, ConnectedSchema
from project import app, Session

user_schema = UserSchema()
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
        event = session.query(tag_to_event).filter_by(tag=tags).one()
    except:
        abort(404, description="Event not found")
    return TagSchema().dump(event)


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

    return jsonify({"Success": "User has been deleted from event"}), 200


if __name__ == "__main__":
    app.run(debug=True)
# serve(app, host='0.0.0.0', port=5000)
