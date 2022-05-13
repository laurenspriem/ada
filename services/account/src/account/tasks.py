from huey import crontab

from account.interactions import AccountInteractions
from account.app import worker


def example_interactions():
    return AccountInteractions(**worker.repositories)


@worker.periodic_task(crontab(minute="*"))
def example_subscribe_task():
    example_interactions().pull()
