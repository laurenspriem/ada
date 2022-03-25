# pylint: disable=import-error, global-statement
import logging
import os

from sqlalchemy.engine.url import URL
from google.cloud import storage
import functions_framework
import flask

from repositories import MetadataRepository, StorageRepository, NotFoundError
from interactions import PictureInteractions
from db import db


log = logging.getLogger(__name__)

metadata_repository = None
storage_repository = None


def _init_function():
    global metadata_repository, storage_repository

    if not metadata_repository or not storage_repository:
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

        # Create storage client
        storage_bucket = os.getenv("FUNCTION_STORAGE_BUCKET")

        storage_client = storage.Client()

        # Create repositories
        metadata_repository = MetadataRepository(db.session)
        storage_repository = StorageRepository(storage_client, storage_bucket)


@functions_framework.http
def upload_picture(request):
    interactions = PictureInteractions(metadata_repository, storage_repository)

    if not request.method == "POST":
        return {"message": "Method not allowed"}, 405

    if not request.content_type or not request.content_type.startswith("multipart/form-data"):
        return {"message": "Invalid content type"}, 400

    if not request.files.get("file"):
        return {"message": "Invalid file"}, 400

    return interactions.upload(flask.request.files.get("file"))


@functions_framework.http
def download_picture(request):
    interactions = PictureInteractions(metadata_repository, storage_repository)

    if not request.method == "GET":
        return {"message": "Method not allowed"}, 405

    if request.view_args["path"] == "" or not request.view_args["path"].isdigit():
        return {"message": "Invalid id"}, 400

    try:
        return interactions.download(int(request.view_args["path"]))
    except NotFoundError:
        return {"message": "Not found"}, 404


@functions_framework.errorhandler(Exception)
def default_error(_):
    log.exception("Unhandled exception occurred:")

    return {"message": "Internal server error"}, 500


if __name__ == "main":
    _init_function()
