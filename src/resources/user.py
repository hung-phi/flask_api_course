from flask_restful import Resource, reqparse

from src.models.user import UserModel


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
        if data['username'] != data['username'].strip() or data['password'] != data['password'].strip():
            return {'message': 'username or password must not contain white space'}, 400
        if UserModel.find_by_username(data['username']) is not None:
            return {'message': 'user existed'}, 400
        user = UserModel(**data)
        user.save_to_db()
        return {'message': 'user registered'}, 201
