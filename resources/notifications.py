from flask_restful import Resource
from services import db
from math import ceil
from config import config
from services.auth import authorization_level
from permissions import permissions_map as perm
from utils.getters import decode_token_from_header


class Notifications(Resource):
    @staticmethod
    @authorization_level(perm.normal)
    def get(page_number=0):
        user = decode_token_from_header()
        pages_num = config.NUMBER_OF_NOTIFICATION_PAGES
        number_of_pages = ceil(db.get_number_of_user_notifications(user["user_id"])["count"] / pages_num)
        notifications = db.get_paginated_user_notifications(user["user_id"], page_number)
        if not notifications:
            return {"notifications": [], "number_of_pages": number_of_pages, "message": "this page doesn't exist"}, 404
        db.mark_user_notifications_as_read(user['user_id'])
        return {"notifications": notifications, "number_of_pages": number_of_pages}
