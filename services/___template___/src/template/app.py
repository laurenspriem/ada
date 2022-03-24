import os

from flask import Flask
from sqlalchemy.engine.url import URL
from werkzeug.exceptions import HTTPException

from template.repositories import ExampleDatabaseRepository, ExamplePredictorRepository, ExampleStorageRepository
from template.resources import resources
from template.db import db


def create_app():
    # Create app
    app = Flask(__name__)

    # Register resources
    app.register_blueprint(resources)

    # Register health
    @app.route("/api/health/")
    def default_health():
        return {"status": "OK"}

    # Register errors
    @app.errorhandler(HTTPException)
    def default_handler(error):
        return {"message": error.name}, error.code

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
    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    db.create_all(app=app)

    # Get model path
    model_path = os.getenv("FLASK_MODEL_PATH")

    # Get files path
    files_path = os.getenv("FLASK_FILES_PATH")

    # Create repositories
    setattr(
        app,
        "repositories",
        {
            "database_repository": ExampleDatabaseRepository(db.session),
            "predictor_repository": ExamplePredictorRepository(model_path),
            "storage_repository": ExampleStorageRepository(files_path),
        },
    )

    return app
