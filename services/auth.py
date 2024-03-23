from flask import request, abort
from utils import jwt
from config import config


def authorization_level(level):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                token = request.headers[config.AUTH_TOKEN_NAME]
            except KeyError:
                return abort(400, 'Access denied, no token provided')

            decoded = jwt.decode_auth_token(token)
            if decoded:
                if decoded['permission_level'] >= level:
                    return func(*args, **kwargs)
                return abort(403, 'Forbidden, user does not have appropriate permissions')
            return abort(401, 'Access denied, Invalid token')
        return wrapper
    return decorator
