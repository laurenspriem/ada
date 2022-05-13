from huey import crontab

from template.interactions import ExampleInteractions
from template.app import worker


def example_interactions():
    return ExampleInteractions(**worker.repositories)


@worker.periodic_task(crontab(minute="*"))
def example_subscribe_task():
    example_interactions().pull()
