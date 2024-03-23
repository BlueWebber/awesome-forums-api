from flask import Flask
from extensions import api
from resources import (posts, post, post_replies, post_reply, auth, users, upload, refresh, post_reactions,
                       reply_reactions, reactions, search_posts)


def register_resources(curr_api):
    curr_api.add_resource(posts.Posts, '/posts/<string:sort_column>/<int:page_number>/')
    curr_api.add_resource(search_posts.SearchPosts,
                          '/search_posts/<string:search_query>/<string:sort_column>/<int:page_number>/')
    curr_api.add_resource(post.Post, '/post', '/post/<string:post_id>')
    curr_api.add_resource(post_replies.PostReplies, '/post_replies/<string:post_id>/<string:sort_column>/'
                                                    '<int:page_number>')
    curr_api.add_resource(post_reply.PostReply, '/post_reply/<string:reply_id>')
    curr_api.add_resource(auth.Auth, '/auth')
    curr_api.add_resource(users.Users, '/users', '/users/<string:user_id>')
    curr_api.add_resource(upload.Upload, '/upload')
    curr_api.add_resource(refresh.Refresh, '/refresh')
    curr_api.add_resource(post_reactions.PostReactions, '/post_reactions', '/post_reactions/<string:post_id>')
    curr_api.add_resource(reply_reactions.ReplyReactions, '/reply_reactions', '/reply_reactions/<string:reply_id>')
    curr_api.add_resource(reactions.Reactions, '/reactions')


def register_extensions(app):
    api.init_app(app)


def register_error_handlers(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return {"message": "resource doesn't exist"}, 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return {"message": "internal server error, most likely because of parameters of incorrect length or type"}, 500


def register_response_wrappers(app, config):
    @app.after_request
    def apply_headers(response):
        response.headers['Access-Control-Allow-Origin'] = config.ALLOWED_ORIGINS
        response.headers["Access-Control-Allow-Methods"] = config.ALLOWED_METHODS
        response.headers["Access-Control-Allow-Headers"] = config.ALLOWED_HEADERS
        response.headers["Access-Control-Expose-Headers"] = config.EXPOSED_HEADERS
        response.headers["Content-Type"] = "application/json"
        return response


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_resources(api)
    register_extensions(app)
    register_response_wrappers(app, config)
    register_error_handlers(app)
    return app
