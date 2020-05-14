import os

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from dotenv import load_dotenv
load_dotenv()

from src.security import authenticate, identity
from src.resources.user import UserRegister
from src.resources.item import Item, ItemList
from src.resources.store import Store, StoreList
from src.db import db

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
try:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
except EnvironmentError:
    print('specify database_uri in .env file')
    exit(0)
api = Api(app)
app.secret_key = os.getenv('SECRET')


@app.before_first_request
def create_table():
    db.create_all()


jwt = JWT(app, authenticate, identity)


api.add_resource(Item, '/items/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/stores/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
