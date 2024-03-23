from flask_restful import Resource
from flask import abort
from services import db
from utils.validators import validate_and_inject
from utils.getters import decode_token_from_header
from services.auth import authorization_level
from permissions import permissions_map as perm
from parsers import reaction_parser


class PostReactions(Resource):
    @staticmethod
    @validate_and_inject([db.get_post])
    def get(post):
        reactions = db.get_post_reactions(post["post_id"])
        if not reactions:
            return {}, 204
        user = decode_token_from_header()
        user_reaction = None
        if user:
            user_reaction = db.get_user_post_reaction(user["user_id"], post["post_id"])
        return {"reactions": reactions, "user_reaction": user_reaction}

    @staticmethod
    @validate_and_inject([db.get_post])
    @authorization_level(perm.normal)
    def post(post):
        reaction_id = reaction_parser.parse_args()["reaction_type_id"]
        user_id = decode_token_from_header()["user_id"]
        if user_id == post["author_id"]:
            return abort(400, "can't react to own post")
        if not db.get_reaction(reaction_id):
            return abort(400, "reaction type doesn't exist")
        if db.get_user_post_reaction(user_id, post["post_id"]):
            return abort(409, "User already has a reaction on said post")
        return db.create_post_reaction(reaction_id, post["post_id"], user_id)

    @staticmethod
    @authorization_level(perm.normal)
    def delete(post_id):
        user = decode_token_from_header()
        reaction = db.get_user_post_reaction(user["user_id"], post_id)
        if not reaction:
            return abort(404, "you don't have a reaction on this post")
        if reaction["creator_id"] != user["user_id"] and user["permission_level"] < perm.mod:
            return abort(403)
        return db.delete_post_reaction(reaction["reaction_id"]), 204

    @staticmethod
    @validate_and_inject([db.get_post])
    @authorization_level(perm.normal)
    def put(post):
        reaction_id = reaction_parser.parse_args()["reaction_type_id"]
        user_id = decode_token_from_header()["user_id"]
        if user_id == post["author_id"]:
            return abort(400, "can't react to own post")
        if not db.get_reaction(reaction_id):
            return abort(400, "reaction type doesn't exist")
        reaction = db.get_user_post_reaction(user_id, post["post_id"])
        if reaction:
            if reaction["reaction_type_id"] == reaction_id:
                return abort(400, "can't overwrite reaction of same type")
            if reaction["creator_id"] != user_id:
                return abort(403)
            db.delete_post_reaction(reaction["reaction_id"])
        return db.create_post_reaction(reaction_id, post["post_id"], user_id)
