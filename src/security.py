from src.models.user import UserModel
from src.hash_password import verify_password


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user is not None and verify_password(user.hashed_password, user.salt, password):
        return user
    return None


def identity(payload):
    _id = payload['identity']
    return UserModel.find_by_id(_id)
