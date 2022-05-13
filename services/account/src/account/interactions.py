from account.models import User, Profile, PaymentInfo, ShippingInfo, NotificationSettings


class AccountInteractions:
    def __init__(self, **repositories):
        self._database_repository = repositories["database_repository"]
        self._pubsub_repository = repositories["pubsub_repository"]
        self._web_repository = repositories["web_repository"]

    # def list(self):
    #     return [m.to_dict() for m in self._database_repository.list_models()]
    #
    # def store(self, data):
    #     model = Model(input=data["input"], output=data["output"])
    #
    #     return self._database_repository.store_model(model).to_dict()

    def create(self, data):
        user = User(username=data["username"], first_name=data["first_name"], last_name=data["last_name"],
                    email=data["email"], password=data["password"], is_verified=data["is_verified"])
        # user.notificationsettings = NotificationSettings(item_notifications_enabled=False, bids_notifications_enabled=False,
        #                                                  chat_notifications_enabled=False, news_notifications_enabled=False)
        # user.shippinginfo = ShippingInfo(street="empty", street_number="empty",
        #                                  zip_code="empty", city="empty")
        # user.paymentinfo = PaymentInfo(iban="empty", name="empty", bank="empty")
        #user.profile = Profile(birthday="empty", gender="empty", height="empty", shirt_size="empty", jeans_size="empty", shoe_size=False)

        return self._database_repository.create_user(user).to_dict()

    def get(self, data):
        return self._database_repository.get_user(data)

    def update(self, username, data):
        password = data["password"]
        email = data["email"]
        return self._database_repository.update_user(username, password, email)

    def update_profile(self,username, data):
        birthday = data["birthday"]
        gender = data["gender"]
        height = data["height"]
        shirt_size = data["shirt_size"]
        jeans_size = data["jeans_size"]
        shoe_size = data["shoe_size"]
        return self._database_repository.update_profile(username, birthday, gender, height, shirt_size, jeans_size, shoe_size)


    def update_shippinginfo(self, username, data):
        street = data["street"]
        street_number = data["street_number"]
        zip_code = data["zip_code"]
        city = data["city"]
        return self._database_repository.update_user(username, street, street_number, zip_code, city)

    def update_notificationsettings(self, username, data):
        item_notifications_enabled = data["item_notifications_enabled"]
        bids_notifications_enabled = data["bids_notifications_enabled"]
        chat_notifications_enabled = data["chat_notifications_enabled"]
        news_notifications_enabled = data["news_notifications_enabled"]
        return self._database_repository.update_user(username, item_notifications_enabled, bids_notifications_enabled, chat_notifications_enabled, news_notifications_enabled)

    def update_paymentinfo(self, username, data):
        iban = data["iban"]
        name = data["name"]
        bank = data["bank"]
        return self._database_repository.update_user(username, iban, name, bank)

    def delete(self, d_username):
        return self._database_repository.delete_user(d_username)

    # def pull(self):
    #     return self._pubsub_repository.pull(self._pubsub_repository.TEST_TOPIC)
    #
    # def push(self, message):
    #     return self._pubsub_repository.push(self._pubsub_repository.TEST_TOPIC, message)

