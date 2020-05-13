from flask_restful import Resource, reqparse

from src.security import *
from src.encoder import *


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='Username is required, must not contain any white space'
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='Password is required, must not contain any white space'
                        )

    @staticmethod
    def post():
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']) is not None:
            return {'message': 'user with username {} existed'.format(data['username'])}, 400
        data['hashed_password'], data['salt'] = encoder(data['password'])
        print({k: v for k, v in data if k != 'password'})
        user = UserModel(**{k: v for k, v in data if k != 'password'})
        user.save_to_db(user)
        return {'message': 'user with username {} registered'.format(data['username'])}, 201
