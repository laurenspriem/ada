# pylint: disable=import-error, global-statement
import logging
import os

from sqlalchemy.engine.url import URL
from flask import jsonify
import functions_framework
import flask

from repositories import (
    ExampleDatabaseRepository,
    ExamplePredictorRepository,
    ExampleStorageRepository,
)
from interactions import ExampleDatabaseInteractions, ExamplePredictorInteractions, ExampleStorageInteractions
from db import db


log = logging.getLogger(__name__)

database_repository = None
predictor_repository = None
storage_repository = None


def _init_function():
    global database_repository, predictor_repository, storage_repository

    if not database_repository or not predictor_repository or not storage_repository:
        # Create database
        host = os.getenv("FUNCTION_DB_HOST")
        port = os.getenv("FUNCTION_DB_PORT")
        user = os.getenv("FUNCTION_DB_USER")
        password = os.getenv("FUNCTION_DB_PASSWORD")
        name = os.getenv("FUNCTION_DB_NAME")
        socket = os.getenv("FUNCTION_DB_SOCKET")
        instance = os.getenv("FUNCTION_DB_INSTANCE")

        uri = URL.create(
            drivername="postgresql+pg8000",
            host=host,
            port=port,
            username=user,
            password=password,
            database=name,
            query={"unix_sock": f"{socket}/{instance}/.s.PGSQL.5432"} if socket and instance else {}
        )
        flask.current_app.config["SQLALCHEMY_DATABASE_URI"] = uri
        flask.current_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        db.init_app(flask.current_app)
        db.create_all(app=flask.current_app)

        # Get model path
        model_path = os.getenv("FUNCTION_MODEL_PATH")

        # Get files path
        files_path = os.getenv("FUNCTION_FILES_PATH")

        # Create repositories
        database_repository = ExampleDatabaseRepository(db.session)
        predictor_repository = ExamplePredictorRepository(model_path)
        storage_repository = ExampleStorageRepository(files_path)


@functions_framework.http
def example_list_endpoint():
    interactions = ExampleDatabaseInteractions(database_repository)

    return jsonify(interactions.list())


@functions_framework.http
def example_store_endpoint(request):
    interactions = ExampleDatabaseInteractions(database_repository)

    return interactions.store(request.get_json())


@functions_framework.errorhandler(Exception)
def default_error(_):
    log.exception("Unhandled exception occurred:")

    return {"message": "Internal server error"}, 500


if __name__ == "main":
    _init_function()
