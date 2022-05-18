from huey import crontab

from communication.interactions import CommunicationInteractions
from communication.app import worker


def communication_interactions():
    return CommunicationInteractions(**worker.repositories)


@worker.periodic_task(crontab(minute="*"))
def pull_item_update_topic():
    communication_interactions().pull_item_update_topic()


@worker.periodic_task(crontab(minute="*"))
def pull_offer_accepted_topic():
    communication_interactions().pull_offer_accepted_topic()


@worker.periodic_task(crontab(minute="*"))
def pull_user_blocked_topic():
    communication_interactions().pull_user_blocked_topic()
