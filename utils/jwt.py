import jwt
import datetime
import os
from config import config


def encode_auth_token(user_data):
    payload = {
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=config.EXPIRY_TIME_MINS,
                                                               hours=config.EXPIRY_TIME_HOURS),
        'user_id': str(user_data['user_id']),
        'username': user_data['username'],
        'email': user_data['email'],
        'permission_level': user_data['permission_level']
    }
    return jwt.encode(
        payload,
        os.environ.get('SECRET_KEY'),
        algorithm='HS256'
        )


def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, os.environ.get('SECRET_KEY'), algorithms=["HS256"])
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return False
