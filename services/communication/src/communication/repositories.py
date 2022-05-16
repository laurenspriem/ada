import json

import sqlalchemy as sa

from google.api_core.exceptions import AlreadyExists

from communication.models import Chat, Message


class CommunicationDatabaseRepository:
    def __init__(self, session):
        self._session = session

    def get_chat(self, chat_id):
        return self._session.query(Chat).filter(Chat.id == chat_id).first()

    def get_message(self, message_id):
        return self._session.query(Message).filter(Message.id == message_id).first()

    def get_chats_for_user(self, user_id):
        return self._session.query(Chat).filter(
            sa.or_(
                Chat.participant_1_id == user_id,
                Chat.participant_2_id == user_id,
            )
        )

    def create_chat(self, chat):
        self._session.add(chat)
        self._session.commit()

        return chat

    def create_message(self, chat, message):
        chat.messages.append(message)
        self._session.commit()

        return message

    def delete_chat(self, chat_id):
        self._session.query(Chat).filter(Chat.id == chat_id).delete()
        self._session.commit()

        return chat_id


class CommunicationPubSubRepository:
    ITEM_UPDATE_TOPIC = "jads-adaassignment-item-update"
    MESSAGE_SEND_TOPIC = "jads-adaassignment-message-send"
    OFFER_ACCEPTED_TOPIC = "jads-adaassignment-offer-accepted"
    USER_BLOCKED_TOPIC = "jads-adaassignment-user-blocked"

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


class CommunicationWebRepository:
    # TODO(tomdewildt): update endpoints
    UPLOAD_PICTURE_FUNCTION = "http://upload_picture_func:8080/"
    DOWNLOAD_PICTURE_FUNCTION = "http://download_picture_func:8080/"

    def __init__(self, client):
        self._client = client

    def upload_picture(self, file):
        return self._client.post(self.UPLOAD_PICTURE_FUNCTION, file=file)
