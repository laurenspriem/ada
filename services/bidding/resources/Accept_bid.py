from re import A
from matplotlib.pyplot import title
from flask import jsonify
from db import Session
from daos.bid_dao import BIDDAO

from datetime import datetime
from cmath import nan


class Bid:
    @staticmethod
    def create(acceptance_bid):
        session = Session()
        acceptance_bid = BIDDAO(Bid['price'], Bid['status'], datetime.now(), datetime.now(), Bid['acceptance_bid']) # klopt dit zo met Bid['price/status/etc']?
        session.add(acceptance_bid)
        session.commit()
        session.refresh(acceptance_bid)
        session.close()
        return jsonify({'message': f'The bid is accepted {acceptance_bid}'}), 404 #bid waar moet deze vandaan komen?


    @staticmethod
    def get(acceptance_bid): # moet deze nog aan bid_id gekoppeld worden?
        session = Session()
        a_bid = session.query(BIDDAO).filter(BIDDAO.id == acceptance_bid).first()

        if a_bid:
            status_obj = a_bid.status
            text_out = {
                "item_id": a_bid.id,
                "prize": a_bid.price,
                "status": a_bid.status,
                "date_created": a_bid.date_created,
                "date_created": a_bid.date_updated,
            }
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There is no bid accepted with id {acceptance_bid}'}), 404

    @staticmethod
    def update(bid_id, body, price):
        session = Session()
        a_bid = session.query(BIDDAO).filter(BIDDAO.id == bid_id).first()
        a_bid.price = body['price']
        a_bid.status = body['status']
        a_bid.date_updated = datetime.now()
        session.commit()
        return jsonify({'message': f'The accepted price with id {bid_id} is updated'}), 200