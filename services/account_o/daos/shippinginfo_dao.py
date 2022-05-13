from sqlalchemy import Column, String, Integer, DateTime
from db import Base
from datetime import date

#DAO for the shipping information
class ShippingInfoDAO(Base):
    __tablename__ = 'shippinginfo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    street = Column(String)
    street_number = Column(String)
    zip_code = Column(String)
    city = Column(String)
    date_created = Column(DateTime)
    date_updated = Column(DateTime)

    def __init__(self, street=None, street_number=None, zip_code=None, city=None, date_created=date.today(), date_updated=None):
        self.street = street
        self.street_number = street_number
        self.zip_code = zip_code
        self.city = city
        self.date_created = date_created
        self.date_updated = date_updated
