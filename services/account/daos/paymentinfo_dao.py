from sqlalchemy import Column, String, Integer, DateTime
from db import Base
from datetime import date

#DAO for the payment information
class PaymentInfoDAO(Base):
    __tablename__ = 'paymentinfo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    iban = Column(String)
    name = Column(String)
    bank = Column(String)
    date_created = Column(DateTime)
    date_updated = Column(DateTime)

    def __init__(self, iban=None, name=None, bank=None, date_created=date.today(), date_updated=None):
        self.iban = iban
        self.name = name
        self.bank = bank
        self.date_created = date_created
        self.date_updated = date_updated