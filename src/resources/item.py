from flask_restful import Resource, Api, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='this cannot be blank'
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='this cannot be blank'
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.jsonify()
        return {'message': 'not found'}, 404


    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name) is not None:
            return {'message': 'item existed'}

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {'message': 'error during insertion'}, 500
        return item.jsonify(), 201


    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'item deleted'}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)

        else:
            item.price = data['price']
        item.save_to_db()
        return item.jsonify()


class ItemList(Resource):
    def get(self):
        return {'item': list(map(lambda item: item.jsonify(), ItemModel.query.all()))}


