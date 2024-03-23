from flask_restful import Resource
from flask import abort
from services import db
from utils.jwt import encode_auth_token
from utils.getters import decode_token_from_header


class Refresh(Resource):
    @staticmethod
    def get():
        token = decode_token_from_header()
        if token is None:
            return abort(401, 'No token provided')
        if token is False:
            return abort(401, 'Invalid token')
        user = db.get_user(token['user_id'])
        if not user:
            return abort(400, "User doesn't exist")
        return encode_auth_token(user)
