from marketplace.models import Item


class ItemInteractions:
    def __init__(self, **repositories):
        self._database_repository = repositories["database_repository"]
        self._pubsub_repository = repositories["pubsub_repository"]
        #self._web_repository = repositories["web_repository"]

    def create(self, body):

        item = Item(
            title=body['title'],
            description=body['description'],
            brand=body['brand'],
            type=body['type'],
            size=body['size'],
            color=body['color'],
            state=body['state'],
            price=body['price'],
            status=body['status'],
            user_id=body['user_id']
            )
        
        return self._database_repository.create_item(item).to_dict()

    def get(self, item_id):
        return self._database_repository.get_item(item_id)

    def update(self, item_id, data):

        title=data["title"]
        description=data["description"]
        brand=data["brand"]
        type=data["type"]
        size=data["size"]
        color=data["color"]
        state=data["state"]
        user_id=data["user_id"]
        price=data["price"]
        status=data["status"]

        return self._database_repository.update_item(item_id, title, description, brand, type, size, color, state, user_id, price, status)

    def delete(self, item_id):
        return self._database_repository.delete_item(item_id)

    def getlist(self, user_id):
        return self._database_repository.get_itemlist(user_id)

    def search(self, keyword):
        return self._database_repository.search_item(keyword)

