from models import Model


class ExampleInteractions:
    def __init__(self, database_repository, pubsub_repository, web_repository):
        self._database_repository = database_repository
        self._pubsub_repository = pubsub_repository
        self._web_repository = web_repository

    def list(self):
        return [m.to_dict() for m in self._database_repository.list_models()]

    def store(self, data):
        model = Model(input=data["input"], output=data["output"])

        return self._database_repository.store_model(model).to_dict()
