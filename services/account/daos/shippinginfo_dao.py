from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

from db import Base

class ShippingInfoDAO(Base):
    __tablename__ = 'shippinginfo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    street = Column(String)
    street_number = Column(String)
    zip_code = Column(String)
    city = Column(String)

    def __init__(self, street=None, street_number=None, zip_code=None, city=None):
        self.street = street
        self.street_number = street_number
        self.zip_code = zip_code
        self.city = city
