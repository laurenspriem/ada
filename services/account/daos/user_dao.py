from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

from db import Base
from daos.notificationsettings_dao import NotificationSettingsDAO
from daos.profile_dao import ProfileDAO
from daos.shippinginfo_dao import ShippingInfoDAO

class UserDAO(Base):
    __tablename__ = 'user'
    username = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    is_verified = Column(Boolean)
    # reference to status as foreign key relationship. This will be automatically assigned.
    #profile_id = Column(Integer, ForeignKey('profile.id'))
    #shippinginfo_id = Column(Integer, ForeignKey('shippinginfo.id'))
    #notificationsettings_id = Column(Integer, ForeignKey('notificationsettings.id'))
    # https: // docs.sqlalchemy.org / en / 14 / orm / basic_relationships.html
    # https: // docs.sqlalchemy.org / en / 14 / orm / backref.html
    #profile = relationship(ProfileDAO.__name__, foreign_keys=[username], backref="user")
    #shippinginfo = relationship(ShippingInfoDAO.__name__, foreign_keys=[username], backref="user")
    #notificationsettings = relationship(NotificationSettingsDAO.__name__, foreign_keys=[username], backref="user")
    profile_id = Column(Integer, ForeignKey('profile.id'))
    profile = relationship(ProfileDAO.__name__, backref=backref("user", uselist=False))

    notificationsettings_id = Column(Integer, ForeignKey('notificationsettings.id'))
    notificationsettings = relationship(NotificationSettingsDAO.__name__, backref=backref("user", uselist=False))

    shippinginfo_id = Column(Integer, ForeignKey('shippinginfo.id'))
    shippinginfo = relationship(ShippingInfoDAO.__name__, backref=backref("user", uselist=False))

    def __init__(self, username, first_name, last_name, email, password, is_verified, profile, shippinginfo, notifcationsettings):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_verified = is_verified
        self.profile = profile
        self.shippinginfo = shippinginfo
        self.notificationsettings = notifcationsettings

