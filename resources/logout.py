from flask_restful import Resource
from flask import after_this_request
from utils.jwt import unset_refresh_cookie


class Logout(Resource):
    @staticmethod
    def get():
        after_this_request(unset_refresh_cookie)
        return {}, 204
