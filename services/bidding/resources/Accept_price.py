from re import A
from matplotlib.pyplot import title
from flask import jsonify
from db import Session
from daos.bid_dao import BIDDAO

from datetime import datetime
from cmath import nan


class Bid:      
    @staticmethod
    def create(acceptance_price):
        session = Session()
        acceptance_price = BIDDAO(Bid['price'], Bid['status'], Bid['acceptance_price'] datetime.now(), datetime.now()) # klopt dit zo met Bid['price/status/etc']?
        session.add(acceptance_price)
        session.commit()
        session.refresh(acceptance_price)
        session.close()
        return jsonify({'message': f'The is price of the item is accepted {acceptance_price}'}), 404 #bid waar moet deze vandaan komen?

    @staticmethod
    def get(acceptance_price): # moet deze nog aan bid_id gekoppeld worden?
        session = Session()
        a_price = session.query(BIDDAO).filter(BIDDAO.id == acceptance_price.first())

        if a_price:
            status_obj = a_price.status
            text_out = {
                "bid_id": a_price.id,
                "prize": a_price.price,
                "status": a_price.status,
                "date_created": a_price.date_created,
                "date_created": a_price.date_updated,
            }
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There is no price accepted with id {acceptance_price}'}), 404

    @staticmethod
    def update(bid_id, price, status, price_accepted):
        session = Session()
        a_price = session.query(BIDDAO).filter(BIDDAO.id == bid_id).first()
        a_price.price = Bid['price']
        a_price.status = Bid['status']
        a_price.price_accepted = Bid['price_accepted']
        a_price.date_updated = datetime.now()
        session.commit()
        return jsonify({'message': f'The bid acceptance with id {bid_id} is updated'}), 200

