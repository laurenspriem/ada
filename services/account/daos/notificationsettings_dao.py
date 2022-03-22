from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

from db import Base

class NotificationSettingsDAO(Base):
    __tablename__ = 'notificationsettings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    item_notifications_enabled = Column(Boolean)
    bids_notifications_enabled = Column(Boolean)
    chat_notifications_enabled = Column(Boolean)
    news_notifications_enabled = Column(Boolean)


    def __init__(self, id, item_notifications_enabled, bids_notifications_enabled, chat_notifications_enabled, news_notifications_enabled):
        self.id = id
        self.item_notifications_enabled = item_notifications_enabled
        self.bids_notifications_enabled = bids_notifications_enabled
        self.chat_notifications_enabled = chat_notifications_enabled
        self.news_notifications_enabled = news_notifications_enabled