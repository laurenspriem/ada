from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float, Boolean
from db import Base
from datetime import date


class BidDAO(Base):
    __tablename__ = 'Bidding'
    id = Column(Integer, primary_key=True, autoincrement=True) 
    price = Column(Float)
    status = Column(String)                 # I do not know what we mean by status
    date_created = Column(DateTime)
    date_updated = Column(DateTime)
    bid_accepted = Column(Boolean)
    price_accepted = Column(Boolean)

    def __init__(self, price, status, date_created=date.today(), date_updated=date.today(), bid_accepted=False, price_accepted=False):
        self.price = price
        self.status = status
        self.date_created = date_created    # Is set to current time in item.py
        self.date_updated = date_updated    # Is initialized as nan in item.py
        self.bid_accepted = bid_accepted
        self.price_accepted = price_accepted