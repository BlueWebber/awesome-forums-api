from utils.jwt import decode_auth_token
from flask import request
from config import config


def decode_token_from_header():
    try:
        token = request.headers[config.AUTH_TOKEN_NAME]
    except KeyError:
        return
    return decode_auth_token(token)


def fetch_result(fetch_method, next_set):
    def decorator(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            result = fetch_method()
            next_set()
            return result
        return wrapper
    return decorator
