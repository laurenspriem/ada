from flask import jsonify
from daos.user_dao import UserDAO
from db import Session

class ShippingInfo:

    #update the shipping information of the user
    @staticmethod
    def update(d_username, body):
        session = Session()
        user = session.query(UserDAO).filter(UserDAO.username == d_username)[0]
        user.shippinginfo.street = body['street']
        user.shippinginfo.street_number = body['street_number']
        user.shippinginfo.zip_code = body['zip_code']
        user.shippinginfo.city = body['city']

        session.commit()
        return jsonify({'message': 'The shipping information was updated'}), 200