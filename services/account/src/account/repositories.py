import json

from google.api_core.exceptions import AlreadyExists

from account.models import (
    User,
    Profile,
    NotificationSettings,
    PaymentInfo,
    ShippingInfo,
)


class UserDatabaseRepository:
    def __init__(self, session):
        self._session = session

    def create_user(self, user):
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user

    def get_user(self, d_username):
        user = self._session.query(User).filter(User.username == d_username).first()
        return user

    def update_user(self, d_username, d_email, d_password):
        user = self.get_user(d_username)
        user.email = d_email
        user.password = d_password
        self._session.commit()
        return user

    def delete_user(self, d_username):
        self._session.query(User).filter(User.username == d_username).delete()
        self._session.commit()
        return d_username

    def update_profile(
        self,
        d_username,
        d_birthday,
        d_gender,
        d_height,
        d_shirt_size,
        d_jeans_size,
        d_shoe_size,
    ):
        user = self.get_user(d_username)
        user.profile.birthday = d_birthday
        user.profile.gender = d_gender
        user.profile.height = d_height
        user.profile.shirt_size = d_shirt_size
        user.profile.jeans_size = d_jeans_size
        user.profile.shoe_size = d_shoe_size
        self._session.commit()
        return user

    def update_shippinginfo(
        self, d_username, d_street, d_street_number, d_zip_code, d_city
    ):
        user = self.get_user(d_username)
        user.shippinginfo.street = d_street
        user.shippinginfo.street_number = d_street_number
        user.shippinginfo.zip_code = d_zip_code
        user.shippinginfo.city = d_city
        self._session.commit()
        return user

    def update_notificationsettings(
        self,
        d_username,
        d_item_notifications_enabled,
        d_bids_notifications_enabled,
        d_chat_notifications_enabled,
        d_news_notifications_enabled,
    ):
        user = self.get_user(d_username)
        user.notificationsettings.item_notifications_enabled = (
            d_item_notifications_enabled
        )
        user.notificationsettings.bids_notifications_enabled = (
            d_bids_notifications_enabled
        )
        user.notificationsettings.chat_notifications_enabled = (
            d_chat_notifications_enabled
        )
        user.notificationsettings.news_notifications_enabled = (
            d_news_notifications_enabled
        )
        self._session.commit()
        return user

    def update_paymentinfo(self, d_username, d_iban, d_name, d_bank):
        user = self.get_user(d_username)
        user.paymentinfo.iban = d_iban
        user.paymentinfo.name = d_name
        user.paymentinfo.bank = d_bank
        self._session.commit()
        return user


class ExamplePubSubRepository:
    USER_BLOCKED_TOPIC = "jads-adaassignment-user-blocked"

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
