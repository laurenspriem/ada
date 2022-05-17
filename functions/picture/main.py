# pylint: disable=global-statement
import logging
import os

from google.cloud import storage
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import scoped_session, sessionmaker

import functions_framework
import flask

from repositories import MetadataRepository, StorageRepository, NotFoundError
from interactions import PictureInteractions
from db import Base


log = logging.getLogger(__name__)

metadata_repository = None
storage_repository = None


def _connect_db():
    global metadata_repository

    if not metadata_repository:
        # Load config
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_socket = os.getenv("DB_SOCKET")
        db_instance = os.getenv("DB_INSTANCE")
        db_name = os.getenv("DB_NAME")

        # Create uri
        uri = URL.create(
            drivername="postgresql+pg8000",
            host=db_host,
            port=db_port,
            username=db_user,
            password=db_password,
            database=db_name,
            query={"unix_sock": f"{db_socket}/{db_instance}/.s.PGSQL.5432"}
            if db_socket and db_instance
            else {},
        )

        # Create engine
        engine = create_engine(uri)

        # Create session
        session = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=engine,
            )
        )

        # Create tables
        Base.metadata.create_all(bind=engine)

        # Create repository
        metadata_repository = MetadataRepository(session)


def _connect_storage():
    global storage_repository

    if not storage_repository:
        # Load config
        storage_bucket = os.getenv("STORAGE_BUCKET")

        # Create client
        storage_client = storage.Client()

        # Create repository
        storage_repository = StorageRepository(storage_client, storage_bucket)


@functions_framework.http
def upload_picture(request):
    interactions = PictureInteractions(metadata_repository, storage_repository)

    if not request.method == "POST":
        return {"message": "Method not allowed"}, 405

    if not request.content_type or not request.content_type.startswith(
        "multipart/form-data"
    ):
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
    _connect_db()
    _connect_storage()
