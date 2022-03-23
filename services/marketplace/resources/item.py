from matplotlib.pyplot import title
from flask import jsonify
from db import Session
from services.user.daos.item_dao import ItemDAO

from datetime import datetime
from cmath import nan


class Item:
    @staticmethod
    def create(body):
        session = Session()
        item = ItemDAO(body['title'], body['description'], body['brand'], body['type'], body['size'],
            body['color'], body['state'], body['price'], body['status'], datetime.now(), nan)
        session.add(item)
        session.commit()
        session.refresh(item)
        session.close()
        return jsonify({'item_id': item.id}), 200

    @staticmethod
    def get(item_id):
        session = Session()
        item = session.query(ItemDAO).filter(ItemDAO.id == item_id).first()

        if item:
            status_obj = item.status
            text_out = {
                "item_id": item.id,
                "title": item.title,
                "description": item.description,
                "brand": item.brand,
                "type": item.type,
                "size": item.size,
                "color": item.color,
                "state": item.state,
                "prize": item.price,
                "status": item.status,
                "date_created": item.date_created,
                "date_created": item.date_updated,
            }
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There is no item with id {item_id}'}), 404

    @staticmethod
    def update(item_id, title, description, brand, type, size, color, state, price, status):
        session = Session()
        item = session.query(ItemDAO).filter(ItemDAO.id == item_id).first()
        item.title = title
        item.description = description
        item.brand = brand
        item.type = type
        item.size = size
        item.color = color
        item.state = state
        item.price = price
        item.status = status
        item.date_updated = datetime.now()
        session.commit()
        return jsonify({'message': f'The item information with id {item_id} is updated'}), 200

    @staticmethod
    def delete(item_id):
        session = Session()
        effected_rows = session.query(ItemDAO).filter(ItemDAO.id == item_id).delete()
        session.commit()
        session.close()
        if effected_rows == 0:
            return jsonify({'message': f'There is no delivery with id {item_id}'}), 404
        else:
            return jsonify({'message': 'The item is removed'}), 200