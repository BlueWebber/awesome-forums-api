from flask_restful import Resource
from parsers import new_post_reply_parser
from services.auth import authorization_level
from services import db
from utils.validators import validate_and_inject
from config import config
from permissions import permissions_map as perm
from utils.getters import decode_token_from_header
from math import ceil
from flask import abort


class PostReplies(Resource):
    @staticmethod
    @validate_and_inject([db.get_post])
    def get(post, sort_column="newest", page_number=0):
        pages_num = config.NUMBER_OF_POST_PAGES
        number_of_replies = db.get_number_of_post_replies(post["post_id"])
        number_of_pages = ceil(number_of_replies["count"] / pages_num)
        if sort_column not in config.ALLOWED_REPLY_SORT_CLAUSES:
            return abort(400, "Invalid sorting clause")
        replies = db.get_paginated_post_replies(post['post_id'], page_number, pages_num, sort_column)
        if not replies:
            return {"replies": [], "number_of_pages": number_of_pages, "message": "this page doesn't exist"}, 404
        return {"replies": replies, "number_of_pages": number_of_pages}

    @staticmethod
    @validate_and_inject([db.get_post])
    @authorization_level(perm.normal)
    def post(post):
        body = new_post_reply_parser.parse_args()['body']
        user_id = decode_token_from_header()['id']
        return db.create_post_reply(post['post_id'], user_id, body), 201
