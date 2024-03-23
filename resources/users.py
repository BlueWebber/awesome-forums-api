from flask_restful import Resource
from flask import abort, after_this_request
from services import db
from parsers import register_parser, patch_user_parser
from utils.pw_hash import hash_pw
from utils.validators import validate_and_inject
from utils.getters import decode_token_from_header
from utils.validators import validate_and_upload_pfp
from services.auth import authorization_level, with_refresh
from permissions import permissions_map as perm
from utils.jwt import encode_auth_token, set_refresh_cookie
from config import config
import json


class Users(Resource):
    @staticmethod
    @validate_and_inject([db.get_user])
    @with_refresh
    def get(user):
        del user['password']
        token = decode_token_from_header()
        user['is_own'] = True
        if not token or token['user_id'] != user['user_id']:
            del user['email']
            del user['settings']
            del user['is_own']
        else:
            user['settings'] = json.loads(user['settings'])
        return user

    @staticmethod
    def post(user_id=None):
        data = register_parser.parse_args()
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
        result['token'] = encode_auth_token(result)
        after_this_request(set_refresh_cookie(result))
        del result['password']
        return result, 201

    @staticmethod
    @authorization_level(perm.normal)
    def patch(user_id=None):
        data = patch_user_parser.parse_args()

        if data['email'] and db.get_user_by_email(data['email']):
            return abort(409, 'E-mail is already in use')
        if data['username'] and db.get_user_by_username(data['username']):
            return abort(409, 'Username is already in use')

        user_id = decode_token_from_header()["user_id"]
        user = db.get_user(user_id)
        pfp_link = user["pfp_link"]
        pfp_b64 = data.pop("pfp_base64")

        if pfp_b64:
            pfp_link = validate_and_upload_pfp(pfp_b64)
            if not pfp_link:
                return abort(400, "Invalid pfp (pfp_base64)")
        data["pfp_link"] = pfp_link

        settings = data.pop("settings") or {}
        if settings:
            for key in settings.keys():
                if key not in config.ALLOWED_USER_SETTINGS:
                    return abort(400, "invalid settings value")

        user.update({k: v for k, v in data.items() if v})
        user["settings"] = json.loads(user["settings"])
        user["settings"].update(settings)
        user["settings"] = json.dumps(user["settings"])
        db.edit_user(**user)
        user['token'] = encode_auth_token(user)
        after_this_request(set_refresh_cookie(user))
        del user['password']
        return user
