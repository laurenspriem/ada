from huey import crontab

from bidding.interactions import ExampleInteractions
from bidding.app import worker


def example_interactions():
    return ExampleInteractions(**worker.repositories)


@worker.periodic_task(crontab(minute="*"))
def example_subscribe_task():
    example_interactions().pull()
