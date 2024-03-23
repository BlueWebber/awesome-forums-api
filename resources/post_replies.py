from flask_restful import Resource
from parsers import new_post_reply_parser
from services.auth import authorization_level
from services import db
from utils.validators import validate_and_inject
from config import config
from permissions import permissions_map as perm
from utils.getters import decode_token_from_header


class PostReplies(Resource):
    @staticmethod
    @validate_and_inject([db.get_post])
    def get(post, page_number):
        pages_num = config.NUMBER_OF_POST_PAGES
        return db.get_paginated_post_replies(post['post_id'], page_number, pages_num)

    @staticmethod
    @validate_and_inject([db.get_post])
    @authorization_level(perm.normal)
    def post(post):
        body = new_post_reply_parser.parse_args()['body']
        user_id = decode_token_from_header()['id']
        return db.create_post_reply(post['post_id'], user_id, body), 201
