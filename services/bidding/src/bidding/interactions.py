from bidding.models import Bid


class BiddingInteractions:
    def __init__(self, **repositories):
        self._database_repository = repositories["database_repository"]
        self._pubsub_repository = repositories["pubsub_repository"]

    def create_bid(self, data):
        bid = Bid(
            item_id=data["item_id"],
            user_id=data["user_id"],
            price=data["price"],
            status=data["status"],
            bid_accepted=data["bid_accepted"],
            price_accepted=data["price_accepted"],
        )

        bid = self._database_repository.create_bid(bid).to_dict()
        if bid["bid_accepted"]:
            self._pubsub_repository.push(
                self._pubsub_repository.OFFER_ACCEPTED_TOPIC,
                bid,
            )

        return bid

    def get_bid(self, data):
        return self._database_repository.get_bid(int(data)).to_dict()

    def update_bid(self, id, data):
        price = data["price"]
        status = data["status"]
        bid_accepted = data["bid_accepted"]
        price_accepted = data["price_accepted"]

        bid = self._database_repository.update_bid(
            int(id),
            price,
            status,
            bid_accepted,
            price_accepted,
        ).to_dict()

        if bid["bid_accepted"]:
            self._pubsub_repository.push(
                self._pubsub_repository.OFFER_ACCEPTED_TOPIC,
                bid,
            )

        return bid

    def delete_bid(self, d_id):
        return self._database_repository.delete_bid(int(d_id))
