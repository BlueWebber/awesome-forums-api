from flask_restful import Resource
from services.db import get_post
from utils.validators import validate_and_inject


class Test(Resource):
    @staticmethod
    @validate_and_inject([get_post])
    def get(post):
        return {"post": post}
