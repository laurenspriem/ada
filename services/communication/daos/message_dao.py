from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref

from db import Base
from datetime import date


#DAO for the user table
class MessageDAO(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_created = Column(DateTime)
    text = Column(String)

    #relationship to messages, one to many
    messages = relationship("Message", back_populates="chat")
    chat_id = Column(Integer, ForeignKey('chat.id'))
    chat = relationship("Chat", back_populates="messages")

    def __init__(self, chat_id, date_created=date.today(), text=None):
        self.chat_id = chat_id
        self.date_created = date_created
        self.text = text