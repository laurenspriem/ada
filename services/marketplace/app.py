from flask import Flask, request

from db import Base, engine
from resources.item import Item

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['JSON_SORT_KEYS'] = False
Base.metadata.create_all(engine)


@app.route('/items', methods=['POST'])
def create_item():
    req_data = request.get_json()
    return Item.create(req_data)


@app.route('/items/<item_id>', methods=['GET'])
def get_item(item_id):
    return Item.get(item_id)


@app.route('/items/<item_id>', methods=['PUT'])
def update_item(item_id):
    req_data = request.get_json()
    return Item.update(item_id, req_data)


@app.route('/items/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    return Item.delete(item_id)

@app.route('/items/list/<user_id>', methods=['GET'])
def get_list(user_id):
    return Item.getlist(user_id)

@app.route('/items/search/<keyword>', methods=['GET'])
def search(keyword):
    return Item.search(keyword)


app.run(host='0.0.0.0', port=5000)