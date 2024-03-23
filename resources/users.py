from flask_restful import Resource
from flask import abort
from services import db
from parsers import register_parser
from utils.pw_hash import hash_pw
from utils.validators import validate_email, validate_and_inject
from utils.getters import decode_token_from_header


class Users(Resource):
    @staticmethod
    @validate_and_inject([db.get_user])
    def get(user):
        del user['password']
        token = decode_token_from_header()
        if not token or token['user_id'] != user['user_id']:
            del user['email']
            del user['settings']
        return user

    @staticmethod
    def post(user_id=None):
        data = register_parser.parse_args()
        if not validate_email(data['email']):
            return abort(400, 'E-mail must be a valid E-mail')
        if db.get_user_by_email(data['email']):
            return abort(409, 'E-mail is already in use')
        if db.get_user_by_username(data['username']):
            return abort(409, 'Username is already in use')
        password = hash_pw(data['password'])
        result = db.create_user(data['username'], data['email'], password)
        del result['password']
        return result, 201
