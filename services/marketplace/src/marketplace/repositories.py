import json

from google.api_core.exceptions import AlreadyExists

from marketplace.models import Item


class ItemDatabaseRepository:
    def __init__(self, session):
        self._session = session

    # Retrieve information of specific item of certain user
    def get_item(self, d_item_id):
        item = self._session.query(Item).filter(Item.id == d_item_id).first()

        return item

    # Retrieve all listed items of certain user
    def get_itemlist(self, d_user_id):
        items = self._session.query(Item).filter(Item.user_id == d_user_id).all()

        return items

    # Search in marketplace on keywords for listed items matching keywords
    def search_item(self, d_keyword):
        items = (
            self._session.query(Item).filter(Item.description.contains(d_keyword)).all()
        )

        return items

    # Create item
    def create_item(self, item):
        self._session.add(item)
        self._session.commit()
        self._session.refresh(item)

        return item

    # Edit item of certain user
    def update_item(
        self,
        d_item_id,
        d_title,
        d_description,
        d_brand,
        d_type,
        d_size,
        d_color,
        d_state,
        d_user_id,
        d_price,
        d_status,
    ):
        item = self.get_item(d_item_id)

        item.title = d_title
        item.description = d_description
        item.brand = d_brand
        item.type = d_type
        item.size = d_size
        item.color = d_color
        item.state = d_state
        item.user_id = d_user_id
        item.price = d_price
        item.status = d_status

        self._session.commit()

        return item

    # Delete item of certain user
    def delete_item(self, d_item_id):
        self._session.query(Item).filter(Item.id == d_item_id).delete()
        self._session.commit()

        return d_item_id


class ItemPubSubRepository:
    #REFUND_TOPIC = "fintet-refund"
    #ITEM_RECEIVED_TOPIC = "fintet-item-received"
    ITEM_UPDATE_TOPIC = "jads-adaassignment-item-update"
    OFFER_ACCEPTED_TOPIC = "jads-adaassignment-offer-accepted"
    #TRANSACTION_CANCELLED_TOPIC = "fintet-transaction-cancelled"

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


class ItemWebRepository:
    UPLOAD_PICTURE_FUNCTION = "https://europe-west3-jads-adaassignment.cloudfunctions.net/fintet-upload-picture"
    DOWNLOAD_PICTURE_FUNCTION = "https://europe-west3-jads-adaassignment.cloudfunctions.net/fintet-download-picture"

    def __init__(self, client):
        self._client = client

    def upload_picture(self, file):
        pass

    def download_picture(self, metadata_id):
        pass
