from flask import jsonify

from daos.user_dao import UserDAO
from daos.notificationsettings_dao import NotificationSettingsDAO
from daos.profile_dao import ProfileDAO
from daos.shippinginfo_dao import ShippingInfoDAO
from daos.paymentinfo_dao import PaymentInfoDAO

from db import Session

class User:

    #create a user
    @staticmethod
    def create(body):
        session = Session()
        user = UserDAO(body['username'], body['first_name'], body['last_name'], body['email'],
                       body['password'], body['is_verified'], ProfileDAO(), NotificationSettingsDAO(), ShippingInfoDAO(),
                       PaymentInfoDAO())
        session.add(user)
        session.commit()
        session.refresh(user)
        session.close()
        return jsonify({'username': user.username}), 200

    #get a user
    @staticmethod
    def get(d_username):
        session = Session()
        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
        user = session.query(UserDAO).filter(UserDAO.username == d_username).first()

        if user:
            shippinginformation_obj = user.shippinginfo
            paymentinformation_obj = user.paymentinfo
            profile_obj = user.profile
            notificationsettings_obj = user.notificationsettings
            text_out = {
                "username:": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "is_verified": user.is_verified,
                "shipping info": {
                    "street": shippinginformation_obj.street,
                    "street_number": shippinginformation_obj.street_number,
                    "zip_code": shippinginformation_obj.zip_code,
                    "city": shippinginformation_obj.city
                },
                "payment info": {
                    "iban": paymentinformation_obj.iban,
                    "name": paymentinformation_obj.name,
                    "bank": paymentinformation_obj.bank
                },
                "notification settings": {
                    "item_notifications_enabled": notificationsettings_obj.item_notifications_enabled,
                    "bids_notifications_enabled": notificationsettings_obj.bids_notifications_enabled,
                    "chat_notifications_enabled": notificationsettings_obj.chat_notifications_enabled,
                    "news_notifications_enabled": notificationsettings_obj.news_notifications_enabled
                },
                "profile" : {
                    "birthday": profile_obj.birthday,
                    "gender": profile_obj.gender,
                    "height": profile_obj.height,
                    "shirt_size": profile_obj.shirt_size,
                    "jeans_size": profile_obj.jeans_size,
                    "shoe_size": profile_obj.shoe_size
                }
            }
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There is no user with id {d_username}'}), 404

    #update user information
    @staticmethod
    def update(d_username, body):
        session = Session()
        user = session.query(UserDAO).filter(UserDAO.username == d_username)[0]
        user.email = body['email']
        user.password = body['password']
        session.commit()
        return jsonify({'message': 'The user information was updated'}), 200

    #delete a user
    @staticmethod
    def delete(d_username):
        session = Session()
        effected_rows = session.query(UserDAO).filter(UserDAO.username == d_username).delete()
        session.commit()
        session.close()
        if effected_rows == 0:
            return jsonify({'message': f'There is no user with id {d_username}'}), 404
        else:
            return jsonify({'message': 'The user was removed'}), 200