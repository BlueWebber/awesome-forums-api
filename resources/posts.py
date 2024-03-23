from flask_restful import Resource
from services import db
from math import ceil
from config import config


class Posts(Resource):
    @staticmethod
    def get(page_number=0):
        pages_num = config.NUMBER_OF_POST_PAGES
        number_of_pages = ceil(db.get_number_of_posts() / pages_num)
        return {"posts": db.get_paginated_posts(page_number, pages_num), "number_of_pages": number_of_pages}
