from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

from db import Base

class ShippingInformationDAO(Base):
    __tablename__ = 'shippinginformation'
    id = Column(Integer, primary_key=True)
    street = Column(String)
    street_number = Column(String)
    zip_code = Column(String)
    city = Column(String)

    def __init__(self, id, street, street_number, zip_code, city):
        self.id = id
        self.street = street
        self.street_number = street_number
        self.zip_code = zip_code
        self.city = city
