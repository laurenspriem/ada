# pylint: disable=import-error, global-statement
import logging
import os

from sqlalchemy.engine.url import URL
import functions_framework
import flask

from repositories import AuthenticationRepository, InvalidTokenError, NotFoundError
from interactions import AuthenticationInteractions, InvalidCredentialsError
from db import db


log = logging.getLogger(__name__)

authentication_repository = None


def _init_function():
    global authentication_repository

    if not authentication_repository:
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

        # Create authentication client
        secret = os.getenv("FUNCTION_JWT_SECRET")

        # Create repositories
        authentication_repository = AuthenticationRepository(db.session, secret)


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
    _init_function()
