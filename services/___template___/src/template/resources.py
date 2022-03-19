import flask

from flask import Blueprint, jsonify

from template.interactions import (
    ExampleDatabaseInteractions,
    ExamplePredictorInteractions,
    ExampleStorageInteractions,
)

resources = Blueprint("api", __name__, url_prefix="/api")


def example_database_interactions():
    return ExampleDatabaseInteractions(**flask.current_app.repositories)


def example_predictor_interactions():
    return ExamplePredictorInteractions(**flask.current_app.repositories)


def example_storage_interactions():
    return ExampleStorageInteractions(**flask.current_app.repositories)


@resources.route("/example/", methods=["GET"])
def example_list_endpoint():
    return jsonify(example_database_interactions().list())


@resources.route("/example/", methods=["POST"])
def example_store_endpoint():
    return example_database_interactions().store(flask.request.json)
