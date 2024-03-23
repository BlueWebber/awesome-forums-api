from flask_restful import reqparse
from wtforms import ValidationError
import models


def max_length(max_len, help_str):
    def validate(s):
        if len(s) < max_len:
            return s
        raise ValidationError(f"{help_str} must be shorter than {max_len} characters")
    return validate


new_post_parser = reqparse.RequestParser()
new_post_parser.add_argument('title', type=max_length(models.Post.title.type.length, help_str="title"), required=True)
new_post_parser.add_argument('body', type=max_length(models.Post.body.type.length, help_str="body"), required=True)

patch_post_parser = reqparse.RequestParser()
patch_post_parser.add_argument('title', type=max_length(models.Post.title.type.length, help_str="title"))
patch_post_parser.add_argument('body', type=max_length(models.Post.body.type.length, help_str="body"))

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str, required=True)
login_parser.add_argument('password', type=str, required=True)

register_parser = reqparse.RequestParser()
register_parser.add_argument('username', type=max_length(models.User.username.type.length, help_str="username"),
                             required=True)
register_parser.add_argument('email', type=max_length(models.User.email.type.length, help_str="email"), required=True)
register_parser.add_argument('password', type=max_length(1000, help_str="password"), required=True)

new_post_reply_parser = reqparse.RequestParser()
new_post_reply_parser.add_argument('body', type=max_length(models.PostReply.body.type.length, help_str="body"),
                                   required=True)
