import flask

from flask import Blueprint, jsonify

from template.interactions import ExampleInteractions


resources = Blueprint("api", __name__, url_prefix="/api")


def example_interactions():
    return ExampleInteractions(**flask.current_app.repositories)


@resources.route("/list/", methods=["GET"])
def example_db_list_endpoint():
    return jsonify(example_interactions().list())


@resources.route("/store/", methods=["POST"])
def example_db_store_endpoint():
    return example_interactions().store(flask.request.json)


@resources.route("/pull/", methods=["GET"])
def example_pubsub_pull_endpoint():
    return jsonify(example_interactions().pull())


@resources.route("/push/", methods=["POST"])
def example_pubsub_push_endpoint():
    return example_interactions().push(flask.request.json)


@resources.route("/get/", methods=["GET"])
def example_web_get_endpoint():
    return example_interactions().get()


@resources.route("/post/", methods=["POST"])
def example_web_post_endpoint():
    return example_interactions().post(flask.request.json)


@resources.route("/put/", methods=["PUT"])
def example_web_put_endpoint():
    return example_interactions().put(flask.request.json)
