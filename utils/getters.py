from utils.jwt import decode_auth_token
from flask import request
from config import config


def decode_token_from_header():
    try:
        token = request.headers[config.AUTH_TOKEN_NAME]
    except KeyError:
        return
    return decode_auth_token(token)
