from flask_restful import Resource
from flask import abort
from services.auth import authorization_level
from permissions import permissions_map as perm
from parsers import upload_parser
from config import config
from utils.validators import validate_and_upload_media


class Upload(Resource):
    @staticmethod
    @authorization_level(perm.normal)
    def post():
        data = upload_parser.parse_args()
        if data["content_type"] == "image":
            link = validate_and_upload_media("image", data["content_base64"])
            if not link:
                return abort(400, "Corrupted or invalid image, also make sure your image's size is below"
                                  f"{config.MAX_IMAGE_SIZE} bytes")
            return {"link": link}, 201

        elif data["content_type"] == "video":
            link = validate_and_upload_media("video", data["content_base64"])
            if not link:
                return abort(400, "Corrupted or invalid video, also make sure your image's size is below"
                                  f"{config.MAX_VID_SIZE} bytes")
            return {"link": link}, 201
        else:
            return abort(400, "Invalid content_type, must be 'image' or 'video'")
