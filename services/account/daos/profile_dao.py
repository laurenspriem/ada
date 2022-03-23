from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

from db import Base

class ProfileDAO(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True, autoincrement = True)
    age = Column(Integer)
    gender = Column(String)
    height = Column(Integer)
    shirt_size = Column(String)
    jeans_size = Column(String)
    shoe_size = Column(Integer)

    def __init__(self, age=None, gender=None, height=None, shirt_size=None, jeans_size=None, shoe_size=None):
        self.age = age
        self.gender = gender
        self.height = height
        self.shirt_size = shirt_size
        self.jeans_size = jeans_size
        self.shoe_size = shoe_size