from huey import crontab

from marketplace.interactions import ItemInteractions
from marketplace.app import worker


def item_interactions():
    return ItemInteractions(**worker.repositories)

@worker.periodic_task(crontab(minute="*"))
def pull_offer_accepted_topic():
    item_interactions().pull_offer_accepted_topic()