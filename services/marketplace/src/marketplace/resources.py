import flask

from flask import Blueprint, jsonify

from marketplace.interactions import ItemInteractions

resources = Blueprint("api", __name__, url_prefix="/api")


def item_interactions():
    return ItemInteractions(**flask.current_app.repositories)


@resources.route("/items/<d_item_id>", methods=["GET"])
def get_item(d_item_id):
    return item_interactions().get(d_item_id)


@resources.route("/items/list/<user_id>", methods=["GET"])
def get_list(user_id):
    return jsonify(item_interactions().getlist(user_id))


@resources.route("/items/search/<keyword>", methods=["GET"])
def search_keyword(keyword):
    return jsonify(item_interactions().search(keyword))


@resources.route("/items/", methods=["POST"])
def create_item():
    return item_interactions().create(flask.request.json)


@resources.route("/items/<item_id>", methods=["PUT"])
def update_item(item_id):
    return item_interactions().update(item_id, flask.request.json)


@resources.route("/items/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    item_interactions().delete(item_id)

    return "", 204
