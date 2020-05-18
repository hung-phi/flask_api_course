from flask_restful import Resource
from functools import wraps

from src.models.store import StoreModel
from src.models.item import ItemModel
from src.error import safe_run


class MSG:
    OK = 'OK'
    NOT_FOUND = 'store with name {} not found'
    EXISTED = 'store with name {} has already existed'
    ERROR_DELETE = 'error during deleting store with name {}'
    ERROR_INSERT = 'error during inserting store with name {}'
    NOT_EXIST = 'store with name {} does not exist'
    DELETED = 'store with name {} has been deleted'
    EMPTY = 'store name cannot be empty'
    ERROR_UPDATE = 'error during updating store with name {}'


def validate_store_name_input(func):
    @wraps(func)
    def func_wrapper(self, name):
        if len(name.strip()) == 0:
            return {'message': MSG.EMPTY}, 400
        return func(self, name)
    return func_wrapper


class Store(Resource):
    @staticmethod
    @validate_store_name_input
    def get(name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.jsonify()
        return {'message': MSG.NOT_FOUND.format(name)}, 404

    @staticmethod
    @validate_store_name_input
    def post(name):
        store = StoreModel.find_by_name(name)
        if store:
            return {'message': MSG.EXISTED.format(name)}, 400
        store = StoreModel(name)
        safe_run(message=MSG.ERROR_INSERT.format(name),
                 error_code=500)(store.save_to_db(store))
        return store.jsonify(), 201

    @staticmethod
    @validate_store_name_input
    def delete(name):
        store = StoreModel.find_by_name(name)
        if store:
            ItemModel.query.filter(ItemModel.store_id == store.id).delete()
            safe_run(message=MSG.ERROR_DELETE.format(name),
                     error_code=500)(store.delete_from_db(store))
        else:
            return {'message': MSG.NOT_EXIST.format(name)}, 400
        return {'message': MSG.DELETED.format(name)}


class StoreList(Resource):
    @staticmethod
    def get():
        return {'stores': [store.jsonify() for store in StoreModel.query.all()]}
