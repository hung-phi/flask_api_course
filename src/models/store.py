from src.db import db
from src.models.db_action import DBAction


class StoreModel(db.Model, DBAction):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def jsonify(self):
        return {'name': self.name, 'items': [item.jsonify() for item in self.items]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

