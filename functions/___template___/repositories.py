import json

from google.api_core.exceptions import AlreadyExists

from models import Model


class ExampleDatabaseRepository:
    def __init__(self, session):
        self._session = session

    def list_models(self):
        return self._session.query(Model)

    def store_model(self, model):
        self._session.add(model)
        self._session.commit()

        return model


class ExamplePubSubRepository:
    TEST_TOPIC = "test"

    def __init__(self, project_id, project_name, publisher):
        self._project_id = project_id
        self._project_name = project_name
        self._publisher = publisher

    def push(self, topic, message):
        topic_path = self._ensure_topic_exists(topic)

        res = self._publisher.publish(topic_path, str.encode(json.dumps(message)))

        return {"message_id": res.result()}

    def _ensure_topic_exists(self, topic):
        topic_path = self._publisher.topic_path(self._project_id, topic)

        try:
            self._publisher.create_topic(name=topic_path)
        except AlreadyExists:
            pass

        return topic_path


class ExampleWebRepository:
    TEST_FUNCTION = "http://test:8080/api"

    def __init__(self, client):
        self._client = client

    def get(self, endpoint):
        return self._client.get(endpoint)

    def post(self, endpoint, data):
        return self._client.post(endpoint, data=data)

    def put(self, endpoint, data):
        return self._client.put(endpoint, data=data)
