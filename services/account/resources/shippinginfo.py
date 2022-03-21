from flask import jsonify
from daos.user_dao import UserDAO
from db import Session

class ShippingInfo:

    @staticmethod
    def update(d_username, street, street_number, zip_code, city):
        session = Session()
        user = session.query(UserDAO).filter(UserDAO.username == d_username)[0]
        user.shippinginfo.street = street
        user.shippinginfo.street_number = street_number
        user.shippinginfo.zip_code = zip_code
        user.shippinginfo.city = city
        session.commit()
        return jsonify({'message': 'The shipping information was updated'}), 200