from user import User
users = [
    User(1,'bob','asd')
]

username_mapping = {u.username: u for u in users}


userid_mapping = {u.id: u for u in users}

def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user is not None and user.password == password:
        return user

def identity(payload):
    userid = payload['identity']
    return userid_mapping.get(userid, None)
