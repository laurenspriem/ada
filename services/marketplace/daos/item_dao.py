from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float
from db import Base
from datetime import datetime


class ItemDAO(Base):
    __tablename__ = 'Marketplace'
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
    date_created = Column(DateTime)
    date_updated = Column(DateTime)

    def __init__(self, title, description, brand, type, size, color, state, price, status, date_created, date_updated):
        self.title = title
        self.description = description
        self.brand = brand
        self.type = type
        self.size = size
        self.color = color
        self.state = state
        self.price = price
        self.status = status
        self.date_created = date_created    # Is set to current time in item.py
        self.date_updated = date_updated    # Is initialized as nan in item.py