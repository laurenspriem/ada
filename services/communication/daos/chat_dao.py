from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref

from db import Base
from daos.message_dao import MessageDAO
from datetime import date


#DAO for the user table
class UserDAO(Base):
    __tablename__ = 'chat'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_created = Column(DateTime)
    date_updated = Column(DateTime)

    #relationship to messages, one to many
    messages = relationship("Message", back_populates="chat")

    def __init__(self, chat_id, date_created=date.today(), date_updated=None, messages=None):
        self.chat_id = chat_id
        self.date_created = date_created
        self.date_updated = date_updated
        self.messages = messages
