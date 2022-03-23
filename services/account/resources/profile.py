from flask import jsonify
from daos.user_dao import UserDAO
from db import Session

class Profile:

    @staticmethod
    def update(d_username, body):
        session = Session()
        user = session.query(UserDAO).filter(UserDAO.username == d_username)[0]
        user.profile.age = body['age']
        user.profile.height = body['height']
        user.profile.gender = body['gender']
        user.profile.shirt_size = body['shirt_size']
        user.profile.jeans_size = body['jeans_size']
        user.profile.shoe_size = body['shoe_size']
        session.commit()
        return jsonify({'message': 'The profile was updated'}), 200