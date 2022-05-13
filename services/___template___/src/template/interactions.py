from template.models import Model


class ExampleInteractions:
    def __init__(self, **repositories):
        self._database_repository = repositories["database_repository"]
        self._pubsub_repository = repositories["pubsub_repository"]
        self._web_repository = repositories["web_repository"]

    def list(self):
        return [m.to_dict() for m in self._database_repository.list_models()]

    def store(self, data):
        model = Model(input=data["input"], output=data["output"])

        return self._database_repository.store_model(model).to_dict()

    def pull(self):
        return self._pubsub_repository.pull(self._pubsub_repository.TEST_TOPIC)

    def push(self, message):
        return self._pubsub_repository.push(self._pubsub_repository.TEST_TOPIC, message)

    def get(self):
        return self._web_repository.get(
            self._web_repository.TEST_SERVICE + "/endpoint/",
        )

    def post(self, data):
        return self._web_repository.post(
            self._web_repository.TEST_SERVICE + "/endpoint/",
            data,
        )

    def put(self, data):
        return self._web_repository.put(
            self._web_repository.TEST_SERVICE + "/endpoint/",
            data,
        )
