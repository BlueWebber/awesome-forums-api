from flask_restful import Resource
from flask import abort
from services import db
from parsers import register_parser
from utils.pw_hash import hash_pw
from utils.validators import validate_email, validate_and_inject, validate_username
from utils.getters import decode_token_from_header
from utils.validators import upload_image
from services.auth import authorization_level
from permissions import permissions_map as perm
import services.imgur as imgur
from parsers import image_upload_parser


class Upload(Resource):
    @staticmethod
    @authorization_level(perm.normal)
    def post(user_id=None):
        img_str = image_upload_parser.parse_args()["image_base64"]

        pfp_link = None
        if data["pfp_base64"]:
            pfp_link = validate_and_upload_image(data["pfp_base64"])
            if not pfp_link:
                return abort(400, "Invalid pfp (pfp_base64)")
        result = db.create_user(data['username'], data['email'], password, pfp_link)
        del result['password']
        return result, 201
