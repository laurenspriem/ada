from flask import jsonify
from daos.user_dao import UserDAO
from db import Session

class NotificationSettings:

    @staticmethod
    def update(d_username, item_not, bids_not, chat_not, news_not):
        session = Session()
        user = session.query(UserDAO).filter(UserDAO.username == d_username)[0]
        user.notificationsettings.item_notifications_enabled = item_not
        user.notificationsettings.bids_notifications_enabled = bids_not
        user.notificationsettings.chat_notifications_enabled = chat_not
        user.notificationsettings.news_notifications_enabled = news_not

        session.commit()
        return jsonify({'message': 'The shipping information was updated'}), 200