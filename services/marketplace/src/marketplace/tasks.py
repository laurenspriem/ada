from marketplace.interactions import ItemInteractions
from marketplace.app import worker


def item_interactions():
    return ItemInteractions(**worker.repositories)
