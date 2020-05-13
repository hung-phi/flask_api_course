from flask_restful import Resource, reqparse

from src.security import *
from src.helper import *


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
        status, message = validate_input_string(data['username'], 32)  # validate username
        if not status:
            return {'message': message}, 400
        status, message = validate_input_string(data['password'], 32)  # validate password
        if not status:
            return {'message': message}, 400
        if UserModel.find_by_username(data['username']) is not None:
            return {'message': 'user with username {} existed'.format(data['username'])}, 400
        data['password'] = hash_password(data['password'])
        user = UserModel(**data)
        user.save_to_db(user)
        return {'message': 'user with username {} registered'.format(data['username'])}, 201
