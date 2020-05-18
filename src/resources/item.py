from flask_restful import Resource, Api, reqparse
from flask_jwt import jwt_required
from functools import wraps

from src.models.item import ItemModel
from src.error import safe_run


class MSG:
    OK = 'OK'
    NOT_FOUND = 'item with name {} not found'
    EXISTED = 'item with name {} has already existed'
    ERROR_DELETE = 'error during deleting item with name {}'
    ERROR_INSERT = 'error during inserting item with name {}'
    NOT_EXIST = 'item with name {} does not exist'
    DELETED = 'item with name {} has been deleted'
    EMPTY = 'item name cannot be empty'
    ERROR_UPDATE = 'error during updating item with name {}'


def validate_item_name_input(func):
    @wraps(func)
    def func_wrapper(self, name):
        if len(name.strip()) == 0:
            return {'message': MSG.EMPTY}, 400
        return func(self, name)
    return func_wrapper


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='name must be a string'
                        )
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='price must be a real number'
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='store_id must be an integer'
                        )

    @jwt_required()
    @validate_item_name_input
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.jsonify()
        return {'message': MSG.NOT_FOUND.format(name)}, 404

    @jwt_required()
    @validate_item_name_input
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': MSG.EXISTED.format(name)}, 400
        data = self.parser.parse_args()
        item = ItemModel(**data)
        safe_run(message=MSG.ERROR_INSERT.format(name),
                 error_code=500)(item.save_to_db(item))
        return item.jsonify(), 201

    @jwt_required()
    @validate_item_name_input
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            safe_run(message=MSG.ERROR_DELETE.format(name),
                     error_code=500)(item.delete_from_db(item))
        else:
            return {'message': MSG.NOT_FOUND.format(name)}, 400
        return {'message': MSG.DELETED.format(name)}, 201

    @jwt_required()
    @validate_item_name_input
    def put(self, name):
        data = self.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(**data)
        else:
            for key in ['price', 'name']:
                setattr(item, key, data[key])
        safe_run(message=MSG.ERROR_UPDATE.format(name),
                 error_code=500)(item.save_to_db(item))
        return item.jsonify(), 201


class ItemList(Resource):
    @staticmethod
    def get():
        return {'item': list(map(lambda item: item.jsonify(), ItemModel.query.all()))}
