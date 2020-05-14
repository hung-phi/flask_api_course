from flask_restful import Resource, reqparse

from src.security import *
from src.encoder import *
from src.constants import *


class MSG:
    OK = 'OK'
    EXISTED = 'user with username {} existed'
    REGISTERED = 'user with username {} registered'
    USERNAME_EMPTY = 'username cannot be empty'
    USERNAME_LEN_EXCEED = 'username length cannot exceed {}'.format(USERNAME_LEN)
    PASSWORD_EMPTY = 'password cannot be empty'
    PASSWORD_LEN_EXCEED = 'password length cannot exceed {}'.format(PASSWORD_LEN)


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

    @classmethod
    def post(cls):
        data = UserRegister.parser.parse_args()
        is_valid, msg = cls.validate_username_input(data['username'])
        if not is_valid:
            return {'message': msg}, 400
        is_valid, msg = cls.validate_password_input(data['password'])
        if not is_valid:
            return {'message': msg}, 400
        if UserModel.find_by_username(data['username']) is not None:
            return {'message': MSG.EXISTED.format(data['username'])}, 400
        data['hashed_password'], data['salt'] = encoder(data['password'])
        user = UserModel(**data)
        user.save_to_db(user)
        return {'message': MSG.REGISTERED.format(data['username'])}, 201

    @staticmethod
    def validate_username_input(username):
        if len(username.strip()) == 0:
            return False, MSG.USERNAME_EMPTY
        if len(username) > USERNAME_LEN:
            return False, MSG.USERNAME_LEN_EXCEED
        return True, MSG.OK

    @staticmethod
    def validate_password_input(password):
        if len(password.strip()) == 0:
            return False, MSG.PASSWORD_EMPTY
        if len(password) > PASSWORD_LEN:
            return False, MSG.PASSWORD_LEN_EXCEED
        return True, MSG.OK
