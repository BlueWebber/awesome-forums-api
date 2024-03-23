from flask_restful import Resource
from flask import abort
from parsers import new_post_reply_parser
from services.auth import authorization_level
from services import db
from utils.validators import validate_and_inject
from permissions import permissions_map as perm
from utils.getters import decode_token_from_header


class PostReply(Resource):
    @staticmethod
    @validate_and_inject([db.get_post_reply])
    @authorization_level(perm.normal)
    def patch(reply):
        body = new_post_reply_parser.parse_args()['body']
        user = decode_token_from_header()
        if user['user_id'] != reply['author_id'] and user['permission_level'] < perm.mod:
            return abort(403)
        reply["body"] = body
        db.edit_post_reply(reply["reply_id"], body)
        return reply

    @staticmethod
    @validate_and_inject([db.get_post_reply])
    @authorization_level(perm.normal)
    def delete(reply):
        print('deleting')
        user = decode_token_from_header()
        if user['user_id'] != reply['author_id'] and user['permission_level'] < perm.mod:
            return abort(403)
        return db.delete_post_reply(reply["reply_id"]), 204
