from flask_restful import Resource
from services import db
from utils.validators import validate_and_inject
from utils.serializer import group_reactions


class PostReactions(Resource):
    @staticmethod
    @validate_and_inject([db.get_post])
    def get(post):
        reactions = db.get_post_reactions(post["post_id"])
        if not reactions:
            return {}, 204
        return group_reactions(reactions)
