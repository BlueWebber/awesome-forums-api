from flask_restful import Resource
from flask import abort
from utils.media import Image
from services.auth import authorization_level
from permissions import permissions_map as perm
from parsers import image_upload_parser


class Upload(Resource):
    @staticmethod
    @authorization_level(perm.normal)
    def post():
        img_str = image_upload_parser.parse_args()["image_base64"]
        img = Image(img_str)
        link = img.upload()
        if not link:
            return abort(400, "Corrupted image or bad image format")
        return {"link": link}, 201
