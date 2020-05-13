import hashlib, binascii, os

import src.config as cfg
from src.constants import *

SEED = cfg.SEED
ALGORITHM = cfg.HASH_ALG


def encoder(password):
    """Hash a password for storing.
    """
    salt = os.urandom(SALT_LEN)
    pwdhash = hashlib.pbkdf2_hmac(ALGORITHM, password.encode('utf-8'),
                                  salt, SEED)
    pwdhash = binascii.hexlify(pwdhash)
    return pwdhash.decode('ascii'), salt


def decoder(stored_pwd, salt, provided_pwd):
    """Verify a stored password against one provided by user.
    """
    pwdhash = hashlib.pbkdf2_hmac(ALGORITHM,
                                  provided_pwd.encode('utf-8'),
                                  salt, SEED)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_pwd
