import json

from google.api_core.exceptions import AlreadyExists

from template.models import Model


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

    def __init__(self, project_id, project_name, publisher, subscriber):
        self._project_id = project_id
        self._project_name = project_name
        self._publisher = publisher
        self._subscriber = subscriber

    def pull(self, topic):
        topic_path = self._ensure_topic_exists(topic)
        subscription_path = self._ensure_subscription_exists(topic_path)

        res = self._subscriber.pull(
            subscription=subscription_path,
            return_immediately=True,
            max_messages=1,
        )

        if len(res.received_messages) == 0:
            return []

        received_message_ids = [m.ack_id for m in res.received_messages]
        received_message_data = [
            json.loads(m.message.data.decode("utf-8")) for m in res.received_messages
        ]

        self._subscriber.acknowledge(
            subscription=subscription_path,
            ack_ids=received_message_ids,
        )

        return received_message_data

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

    def _ensure_subscription_exists(self, topic_path):
        subscription_path = self._subscriber.subscription_path(
            self._project_id,
            f"{topic_path[topic_path.rindex('/')+1:]}-{self._project_name}-subscription",
        )

        try:
            self._subscriber.create_subscription(
                name=subscription_path,
                topic=topic_path,
            )
        except AlreadyExists:
            pass

        return subscription_path


class ExampleWebRepository:
    TEST_SERVICE = "http://test:8080/api"

    def __init__(self, client):
        self._client = client

    def get(self, endpoint):
        return self._client.get(endpoint)

    def post(self, endpoint, data):
        return self._client.post(endpoint, data=data)

    def put(self, endpoint, data):
        return self._client.put(endpoint, data=data)
