from flask import jsonify
from daos.user_dao import UserDAO
from db import Session

class NotificationSettings:

    #update the notification settings
    @staticmethod
    def update(d_username, body):
        session = Session()
        user = session.query(UserDAO).filter(UserDAO.username == d_username)[0]
        user.notificationsettings.item_notifications_enabled = body['item_notifications_enabled']
        user.notificationsettings.bids_notifications_enabled = body['bids_notifications_enabled']
        user.notificationsettings.chat_notifications_enabled = body['chat_notifications_enabled']
        user.notificationsettings.news_notifications_enabled = body['news_notifications_enabled']

        session.commit()
        return jsonify({'message': 'The shipping information was updated'}), 200