import sqlalchemy as sa
from marketplace.db import Base

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float
from datetime import datetime, date





class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    brand = Column(String, nullable=True)
    type = Column(String, nullable=True)
    size = Column(String, nullable=True)
    color = Column(String, nullable=True)
    state = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String, nullable=False)                 # I do not know what we mean by status
    user_id = Column(Integer, nullable=False)
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