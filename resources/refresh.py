from flask_restful import Resource
from flask import abort, request, after_this_request
from services import db
from utils.jwt import encode_auth_token, decode_auth_token, set_refresh_cookie


class Refresh(Resource):
    @staticmethod
    def get():
        refresh_token = request.cookies.get('refresh_token')

        if not refresh_token:
            return abort(401, 'No refresh token provided')
        decoded_refresh_token = decode_auth_token(refresh_token)

        if not decoded_refresh_token:
            return abort(401, 'Invalid token')

        if not decoded_refresh_token['is_refresh']:
            return abort(401, 'This is not a refresh token')
        user = db.get_user(decoded_refresh_token['user_id'])

        if not user:
            return abort(401, "User doesn't exist")

        if int(decoded_refresh_token['iat']) < int(user['last_props_change'].timestamp()):
            return abort(401, "User credentials have changed, a new token needs to be reissued")

        after_this_request(set_refresh_cookie(user))
        return encode_auth_token(user)
