from flask_restful import Resource

from src.models.store import StoreModel
from src.helper import *


class Store(Resource):
    @staticmethod
    def get(name):
        status, message = validate_input_string(name, 80)
        if not status:
            return {'message': message}, 400
        store = StoreModel.find_by_name(name)
        if store:
            return store.jsonify()
        return {'message': 'store with name {} not found'.format(name)}, 404

    @staticmethod
    def post(name):
        status, message = validate_input_string(name, 80)
        if not status:
            return {'message': message}, 400
        store = StoreModel.find_by_name(name)
        if store:
            return {'message': 'store with name {} has existed'.format(name)}, 400
        store = StoreModel(name)
        try:
            store.save_to_db(store)
        except Exception as e:
            return {'message': 'error creating store\n {}'.format(e)}, 500
        return store.jsonify(), 201

    @staticmethod
    def delete(name):
        status, message = validate_input_string(name, 80)
        if not status:
            return {'message': message}, 400
        store = StoreModel.find_by_name(name)
        if store:
            try:
                store.delete_from_db(store)
            except Exception as e:
                return {'message': 'error delete store with name {}\n {}'.format(name, e)}, 500
        return {'message': 'store with name {} deleted'.format(name)}


class StoreList(Resource):
    @staticmethod
    def get():
        return {'stores': [store.jsonify() for store in StoreModel.query.all()]}
