from marketplace.models import Item


class ItemInteractions:
    def __init__(self, **repositories):
        self._database_repository = repositories["database_repository"]
        self._pubsub_repository = repositories["pubsub_repository"]

    def get(self, item_id):
        return self._database_repository.get_item(int(item_id)).to_dict()

    def getlist(self, user_id):
        return [i.to_dict() for i in self._database_repository.get_itemlist(int(user_id))]

    def search(self, keyword):
        return [i.to_dict() for i in self._database_repository.search_item(keyword)]

    def create(self, body):

        item = Item(
            title=body["title"],
            description=body["description"],
            brand=body["brand"],
            type=body["type"],
            size=body["size"],
            color=body["color"],
            state=body["state"],
            price=body["price"],
            status=body["status"],
            user_id=body["user_id"],
        )

        return self._database_repository.create_item(item).to_dict()

    def update(self, item_id, data):

        title = data["title"]
        description = data["description"]
        brand = data["brand"]
        type = data["type"]
        size = data["size"]
        color = data["color"]
        state = data["state"]
        user_id = data["user_id"]
        price = data["price"]
        status = data["status"]

        return self._database_repository.update_item(
            int(item_id),
            title,
            description,
            brand,
            type,
            size,
            color,
            state,
            int(user_id),
            float(price),
            status,
        ).to_dict()

    def delete(self, item_id):
        return self._database_repository.delete_item(int(item_id))
