from flask import jsonify

from daos.chat_dao import ChatDAO
from daos.message_dao import MessageDAO

from db import Session

class User:

    #create a chat
    @staticmethod
    def create(body):
        session = Session()
        chat = ChatDAO(MessageDAO())
        session.add(chat)
        session.commit()
        session.refresh(chat)
        session.close()
        return jsonify({'chat': chat.id}), 200

    #get a chat
    @staticmethod
    def get(d_id):
        session = Session()
        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
        chat = session.query(ChatDAO).filter(ChatDAO.id == d_id).first()

        if chat:
            message_obj = chat.message
            text_out = {
                "id":chat.id,
                "date_created":chat.date_created,
                "date_update":chat.date_updated,
                "messages":chat.message,
            }
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There is no chat with id {d_id}'}), 404

    #delete a chat
    @staticmethod
    def delete(d_id):
        session = Session()
        effected_rows = session.query(ChatDAO).filter(ChatDAO.id == d_id).delete()
        session.commit()
        session.close()
        if effected_rows == 0:
            return jsonify({'message': f'There is no chat with id {d_id}'}), 404
        else:
            return jsonify({'message': 'The chat was removed'}), 200