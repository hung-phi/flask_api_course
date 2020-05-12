from flask_restful import Resource

from src.models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.jsonify()
        return {'message': 'store not found'}, 404

    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {'message': 'store with name {} has existed'.format(name)}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except Exception as e:
            return {'message': 'error creating store\n {}'.format(e)}, 500
        return store.jsonify(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            try:
                store.delete_from_db()
            except Exception as e:
                return {'message': 'error delete store\n {}'.format(e)}, 500
        return {'message': 'store deleted'}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.jsonify() for store in StoreModel.query.all()]}
