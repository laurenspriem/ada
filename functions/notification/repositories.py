import logging

log = logging.getLogger(__name__)


class NotificationPrintRepository:
    def __init__(self):
        pass

    def send_notification(self, message):
        log.info(message)
