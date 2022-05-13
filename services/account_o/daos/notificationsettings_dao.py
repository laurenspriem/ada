from sqlalchemy import Column, Integer, Boolean
from db import Base

#DAO for the notification settings
class NotificationSettingsDAO(Base):
    __tablename__ = 'notificationsettings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    item_notifications_enabled = Column(Boolean)
    bids_notifications_enabled = Column(Boolean)
    chat_notifications_enabled = Column(Boolean)
    news_notifications_enabled = Column(Boolean)


    def __init__(self, item_notifications_enabled=True, bids_notifications_enabled=True, chat_notifications_enabled=True, news_notifications_enabled=True):
        self.item_notifications_enabled = item_notifications_enabled
        self.bids_notifications_enabled = bids_notifications_enabled
        self.chat_notifications_enabled = chat_notifications_enabled
        self.news_notifications_enabled = news_notifications_enabled