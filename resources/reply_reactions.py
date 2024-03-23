from flask_restful import Resource
from services import db
from utils.validators import validate_and_inject
from utils.serializer import group_reactions


class ReplyReactions(Resource):
    @staticmethod
    @validate_and_inject([db.get_post_reply])
    def get(reply):
        reactions = db.get_reply_reactions(reply["reply_id"])
        if not reactions:
            return {}, 204
        return group_reactions(reactions)
