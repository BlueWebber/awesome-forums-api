from flask_restful import Resource
from flask import abort
from services import db
from parsers import register_parser, patch_user_parser
from utils.pw_hash import hash_pw
from utils.validators import validate_email, validate_and_inject, validate_username
from utils.getters import decode_token_from_header
from utils.validators import validate_and_upload_pfp
from services.auth import authorization_level
from permissions import permissions_map as perm


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
    def post():
        data = register_parser.parse_args()
        if not validate_email(data['email']):
            return abort(400, 'E-mail must be a valid E-mail')
        if not validate_username(data['username']):
            return abort(400, 'Username contains illegal characters (must be alphanumeric)')
        if db.get_user_by_email(data['email']):
            return abort(409, 'E-mail is already in use')
        if db.get_user_by_username(data['username']):
            return abort(409, 'Username is already in use')
        password = hash_pw(data['password'])
        pfp_link = None
        if data["pfp_base64"]:
            pfp_link = validate_and_upload_pfp(data["pfp_base64"])
            if not pfp_link:
                return abort(400, "Invalid pfp (pfp_base64)")
        result = db.create_user(data['username'], data['email'], password, pfp_link)
        del result['password']
        return result, 201

    @staticmethod
    @authorization_level(perm.normal)
    def patch():
        data = patch_user_parser.parse_args()
        user_id = decode_token_from_header()["user_id"]
        user = db.get_user(user_id)
        pfp_link = user["pfp_link"]
        pfp_b64 = data.pop("pfp_base64")
        if pfp_b64:
            pfp_link = validate_and_upload_pfp(pfp_b64)
            if not pfp_link:
                return abort(400, "Invalid pfp (pfp_base64)")
        data["pfp_link"] = pfp_link
        user.update({k: v for k, v in data.items() if v})
        result = db.edit_user(**user)
        del result['password']
        return result
