from huey import crontab

from marketplace.interactions import ExampleInteractions
from marketplace.app import worker


def example_interactions():
    return ExampleInteractions(**worker.repositories)


@worker.periodic_task(crontab(minute="*"))
def example_subscribe_task():
    example_interactions().pull()
