import os

from flask import Flask
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
    host = os.getenv("FLASK_DB_HOST")
    port = os.getenv("FLASK_DB_PORT")
    user = os.getenv("FLASK_DB_USER")
    password = os.getenv("FLASK_DB_PASSWORD")
    name = os.getenv("FLASK_DB_NAME")

    uri = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"
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
