from flask_restful import Resource
from parsers import new_post_parser, patch_post_parser
from services.auth import authorization_level
from services import db
from flask import abort
from utils.getters import decode_token_from_header
from utils.validators import validate_and_inject
from permissions import permissions_map as perm


class Post(Resource):
    @staticmethod
    @validate_and_inject([db.get_post])
    def get(post):
        return post

    @staticmethod
    @authorization_level(perm.normal)
    def post():
        data = new_post_parser.parse_args()
        user = decode_token_from_header()
        if data["is_pinned"] and user["permission_level"] < perm.mod:
            return abort(403, "can't pin a post with your current permission level")
        return db.create_post(user["user_id"], **data), 201

    @staticmethod
    @validate_and_inject([db.get_post])
    @authorization_level(perm.normal)
    def patch(post):
        data = patch_post_parser.parse_args()
        user = decode_token_from_header()
        if (user['user_id'] != post['author_id'] or data["is_pinned"]) and user['permission_level'] < perm.mod:
            return abort(403)
        post.update(data)
        db.edit_post(**post)
        return post

    @staticmethod
    @validate_and_inject([db.get_post])
    @authorization_level(perm.mod)
    def delete(post):
        return db.delete_post(post["post_id"]), 204
