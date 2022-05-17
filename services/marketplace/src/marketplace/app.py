import os

from flask import Flask
from huey import MemoryHuey
from google.cloud import pubsub
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.exceptions import HTTPException

from marketplace.repositories import (
    ItemDatabaseRepository,
    ItemPubSubRepository,
    ItemWebRepository,
)
from marketplace.resources import resources
from marketplace.web import WebClient
from marketplace.db import Base


def _connect_db():
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

    return session


def _connect_pubsub():
    # Load config
    pubsub_project_id = os.getenv("PUBSUB_PROJECT_ID")

    # Create client
    publisher = pubsub.PublisherClient()
    subscriber = pubsub.SubscriberClient()

    return pubsub_project_id, publisher, subscriber


def _connect_web():
    # Create client
    client = WebClient()

    return client


def create_app():
    # Create app
    flask = Flask(__name__)

    # Register resources
    flask.register_blueprint(resources)

    # Register health
    @flask.route("/api/health/")
    def default_health():
        return {"status": "OK"}

    # Register errors
    @flask.errorhandler(HTTPException)
    def default_handler(error):
        return {"message": error.name}, error.code

    # Create database
    session = _connect_db()

    # Create pub/sub
    project_id, publisher, subscriber = _connect_pubsub()

    # Create web
    client = _connect_web()

    # Set repositories
    setattr(
        flask,
        "repositories",
        {
            "database_repository": ItemDatabaseRepository(session),
            "pubsub_repository": ItemPubSubRepository(
                project_id,
                publisher,
                subscriber,
            ),
            "web_repository": ItemWebRepository(client),
        },
    )

    return flask


def create_worker():
    # Create worker
    huey = MemoryHuey()

    # Create database
    session = _connect_db()

    # Create pub/sub
    project, publisher, subscriber = _connect_pubsub()

    # Create web
    client = _connect_web()

    # Set subscriptions
    setattr(
        huey,
        "repositories",
        {
            "database_repository": ItemDatabaseRepository(session),
            "pubsub_repository": ItemPubSubRepository(
                project,
                publisher,
                subscriber,
            ),
            "web_repository": ItemWebRepository(client),
        },
    )

    return huey


app = create_app()
worker = create_worker()