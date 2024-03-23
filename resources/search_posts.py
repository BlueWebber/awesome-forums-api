from flask_restful import Resource
from flask import abort
from services import db
from math import ceil
from config import config


class SearchPosts(Resource):
    @staticmethod
    def get(search_query=None, sort_column="newest", page_number=0):
        if not search_query.strip():
            return {}, 204
        pages_num = config.NUMBER_OF_POST_PAGES
        if sort_column not in config.ALLOWED_POST_SORT_CLAUSES:
            return abort(400, "Invalid sorting clause")
        posts = db.search_paginated_posts(search_query, page_number, sort_column)
        number_of_pages = ceil(db.get_number_of_searched_posts(search_query)["count"] / pages_num)
        if not posts:
            return {"posts": [], "number_of_pages": number_of_pages, "message": "no results found"}, 204
        return {"posts": posts, "number_of_pages": number_of_pages}
