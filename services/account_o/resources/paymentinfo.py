from datetime import date
from flask import jsonify
from daos.user_dao import UserDAO
from db import Session

class PaymentInfo:

    #update the payment information of the user
    @staticmethod
    def update(d_username, body):
        session = Session()
        user = session.query(UserDAO).filter(UserDAO.username == d_username)[0]
        user.paymentinfo.iban = body['iban']
        user.paymentinfo.name = body['name']
        user.paymentinfo.bank = body['bank']
        user.paymentinfo.date_updated = date.today()
        
        session.commit()
        return jsonify({'message': 'The payment information was updated'}), 200