from flask import Flask, request

from db import Base, engine
from resources.chat import Chat
from resources.message import Message

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)

#create a chat
@app.route('/chat', methods=['POST'])
def create_user():
    req_data = request.get_json()
    return Chat.create(req_data)

#get a chat
@app.route('/users/<d_id>', methods=['GET'])
def get_user(d_id):
    return Chat.get(d_id)

#update a message
@app.route('/users/<d_id>/message/<d_message>', methods=['PUT'])
def update_message(d_username, d_message):
    req_data = request.get_json()
    return Message.update(d_username,d_message, req_data)

#delete a chat
@app.route('/users/<d_id>', methods=['DELETE'])
def delete_user(d_username):
    return Chat.delete(d_username)


app.run(host='0.0.0.0', port=5000)