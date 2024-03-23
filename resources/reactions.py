from flask_restful import Resource
from services import db


class Reactions(Resource):
    @staticmethod
    def get():
        return db.get_reactions()
