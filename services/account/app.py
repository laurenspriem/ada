from flask import Flask, request

from db import Base, engine
from resources.notificationsettings import NotificationSettings
from resources.profile import Profile
from resources.shippinginfo import ShippingInfo
from resources.user import User

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)


@app.route('/users', methods=['POST'])
def create_user():
    req_data = request.get_json()
    return User.create(req_data)


@app.route('/users/<d_username>', methods=['GET'])
def get_user(d_username):
    return User.get(d_username)

@app.route('/users/<d_username>/profile', methods=['PUT'])
def update_user(d_username):
    email = request.args.get('email')
    password = request.args.get('password')
    return User.update(d_username, email, password)

@app.route('/users/<d_username>/profile', methods=['PUT'])
def update_profile(d_username):
    age = request.args.get('age')
    height = request.args.get('height')
    shirt_size = request.args.get('shirt_size')
    jeans_size = request.args.get('jeans_size')
    shoe_size = request.args.get('shoe_size')
    return Profile.update(d_username, age, height, shirt_size, jeans_size, shoe_size)

@app.route('/users/<d_username>/shippinginfo', methods=['PUT'])
def update_shippinginfo(d_username):
    street = request.args.get('street')
    street_number = request.args.get('street_number')
    zip_code = request.args.get('zip_code')
    city = request.args.get('city')
    return ShippingInfo.update(d_username, street, street_number, zip_code, city)

@app.route('/users/<d_username>/notificationsettings', methods=['PUT'])
def update_notificationsettings(d_username):
    item_not = request.args.get('item_notifications')
    bids_not = request.args.get('bids_notifications')
    chat_not = request.args.get('chat_notifications')
    news_not = request.args.get('news_notifications')
    return NotificationSettings.update(d_username, item_not, bids_not, chat_not, news_not)

@app.route('/users/<d_username>', methods=['DELETE'])
def delete_user(d_username):
    return User.delete(d_username)


app.run(host='0.0.0.0', port=5000)