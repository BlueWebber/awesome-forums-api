from flask_restful import Resource
from flask import abort
from services import db
from parsers import notification_is_read_parser
from services.auth import authorization_level
from permissions import permissions_map as perm
from utils.getters import decode_token_from_header
from utils.validators import validate_and_inject


class Notification(Resource):
    @staticmethod
    @authorization_level(perm.normal)
    def get(notification_id):
        user = decode_token_from_header()
        notification = db.get_notification(notification_id)
        if notification['target_id'] != user['user_id']:
            return abort(403, "Can't view other users' notifications")
        return notification

    @staticmethod
    @validate_and_inject([db.get_notification])
    @authorization_level(perm.normal)
    def delete(notification):
        user = decode_token_from_header()
        if user['user_id'] != notification['target_id']:
            return abort(403, "can't delete other users' notifications")
        return db.delete_notification(notification['notification_id']), 204

    @staticmethod
    @validate_and_inject([db.get_notification])
    @authorization_level(perm.normal)
    def patch(notification):
        user = decode_token_from_header()
        is_read = notification_is_read_parser.parse_args()['is_read']
        if user['user_id'] != notification['target_id']:
            return abort(403, "can't modify other users' notifications")
        return db.edit_notification_is_read(notification['notification_id'], is_read), 204
