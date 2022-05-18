# pylint: disable=global-statement
import base64
import json

from repositories import NotificationPrintRepository
from interactions import NotificationInteractions


notification_repository = None


def _connect_notification():
    global notification_repository

    if not notification_repository:
        # Create repository
        notification_repository = NotificationPrintRepository()


def pull_item_update_topic(event, context):
    interactions = NotificationInteractions(notification_repository)

    topic = context.event_id
    data = json.loads(base64.b64decode(event["data"]).decode("utf-8"))

    return interactions.send_notification(topic, data)


def pull_message_send_topic(event, context):
    interactions = NotificationInteractions(notification_repository)

    topic = context.event_id
    data = json.loads(base64.b64decode(event["data"]).decode("utf-8"))

    return interactions.send_notification(topic, data)


def pull_offer_accepted_topic(event, context):
    interactions = NotificationInteractions(notification_repository)

    topic = context.event_id
    data = json.loads(base64.b64decode(event["data"]).decode("utf-8"))

    return interactions.send_notification(topic, data)


def pull_user_blocked_topic(event, context):
    interactions = NotificationInteractions(notification_repository)

    topic = context.event_id
    data = json.loads(base64.b64decode(event["data"]).decode("utf-8"))

    return interactions.send_notification(topic, data)


if __name__ == "main":
    _connect_notification()
