from flask_restful import Resource
from services import db
from services.auth import authorization_level
from permissions import permissions_map as perm
from utils.getters import decode_token_from_header


class UnreadNotifications(Resource):
    @staticmethod
    @authorization_level(perm.normal)
    def get():
        user = decode_token_from_header()
        return {"number_of_unread_notifications": db.get_number_of_unread_user_notifications(user['user_id'])['count']}

