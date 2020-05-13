from flask_restful import Resource, Api, reqparse
from flask_jwt import jwt_required

from src.models.item import ItemModel
from src.error import *


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
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.jsonify()
        return {'message': 'item with name {} not found'.format(name)}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name) is not None:
            return {'message': 'item with name {} has already existed'.format(name)}, 400
        data = self.parser.parse_args()
        item = ItemModel(**data)
        safe_run(message='error during inserting item with name {}'.format(name),
                 error_code=500)(item.save_to_db(item))
        return item.jsonify(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            safe_run(message='error during deleting item with name {}'.format(name),
                     error_code=500)(item.delete_from_db(item))
        else:
            return {'message': 'item with name {} does not exist'.format(name)}, 400
        return {'message': 'item with name {} deleted'.format(name)}, 201

    @jwt_required()
    def put(self, name):
        data = self.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(**data)
        else:
            for key in ['price', 'name']:
                setattr(item, key, data[key])
        safe_run(message='error updating item with name {}'.format(name),
                 error_code=500)(item.save_to_db(item))
        return item.jsonify()


class ItemList(Resource):
    @staticmethod
    def get():
        return {'item': list(map(lambda item: item.jsonify(), ItemModel.query.all()))}
