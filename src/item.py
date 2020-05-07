from flask_restful import Resource, Api, reqparse
from flask_jwt import jwt_required
import sqlite3

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='this cannot be blank'
                        )

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        cursor.execute(query, (name,))
        row = cursor.fetchone()

        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    @classmethod
    def insert_item(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    @jwt_required()
    def post(self, name):
        if self.find_by_name(name) is not None:
            return {'message': 'item existed'}

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        try:
            self.insert_item(item)
        except:
            return {'message': 'error during insertion'}, 500
        return item, 201


    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()
        return {'message': 'item deleted'}

    @jwt_required()
    def put(self, name):

        data = Item.parser.parse_args()

        item = self.find_by_name(name)
        item_object = {'name': name, 'price': data['price']}
        if item is None:
            self.insert_item(item_object)
        else:
            self.update_item(item_object)
        return item

    @classmethod
    def update_item(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name'],))

        connection.commit()
        connection.close()
        return {'message': 'item updated'}

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query,)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.commit()
        connection.close()
        return {'items': items}


