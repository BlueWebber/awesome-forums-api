import nacl.exceptions
from nacl import pwhash


def hash_pw(password):
    return pwhash.argon2id.str(bytes(password, encoding='utf-8'))


def verify_pw(password, hashed_password):
    try:
        pwhash.argon2id.verify(hashed_password, bytes(password, encoding='utf-8'))
    except nacl.exceptions.InvalidkeyError:
        return False
    return True
