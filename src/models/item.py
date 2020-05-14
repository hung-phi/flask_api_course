from src.db import db
from src.models.db_action import DBActionMixin
from src.constants import *


class ItemModel(db.Model, DBActionMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(ITEM_NAME_LENGTH), unique=True)
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, **kwargs):
        super(ItemModel, self).__init__(**kwargs)

    def jsonify(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
