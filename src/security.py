import hashlib, binascii, os

from src.models.user import UserModel
import src.config as cfg

SEED = cfg.SEED
ALGORITHM = cfg.HASH_ALG


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user is not None and verify_password(user.password, password):
        return user
    return None


def identity(payload):
    _id = payload['identity']
    return UserModel.find_by_id(_id)


def hash_password(password):
    """Hash a password for storing.
    """
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac(ALGORITHM, password.encode('utf-8'),
                                  salt, SEED)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_pwd, provided_pwd):
    """Verify a stored password against one provided by user.
    """
    salt = stored_pwd[:64]
    stored_password = stored_pwd[64:]
    pwdhash = hashlib.pbkdf2_hmac(ALGORITHM,
                                  provided_pwd.encode('utf-8'),
                                  salt.encode('ascii'),
                                  SEED)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password
