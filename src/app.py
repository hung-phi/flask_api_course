from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from user import User
from security import authenticate, identity

app = Flask(__name__)
api = Api(app)
app.secret_key = 'phi'

jwt = JWT(app, authenticate, identity)

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='this cannot be blank'
                        )

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item is not None else 404

    @jwt_required()
    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': 'item existed'}, 400
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] == name, items))

    @jwt_required()
    def put(self, name):

        data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            Item.update(data)
        return Item

class ItemList(Resource):
    def get(self):
        return items


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)