from datetime import date
from flask import jsonify
from daos.chat_dao import ChatDAO
from daos.message_dao import MessageDAO
from db import Session

class Message:

    #create a message
    @staticmethod
    def create(d_id, d_message, body):
        session = Session()
        chat = session.query(ChatDAO).filter(ChatDAO.username == d_id)[0]
        chat.message.text = body['text']
        chat.message.date_updated = date.today()
        session.add(chat.message.text)
        session.add(chat.message.date_updated)
        session.commit()
        return jsonify({'message': 'The message was posted'}), 200

    #get a message
    @staticmethod
    def get(d_id):
        session = Session()
        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
        message = session.query(MessageDAO).filter(MessageDAO.id == d_id).first()

        if message:
            text_out = {
                "date_created":message.date_created,
                "text":message.text,
            }
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There is no message with id {d_id}'}), 404