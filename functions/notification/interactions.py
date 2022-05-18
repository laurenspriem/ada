class NotificationInteractions:
    def __init__(self, notification_repository):
        self._notification_repository = notification_repository

    def send_notification(self, topic, data):
        if topic == "jads-adaassignment-item-update":
            message = f"{topic}: item {data['id']} updated"
        elif topic == "jads-adaassignment-message-send":
            message = f"{topic}: message {data['id']} send"
        elif topic == "jads-adaassignment-offer-accepted":
            message = f"{topic}: bid {data['id']} for item {data['item_id']} by user {data['user_id']} accepted"
        elif topic == "jads-adaassignment-user-blocked":
            message = f"{topic}: user {data['id']} blocked"
        else:
            message = f"{topic}: unknown topic."

        self._notification_repository.send_notification(message)
