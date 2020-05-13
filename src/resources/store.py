from flask_restful import Resource

from src.models.store import StoreModel
from src.models.item import ItemModel
from src.error import *


class Store(Resource):
    @staticmethod
    def get(name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.jsonify()
        return {'message': 'store with name {} not found'.format(name)}, 404

    @staticmethod
    def post(name):
        store = StoreModel.find_by_name(name)
        if store:
            return {'message': 'store with name {} has existed'.format(name)}, 400
        store = StoreModel(name)
        safe_run(message='error while creating store with name {}'.format(name),
                 error_code=500)(store.save_to_db(store))
        return store.jsonify(), 201

    @staticmethod
    def delete(name):
        store = StoreModel.find_by_name(name)
        if store:
            ItemModel.query.filter(ItemModel.store_id == store.id).delete()
            safe_run(message='error delete store with name {}'.format(name),
                     error_code=500)(store.delete_from_db(store))
        else:
            return {'message': 'store with name {} does not exist'.format(name)}, 400
        return {'message': 'store with name {} deleted'.format(name)}


class StoreList(Resource):
    @staticmethod
    def get():
        return {'stores': [store.jsonify() for store in StoreModel.query.all()]}
