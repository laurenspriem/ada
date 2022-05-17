from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float
from db import Base
from datetime import datetime, date


class ItemDAO(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    brand = Column(String)
    type = Column(String)
    size = Column(String)
    color = Column(String)
    state = Column(String)
    price = Column(Float)
    status = Column(String)                 # I do not know what we mean by status
    user_id = Column(Integer)
    date_created = Column(DateTime)
    date_updated = Column(DateTime)

    def __init__(self, title=None, description=None, brand=None, type=None, size=None, color=None, state=None, price=None, status=None, user_id=None, date_created=date.today(), date_updated=None):
        self.title = title
        self.description = description
        self.brand = brand
        self.type = type
        self.size = size
        self.color = color
        self.state = state
        self.price = price
        self.status = status
        self.user_id = user_id
        self.date_created = date_created    # Is set to current time in item.py
        self.date_updated = date_updated    # Is initialized as nan in item.py