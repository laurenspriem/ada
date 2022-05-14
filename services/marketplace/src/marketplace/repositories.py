from matplotlib.pyplot import title
from flask import jsonify
import json
from db import Session

from datetime import date
from cmath import nan


from google.api_core.exceptions import AlreadyExists
from marketplace.models import Item

class ItemDatabaseRepository:
    def __init__(self, session):
        self._session = session

    def create_item(self, item ):#Create item
        
        #item = ItemDAO(body['title'], body['description'], body['brand'], body['type'], body['size'],
        #    body['color'], body['state'], body['price'], body['status'],body['user_id'], date.today(), None)
        self._session.add(item)
        self._session.commit()
        self._session.refresh(item)
        
        return item # jsonify({'item_id': item.id}), 200

    def get_item(self, d_item_id):#Retrieve information of specific item of certain user
        
        item = self._session.query(Item).filter(Item.id == d_item_id).first()
        return item
        
        # if item:
        #     #status_obj = item.status
        #     text_out = {
        #         "item_id": item.id,
        #         "title": item.title,
        #         "description": item.description,
        #         "brand": item.brand,
        #         "type": item.type,
        #         "size": item.size,
        #         "color": item.color,
        #         "state": item.state,
        #         "prize": item.price,
        #         "status": item.status,
        #         "user_id": item.user_id,
        #         "date_created": item.date_created,
        #         "date_updated": item.date_updated,
        #     }
            
        #     return jsonify(text_out), 200
        # else:
            
        #     return jsonify({'message': f'There is no item with id {item_id}'}), 404

    def update_item(self, d_item_id, d_title, d_description, d_brand, d_type, d_size, d_color, d_state, d_user_id, d_price, d_status):#Edit item of certain user
        
        item = self.get_item(d_item_id)

        item.title = d_title
        item.description = d_description
        item.brand = d_brand
        item.type = d_type
        item.size = d_size
        item.color = d_color
        item.state = d_state
        item.user_id = d_user_id
        item.price = d_price
        item.status = d_status
        item.date_updated = date.today().isoformat()

        self._session.commit()
        return item
        
        #return jsonify({'message': f'The item information with id {item_id} is updated'}), 200

    def delete_item(self, d_item_id):#Delete item of certain user
        
        self._session.query(Item).filter(Item.id == d_item_id).delete()
        session.commit()
        return d_item_id
        
        # if effected_rows == 0:
        #     return jsonify({'message': f'There is no item with id {item_id}'}), 404
        # else:
        #     return jsonify({'message': 'The item is removed'}), 200


    def get_itemlist(self, d_user_id):#Retrieve all listed items of certain user
        
        items = self._session.query(Item).filter(Item.user_id == d_user_id).all()
        itemlist = [item.id for item in items]
        return itemlist
        
        # if items:
        #     itemlist = [item.id for item in items] # list comprehension
        #     itemjson = json.dumps(itemlist) # from python list to json string
            
        #     return itemjson, 200
        # else:
            
        #     return jsonify({'message': f'User with id {user_id} has no items'}), 404

    def search_item(self, d_keyword):#Search in marketplace on keywords for listed items matching keywords
        
        items = self._session.query(Item).filter(Item.description.contains(d_keyword)).all()
        itemlist = [item.id for item in items]
        return itemlist

        # if items:
        #     itemlist = [item.id for item in items]
        #     itemjson = json.dumps(itemlist) # from python list to json string
            
        #     return itemjson, 200
        # else:
            
        #     return jsonify({'message': f'There is no item with keyword {keyword}'}), 404