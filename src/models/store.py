from src.db import db
from src.models.db_action import DBActionMixin
from src.constants import *


class StoreModel(db.Model, DBActionMixin):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(STORE_NAME_LENGTH))

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def jsonify(self):
        return {'name': self.name, 'items': [item.jsonify() for item in self.items]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
