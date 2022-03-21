from flask import jsonify
from daos.user_dao import UserDAO
from db import Session

class Profile:

    @staticmethod
    def update(d_username, age, height, shirt_size, jeans_size, shoe_size):
        session = Session()
        user = session.query(UserDAO).filter(UserDAO.username == d_username)[0]
        user.profile.age = age
        user.profile.height = height
        user.profile.shirt_size = shirt_size
        user.profile.jeans_size = jeans_size
        user.profile.shoe_size = shoe_size
        session.commit()
        return jsonify({'message': 'The profile was updated'}), 200