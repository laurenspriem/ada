from flask import Flask, request

from db import Base, engine
from resources.Bid import Bid

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)


@app.route('/bids', methods=['POST'])
def create_bid():
    req_data = request.get_json()
    return Bid.create(req_data)


@app.route('/bids/<bid_id>', methods=['GET'])
def get_bid(bid_id):
    return Bid.get(bid_id)


@app.route('/bids/<bid_id>', methods=['PUT'])
def update_bid(bid_id):
    req_data = request.get_json()
    return Bid.update(bid_id, req_data)


@app.route('/bids/<bid_id>', methods=['DELETE'])
def delete_bid(bid_id):
    return Bid.delete(bid_id)

app.run(host='0.0.0.0', port=5000)