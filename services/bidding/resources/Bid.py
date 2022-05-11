from matplotlib.pyplot import title
from flask import jsonify
from db import Session
from daos.bid_dao import BIDDAO

from datetime import datetime
from cmath import nan


class Bid:
    @staticmethod
    def create(bid_id):
        session = Session()
        bid_id = BIDDAO(Bid['price'], datetime.now(), datetime.now()) # klopt dit dat deze gelinkt is aan de item_id?
        # Add here the condition of the bid must be higher than the previous bid?
        # Add here that the bid must be higher than the minimum assigned value of a pro
        bid_id.add(bid_id)
        bid_id.commit()
        bid_id.refresh(bid_id)
        bid_id.close()
        return jsonify({'item_id': Bid.id}, bid_id), 200
        
    @staticmethod
    def update(bid_id):
        session = Session()
        bid_id = session.query(BIDDAO).filter(BIDDAO.id == bid_id).first()
        bid_id.price = Bid['price']
        bid_id.status = Bid['status']
        bid_id.date_updated = datetime.now()
        session.commit()
        return jsonify({'message': f'The bid price with id {bid_id} is updated'}), 200

    @staticmethod
    def get(bid_id):
        session = Session()
        bid = session.query(BIDDAO).filter(BIDDAO.id == bid_id).first()

        if bid:
            status_obj = bid_id.status
            text_out = {
                "item_id": bid_id.id,
                "prize": bid_id.price,
                "status": bid_id.status,
                "date_created": bid_id.date_created,
                "date_created": bid_id.date_updated,
            }
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There is no bid for this item yet {bid_id}'}), 404

    @staticmethod
    def delete(bid_id):
        session = Session()
        effected_rows = session.query(BIDDAO).filter(BIDDAO.id == bid_id).delete()
        session.commit()
        session.close()
        if effected_rows == 0:
            return jsonify({'message': f'There is no bid with id {bid_id}'}), 404
        else:
            return jsonify({'message': 'The bid is removed'}), 200