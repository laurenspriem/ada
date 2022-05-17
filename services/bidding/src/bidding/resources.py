import flask

from flask import Blueprint, jsonify

from bidding.interactions import BiddingInteractions


resources = Blueprint("api", __name__, url_prefix="/api")


def bidding_interactions():
    return BiddingInteractions(**flask.current_app.repositories)


@resources.route("/bids/", methods=["POST"])
def create_bid():
    return bidding_interactions().create_bid(flask.request.json)


@resources.route("/bids/<d_id>", methods=["GET"])
def get_bid(d_id):
    return bidding_interactions().get_bid(d_id)


@resources.route("/bids/<d_id>", methods=["PUT"])
def update_bid(d_id):
    return bidding_interactions().update_bid(d_id, flask.request.json).to_dict()


@resources.route("/bids/<d_id>", methods=["DELETE"])
def delete_bid(d_id):
    bidding_interactions().delete_bid(d_id)

    return "", 204