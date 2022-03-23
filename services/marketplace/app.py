from flask import Flask, request

from db import Base, engine
from resources.item import Item

app = Flask(__name__)
app.config["DEBUG"] = True
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
    return Item.update(item_id)


@app.route('/items/<d_id>', methods=['DELETE'])
def delete_item(item_id):
    return Item.delete(item_id)


app.run(host='0.0.0.0', port=5000)