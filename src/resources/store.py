from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.jsonify()
        return {'message': 'store not found'}, 404

    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {'message': 'store existed'}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'error creating store'}, 500
        return store.jsonify(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': 'store deleted'}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.jsonify() for store in StoreModel.query.all()]}