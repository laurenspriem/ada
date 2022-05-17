from huey import crontab

from bidding.interactions import BiddingInteractions
from bidding.app import worker


def bidding_interactions():
    return BiddingInteractions(**worker.repositories)


@worker.periodic_task(crontab(minute="*"))
def bidding_subscribe_task():
    bidding_interactions().pull()
