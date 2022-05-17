import json

from google.api_core.exceptions import AlreadyExists

from bidding.models import Bid


class BidDatabaseRepository:
    def __init__(self, session):
        self._session = session

    def create_bid(self, bid):
        self._session.add(bid)
        self._session.commit()
        self._session.refresh(bid)
        return bid

    def get_bid(self, d_id):
        bid = self._session.query(Bid).filter(Bid.id == d_id).first()
        return bid

    def update_bid(self, d_id, d_price, d_status, d_bid_accepted, d_price_accepted):
        bid = self.get_user(d_id)
        bid.price = d_price
        bid.status = d_status
        bid.bid_accepted = d_bid_accepted
        bid.price_accepted = d_price_accepted
        self._session.commit()
        return bid

    def delete_bid(self, d_id):
        self._session.query(Bid).filter(Bid.id == d_id).delete()
        self._session.commit()
        return d_id

class ExamplePubSubRepository:
    TEST_TOPIC = "test"

    def __init__(self, project_id, publisher, subscriber):
        self._project_id = project_id
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
            f"{topic_path[topic_path.rindex('/')+1:]}-subscription",
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
