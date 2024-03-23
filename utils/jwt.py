import jwt
import datetime
import os
from config import config


def encode_auth_token(user_data, is_refresh=False):
    if is_refresh:
        exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=config.REFRESH_COOKIE_EXPIRY_SECONDS)
    else:
        exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=config.EXPIRY_TIME_MINS,
                                                              hours=config.EXPIRY_TIME_HOURS)
        # exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=10)
    payload = {
        'iat': datetime.datetime.utcnow(),
        'exp': exp,
        'user_id': user_data['user_id'],
        'username': user_data['username'],
        'email': user_data['email'],
        'permission_level': user_data['permission_level'],
        'pfp_link': user_data['pfp_link'],
        'reputation': user_data['reputation'],
        'is_refresh': is_refresh
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


def set_refresh_cookie(user):
    def cookie_setter(response):
        response.set_cookie(config.REFRESH_COOKIE_NAME, value=encode_auth_token(user, is_refresh=True),
                            max_age=config.REFRESH_COOKIE_EXPIRY_SECONDS, samesite="Lax", httponly=True)
        return response
    return cookie_setter


def unset_refresh_cookie(response):
    response.set_cookie(config.REFRESH_COOKIE_NAME, value='', max_age=0)
    return response
