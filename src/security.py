from src.models.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user is not None and user.password == password:
        return user
    return None


def identity(payload):
    _id = payload['identity']
    return UserModel.find_by_userid(_id)
