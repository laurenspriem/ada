from matplotlib.pyplot import title
from flask import jsonify
from db import Session
from daos.bid_dao import BidDAO

from datetime import datetime
from cmath import nan


class Bid:
    @staticmethod
    def create(body):
        session = Session()
        # Add here the condition of the bid must be higher than the previous bid?
        # Add here that the bid must be higher than the minimum assigned value of a product
        bid = BidDAO(body['price'], body['status'])
        session.add(bid)
        session.commit()
        session.refresh(bid)
        session.close()
        return jsonify({'item_id': bid.id}), 200
        
    @staticmethod
    def update(d_bid_id, body):
        session = Session()
        bid = session.query(BidDAO).filter(BidDAO.id == d_bid_id)
        bid.price = body['price']
        bid.status = body['status']
        bid.date_updated = datetime.now()
        session.commit()
        return jsonify({'message': f'The bid with id {d_bid_id} is updated'}), 200

    @staticmethod
    def get(d_bid_id):
        session = Session()
        bid = session.query(BidDAO).filter(BidDAO.id == d_bid_id).first()

        if bid:
            text_out = {
                "bid_id": bid.id,
                "prize": bid.price,
                "status": bid.status,
                "date_created": bid.date_created,
                "date_created": bid.date_updated,
            }
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There is no bid for this item yet {d_bid_id}'}), 404

    @staticmethod
    def delete(d_bid_id):
        session = Session()
        effected_rows = session.query(BidDAO).filter(BidDAO.id == d_bid_id).delete()
        session.commit()
        session.close()
        if effected_rows == 0:
            return jsonify({'message': f'There is no bid with id {d_bid_id}'}), 404
        else:
            return jsonify({'message': 'The bid is removed'}), 200