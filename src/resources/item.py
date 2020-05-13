from flask_restful import Resource, Api, reqparse
from flask_jwt import jwt_required

from src.models.item import ItemModel
from src.helper import *


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
        status, message = validate_input_string(name, 80)
        if not status:
            return {'message': message}, 400
        item = ItemModel(**data)
        try:
            item.save_to_db(item)
        except Exception as e:
            return {'message': 'error during insertion\n {}'.format(e)}, 500
        return item.jsonify(), 201

    @jwt_required()
    def delete(self, name):
        status, message = validate_input_string(name, 80)
        if not status:
            return {'message': message}, 400
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db(item)
        return {'message': 'item with name {} deleted'.format(name)}

    @jwt_required()
    def put(self, name):
        status, message = validate_input_string(name, 80)
        if not status:
            return {'message': message}, 400
        data = self.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(**data)
        else:
            item.price = data['price']
        item.save_to_db(item)
        return item.jsonify()


class ItemList(Resource):
    def get(self):
        return {'item': list(map(lambda item: item.jsonify(), ItemModel.query.all()))}


