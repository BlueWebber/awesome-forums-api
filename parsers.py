from flask_restful import reqparse
from wtforms import ValidationError
from config import config

lens = config.MAX_LENS_MAP


def max_length(max_len, help_str):
    def validate(s):
        if len(s) < max_len:
            return s
        raise ValidationError(f"{help_str} must be shorter than {max_len} characters")
    return validate


new_post_parser = reqparse.RequestParser()
new_post_parser.add_argument('title', type=max_length(lens["title"], help_str="title"), required=True)
new_post_parser.add_argument('body', type=max_length(lens["body"], help_str="body"), required=True)

patch_post_parser = reqparse.RequestParser()
patch_post_parser.add_argument('title', type=max_length(lens["title"], help_str="title"))
patch_post_parser.add_argument('body', type=max_length(lens["body"], help_str="body"))

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str, required=True)
login_parser.add_argument('password', type=str, required=True)

register_parser = reqparse.RequestParser()
register_parser.add_argument('username', type=max_length(lens["username"], help_str="username"),
                             required=True)
register_parser.add_argument('email', type=max_length(lens["email"], help_str="email"), required=True)
register_parser.add_argument('password', type=max_length(lens["password"], help_str="password"), required=True)
register_parser.add_argument('pfp_base64', type=max_length(((config.MAX_IMAGE_SIZE_SIZE * 4) / 3),
                                                           help_str="pfp_base64"))

new_post_reply_parser = reqparse.RequestParser()
new_post_reply_parser.add_argument('body', type=max_length(lens["body"], help_str="body"),
                                   required=True)

image_upload_parser = reqparse.RequestParser()
image_upload_parser.add_argument('img_base64', type=max_length(((config.MAX_IMAGE_SIZE_SIZE * 4) / 3),
                                                               help_str="img_base64"), required=True)

patch_user_parser = reqparse.RequestParser()
patch_user_parser.add_argument('username', type=max_length(lens["username"], help_str="username"))
patch_user_parser.add_argument('email', type=max_length(lens["email"], help_str="email"))
patch_user_parser.add_argument('password', type=max_length(lens["password"], help_str="password"))
patch_user_parser.add_argument('settings', type=dict)
patch_user_parser.add_argument('pfp_base64', type=max_length(((config.MAX_IMAGE_SIZE_SIZE * 4) / 3),
                                                             help_str="pfp_base64"))
