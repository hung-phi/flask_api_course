from src.db import db
from src.models.db_action import DBAction
from src.constants import *


class ItemModel(db.Model, DBAction):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(ITEM_NAME_LENGTH))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def jsonify(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
