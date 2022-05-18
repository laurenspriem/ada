import sqlalchemy as sa

from bidding.db import Base


class Bid(Base):
    __tablename__ = "bidding"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    price = sa.Column(sa.Integer, nullable=False)
    status = sa.Column(sa.String, nullable=False)
    item_id = sa.Column(sa.Integer, nullable=False)
    user_id = sa.Column(sa.Integer, nullable=False)
    bid_accepted = sa.Column(sa.Boolean, nullable=False)
    price_accepted = sa.Column(sa.Boolean, nullable=False)
    created_on = sa.Column(
        sa.DateTime,
        server_default=sa.func.now(),
    )
    updated_on = sa.Column(
        sa.DateTime,
        server_default=sa.func.now(),
        server_onupdate=sa.func.now(),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "price": self.price,
            "status": self.status,
            "item_id": self.item_id,
            "user_id": self.user_id,
            "bid_accepted": self.bid_accepted,
            "price_accepted": self.price_accepted,
            "created_on": self.created_on.isoformat(),
            "updated_on": self.updated_on.isoformat(),
        }
