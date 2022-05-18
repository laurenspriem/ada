# pylint: disable=global-statement
import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import scoped_session, sessionmaker

import functions_framework

from repositories import AuthenticationRepository, InvalidTokenError, NotFoundError
from interactions import AuthenticationInteractions, InvalidCredentialsError
from db import Base


log = logging.getLogger(__name__)

authentication_repository = None


def _connect_db():
    global authentication_repository

    if not authentication_repository:
        # Load config
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_socket = os.getenv("DB_SOCKET")
        db_instance = os.getenv("DB_INSTANCE")
        db_name = os.getenv("DB_NAME")
        jwt_secret = os.getenv("JWT_SECRET")

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
        authentication_repository = AuthenticationRepository(session, jwt_secret)


@functions_framework.http
def authenticate(request):
    interactions = AuthenticationInteractions(authentication_repository)

    if not request.method == "POST":
        return {"message": "Method not allowed"}, 405

    body = request.get_json()
    if not body.get("username") or not body.get("password"):
        return {"message": "Missing username or password"}, 400

    try:
        return interactions.authenticate(body["username"], body["password"])
    except NotFoundError:
        return {"message": "Invalid username or password"}, 400
    except InvalidCredentialsError:
        return {"message": "Invalid username or password"}, 400


@functions_framework.http
def verify(request):
    interactions = AuthenticationInteractions(authentication_repository)

    if not request.method == "POST":
        return {"message": "Method not allowed"}, 405

    body = request.get_json()
    if not body.get("token"):
        return {"message": "Missing token"}, 400

    try:
        if interactions.verify(body["token"]):
            return {"message": "Valid token"}
    except InvalidTokenError:
        return {"message": "Invalid token"}, 401


@functions_framework.errorhandler(Exception)
def default_error(_):
    log.exception("Unhandled exception occurred:")

    return {"message": "Internal server error"}, 500


if __name__ == "main":
    _connect_db()
