import sqlalchemy as sa
from marketplace.db import Base


class Item(Base):
    __tablename__ = "item"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=True)
    brand = sa.Column(sa.String, nullable=True)
    type = sa.Column(sa.String, nullable=True)
    size = sa.Column(sa.String, nullable=True)
    color = sa.Column(sa.String, nullable=True)
    state = sa.Column(sa.String, nullable=False)
    price = sa.Column(sa.Float, nullable=False)
    status = sa.Column(sa.String, nullable=False)
    user_id = sa.Column(sa.Integer, nullable=False)
    date_created = sa.Column(
        sa.DateTime,
        server_default=sa.func.now(),
    )
    date_updated = sa.Column(
        sa.DateTime,
        server_default=sa.func.now(),
        server_onupdate=sa.func.now(),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "brand": self.brand,
            "type": self.type,
            "size": self.size,
            "color": self.color,
            "state": self.state,
            "price": self.price,
            "status": self.status,
            "user_id": self.user_id,
            "date_created": self.date_created.isoformat(),
            "date_updated": self.date_updated.isoformat(),
        }
