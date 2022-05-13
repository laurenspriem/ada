from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

from db import Base
from daos.notificationsettings_dao import NotificationSettingsDAO
from daos.profile_dao import ProfileDAO
from daos.shippinginfo_dao import ShippingInfoDAO
from daos.paymentinfo_dao import PaymentInfoDAO

#DAO for the user table
class UserDAO(Base):
    __tablename__ = 'user'
    username = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    is_verified = Column(Boolean)

    #relationship to profile
    profile_id = Column(Integer, ForeignKey('profile.id'))
    profile = relationship(ProfileDAO.__name__, backref=backref("user", uselist=False))

    #relationship to notification settings
    notificationsettings_id = Column(Integer, ForeignKey('notificationsettings.id'))
    notificationsettings = relationship(NotificationSettingsDAO.__name__, backref=backref("user", uselist=False))

    #relationship to shipping information
    shippinginfo_id = Column(Integer, ForeignKey('shippinginfo.id'))
    shippinginfo = relationship(ShippingInfoDAO.__name__, backref=backref("user", uselist=False))

    #relationship to payment information
    paymentinfo_id = Column(Integer, ForeignKey('paymentinfo.id'))
    paymentinfo = relationship(PaymentInfoDAO.__name__, backref=backref("user", uselist=False))

    def __init__(self, username, first_name, last_name, email, password, is_verified, profile, notifcationsettings,
                 shippinginfo, paymentinfo):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_verified = is_verified
        self.profile = profile
        self.notificationsettings = notifcationsettings
        self.shippinginfo = shippinginfo
        self.paymentinfo = paymentinfo

