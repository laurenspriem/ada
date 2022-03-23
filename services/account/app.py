from flask import Flask, request

from db import Base, engine
from resources.notificationsettings import NotificationSettings
from resources.profile import Profile
from resources.shippinginfo import ShippingInfo
from resources.user import User

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)

#create a user
@app.route('/users', methods=['POST'])
def create_user():
    req_data = request.get_json()
    return User.create(req_data)

#get a user
@app.route('/users/<d_username>', methods=['GET'])
def get_user(d_username):
    return User.get(d_username)

#update a user
@app.route('/users/<d_username>', methods=['PUT'])
def update_user(d_username):
    email = request.args.get('email')
    password = request.args.get('password')
    return User.update(d_username, email, password)

#update a user profile
@app.route('/users/<d_username>/profile', methods=['PUT'])
def update_profile(d_username):
    req_data = request.get_json()
    return Profile.update(d_username, req_data)

#update a user shipping information
@app.route('/users/<d_username>/shippinginfo', methods=['PUT'])
def update_shippinginfo(d_username):
    req_data = request.get_json()
    return ShippingInfo.update(d_username, req_data)

#update a user notification settings
@app.route('/users/<d_username>/notificationsettings', methods=['PUT'])
def update_notificationsettings(d_username):
    req_data = request.get_json()
    return NotificationSettings.update(d_username, req_data)

#delete a user
@app.route('/users/<d_username>', methods=['DELETE'])
def delete_user(d_username):
    return User.delete(d_username)


app.run(host='0.0.0.0', port=5000)