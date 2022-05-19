from account.models import (
    User,
    Profile,
    PaymentInfo,
    ShippingInfo,
    NotificationSettings,
)


class AccountInteractions:
    def __init__(self, **repositories):
        self._database_repository = repositories["database_repository"]
        self._pubsub_repository = repositories["pubsub_repository"]

    def create(self, data):
        user = User(
            username=data["username"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            password=data["password"],
            is_verified=data["is_verified"],
            profile=Profile(),
            notificationsettings=NotificationSettings(),
            shippinginfo=ShippingInfo(),
            paymentinfo=PaymentInfo(),
        )

        return self._database_repository.create_user(user).to_dict()

    def get(self, data):
        return self._database_repository.get_user(data)

    def update(self, username, data):
        password = data["password"]
        email = data["email"]
        return self._database_repository.update_user(username, email, password)

    def update_profile(self, username, data):
        birthday = data["birthday"]
        gender = data["gender"]
        height = data["height"]
        shirt_size = data["shirt_size"]
        jeans_size = data["jeans_size"]
        shoe_size = data["shoe_size"]
        return self._database_repository.update_profile(
            username,
            birthday,
            gender,
            height,
            shirt_size,
            jeans_size,
            shoe_size,
        )

    def update_shippinginfo(self, username, data):
        street = data["street"]
        street_number = data["street_number"]
        zip_code = data["zip_code"]
        city = data["city"]
        return self._database_repository.update_shippinginfo(
            username,
            street,
            street_number,
            zip_code,
            city,
        )

    def update_notificationsettings(self, username, data):
        item_notifications_enabled = data["item_notifications_enabled"]
        bids_notifications_enabled = data["bids_notifications_enabled"]
        chat_notifications_enabled = data["chat_notifications_enabled"]
        news_notifications_enabled = data["news_notifications_enabled"]
        return self._database_repository.update_notificationsettings(
            username,
            item_notifications_enabled,
            bids_notifications_enabled,
            chat_notifications_enabled,
            news_notifications_enabled,
        )

    def update_paymentinfo(self, username, data):
        iban = data["iban"]
        name = data["name"]
        bank = data["bank"]
        return self._database_repository.update_paymentinfo(username, iban, name, bank)

    def block(self, d_username):
        user = self._database_repository.get_user(d_username).to_dict()

        self._pubsub_repository.push(self._pubsub_repository.USER_BLOCKED_TOPIC, user)

    def delete(self, d_username):
        return self._database_repository.delete_user(d_username)
