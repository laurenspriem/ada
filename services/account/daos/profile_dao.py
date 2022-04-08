from sqlalchemy import Column, String, Integer
from db import Base

#DAO for the profile
class ProfileDAO(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True, autoincrement = True)
    birthday = Column(String)
    gender = Column(String)
    height = Column(Integer)
    shirt_size = Column(String)
    jeans_size = Column(String)
    shoe_size = Column(Integer)

    def __init__(self, birthday=None, gender=None, height=None, shirt_size=None, jeans_size=None, shoe_size=None):
        self.birthday = birthday
        self.gender = gender
        self.height = height
        self.shirt_size = shirt_size
        self.jeans_size = jeans_size
        self.shoe_size = shoe_size