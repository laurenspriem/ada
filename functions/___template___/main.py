# pylint: disable=global-statement
import logging
import os

from google.cloud import pubsub
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import jsonify

import functions_framework

from repositories import (
    ExampleDatabaseRepository,
    ExamplePubSubRepository,
    ExampleWebRepository,
)
from interactions import ExampleInteractions
from web import WebClient
from db import Base


log = logging.getLogger(__name__)

database_repository = None
pubsub_repository = None
web_repository = None


def _connect_db():
    global database_repository

    if not database_repository:
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
        database_repository = ExampleDatabaseRepository(session)


def _connect_pubsub():
    global pubsub_repository

    if not pubsub_repository:
        # Load config
        pubsub_project_id = os.getenv("PUBSUB_PROJECT_ID")
        pubsub_project_name = __name__.split(".", maxsplit=1)[0]

        # Create client
        publisher = pubsub.PublisherClient()

        # Create repository
        pubsub_repository = ExamplePubSubRepository(
            pubsub_project_id,
            pubsub_project_name,
            publisher,
        )


def _connect_web():
    global web_repository

    if not web_repository:
        # Create client
        client = WebClient()

        # Create repository
        web_repository = ExampleWebRepository(client)


@functions_framework.http
def example_list_endpoint(request):
    interactions = ExampleInteractions(
        database_repository,
        pubsub_repository,
        web_repository,
    )

    return jsonify(interactions.list())


@functions_framework.http
def example_store_endpoint(request):
    interactions = ExampleInteractions(
        database_repository,
        pubsub_repository,
        web_repository,
    )

    return interactions.store(request.get_json())


@functions_framework.errorhandler(Exception)
def default_error(_):
    log.exception("Unhandled exception occurred:")

    return {"message": "Internal server error"}, 500


if __name__ == "main":
    _connect_db()
    _connect_pubsub()
    _connect_web()
