from flask_restful import Resource
from flask import abort, after_this_request
from services import db
from parsers import login_parser
from utils.pw_hash import verify_pw
from utils.jwt import encode_auth_token, set_refresh_cookie


class Auth(Resource):
    @staticmethod
    def post():
        data = login_parser.parse_args()
        user = db.get_user_by_email(data['email'])
        if not user or not verify_pw(data['password'], user['password']):
            return abort(401, 'Invalid username or password')
        after_this_request(set_refresh_cookie(user))

        return encode_auth_token(user)
