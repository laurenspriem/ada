# pylint: disable=import-error
from models import Model


class ExampleDatabaseInteractions:
    def __init__(self, database_repository):
        self._database_repository = database_repository

    def list(self):
        return [m.to_dict() for m in self._database_repository.list_models()]

    def store(self, data):
        model = Model(input=data["input"], output=data["output"])

        return self._database_repository.store_model(model).to_dict()


class ExamplePredictorInteractions:
    def __init__(self, predictor_repository):
        self._predictor_repository = predictor_repository

    def create(self, data):
        prediction = self._predictor_repository.create_prediction(data)

        return {"output": float(prediction)}


class ExampleStorageInteractions:
    def __init__(self, storage_repository):
        self._storage_repository = storage_repository

    def load(self, name):
        return self._storage_repository.load_file(name)

    def store(self, file):
        name = self._storage_repository.store_file(file)

        return {"name": name}
