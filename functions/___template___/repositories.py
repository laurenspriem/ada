# pylint: disable=import-error
import os
import io
import pickle
import hashlib

from models import Model


class NotFoundError(Exception):
    pass


class ExampleDatabaseRepository:
    def __init__(self, session):
        self._session = session

    def list_models(self):
        return self._session.query(Model)

    def store_model(self, model):
        self._session.add(model)
        self._session.commit()

        return model


class ExamplePredictorRepository:
    def __init__(self, path):
        with open(path, "rb") as handle:
            self._model = pickle.load(handle)

    def create_prediction(self, inputs):
        if not hasattr(self, "_model") or not self._model:
            raise NotFoundError()

        return self._model.predict([inputs])[0]


class ExampleStorageRepository:
    def __init__(self, files_path):
        self._files_path = files_path

        self._ensure_exists(files_path)

    def load_file(self, name):
        with open(self._files_path + name, "rb") as handle:
            return io.BytesIO(handle.read())

    def store_file(self, file):
        content = file.read()
        digest = hashlib.md5(content).hexdigest()
        extension = file.filename.split(".")[-1]

        name = f"{digest}.{extension}"

        with open(self._files_path + name, "wb") as handle:
            handle.write(content)

        return name

    def _ensure_exists(self, path):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError:
            pass
