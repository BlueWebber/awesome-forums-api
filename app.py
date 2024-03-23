from flask import Flask
from extensions import api
from resources import (posts, post, post_replies, post_reply, auth, users, upload, refresh, post_reactions,
                       reply_reactions, reactions)


def register_resources(curr_api):
    curr_api.add_resource(posts.Posts, '/posts/<string:sort_column>/<int:page_number>/')
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


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_resources(api)
    register_extensions(app)
    return app
