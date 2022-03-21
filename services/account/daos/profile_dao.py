from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

from db import Base
from daos.user_dao import UserDAO

class ProfileDAO(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
    age = Column(String)
    gender = Column(String)
    height = Column(Integer)
    shirt_size = Column(Integer)
    jeans_size = Column(Integer)
    shoe_size = Column(Integer)

    def __init__(self, id, age, gender, height, shirt_size, jeans_size, shoe_size):
        self.id = id
        self.age = age
        self.gender = gender
        self.height = height
        self.shirt_size = shirt_size
        self.jeans_size = jeans_size
        self.shoe_size = shoe_size