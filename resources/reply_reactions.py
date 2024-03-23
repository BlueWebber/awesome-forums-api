from flask_restful import Resource
from flask import abort
from services import db
from utils.validators import validate_and_inject
from services.auth import authorization_level
from utils.getters import decode_token_from_header
from permissions import permissions_map as perm
from parsers import reaction_parser


class ReplyReactions(Resource):
    @staticmethod
    @validate_and_inject([db.get_post_reply])
    def get(reply):
        reactions = db.get_reply_reactions(reply["reply_id"])
        if not reactions:
            return {}, 204
        return reactions

    @staticmethod
    @validate_and_inject([db.get_post_reply])
    @authorization_level(perm.normal)
    def post(reply):
        reaction_id = reaction_parser.parse_args()["reaction_type_id"]
        user_id = decode_token_from_header()["user_id"]
        if user_id == reply["author_id"]:
            return abort(400, "can't react to own reply")
        if not db.get_reaction(reaction_id):
            return abort(400, "reaction type doesn't exist")
        if db.get_user_reply_reaction(user_id, reply["reply_id"]):
            return abort(409, "User already has a reaction on said reply")
        return db.create_reply_reaction(reaction_id, reply["reply_id"], user_id)

    @staticmethod
    @authorization_level(perm.normal)
    def delete(reply_id):
        user = decode_token_from_header()
        reaction = db.get_user_reply_reaction(user["user_id"], reply_id)
        if not reaction:
            return abort(404, "you don't have a reaction on this reply")
        if reaction["creator_id"] != user["user_id"] and user["permission_level"] < perm.mod:
            return abort(403)
        return db.delete_reply_reaction(reaction["reaction_id"]), 204

    @staticmethod
    @validate_and_inject([db.get_post_reply])
    @authorization_level(perm.normal)
    def put(reply):
        reaction_id = reaction_parser.parse_args()["reaction_type_id"]
        user_id = decode_token_from_header()["user_id"]
        if user_id == reply["author_id"]:
            return abort(400, "can't react to own reply")
        if not db.get_reaction(reaction_id):
            return abort(400, "reaction type doesn't exist")
        reaction = db.get_user_reply_reaction(user_id, reply["reply_id"])
        if reaction:
            if reaction["reaction_type_id"] == reaction_id:
                return abort(400, "can't overwrite reaction of same type")
            if reaction["creator_id"] != user_id:
                return abort(403)
            db.delete_reply_reaction(reaction["reaction_id"])
        return db.create_reply_reaction(reaction_id, reply["reply_id"], user_id)
