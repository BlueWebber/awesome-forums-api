from flask_restful import Resource
from flask import abort
from services import db
from math import ceil
from config import config


class Posts(Resource):
    @staticmethod
    def get(sort_column="newest", page_number=0):
        pages_num = config.NUMBER_OF_POST_PAGES
        number_of_pages = ceil(db.get_number_of_posts()["count"] / pages_num)
        if sort_column not in {"newest", "most_replies"}:
            return abort(404, "Invalid sorting clause")
        return {"posts": db.get_paginated_posts(page_number, pages_num, sort_column),
                "number_of_pages": number_of_pages}
