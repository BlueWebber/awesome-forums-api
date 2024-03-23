from flask_restful import reqparse
from wtforms import ValidationError
from config import config

lens = config.LENS_MAP


def length(min_len, max_len, help_str):
    abs_len = max_len if min_len == max_len else None

    def validate(s):
        str_length = len(s)
        if abs_len and str_length != abs_len:
            raise ValidationError(f"{help_str} must be {max_len} characters long")
        if str_length > max_len:
            raise ValidationError(f"{help_str} must be shorter than {max_len} characters")
        if str_length < min_len:
            raise ValidationError(f"{help_str} must be longer than {min_len} characters")
        return s
    return validate


new_post_parser = reqparse.RequestParser()
new_post_parser.add_argument('title', type=length(*lens["title"], help_str="title"), required=True)
new_post_parser.add_argument('body', type=length(*lens["body"], help_str="body"), required=True)

patch_post_parser = reqparse.RequestParser()
patch_post_parser.add_argument('title', type=length(*lens["title"], help_str="title"))
patch_post_parser.add_argument('body', type=length(*lens["body"], help_str="body"))

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str, required=True)
login_parser.add_argument('password', type=str, required=True)

register_parser = reqparse.RequestParser()
register_parser.add_argument('username', type=length(*lens["username"], help_str="username"),
                             required=True)
register_parser.add_argument('email', type=length(*lens["email"], help_str="email"), required=True)
register_parser.add_argument('password', type=length(*lens["password"], help_str="password"), required=True)
register_parser.add_argument('pfp_base64', type=length(0, ((config.MAX_IMAGE_SIZE * 4) / 3), help_str="pfp_base64"))

new_post_reply_parser = reqparse.RequestParser()
new_post_reply_parser.add_argument('body', type=length(*lens["body"], help_str="body"),
                                   required=True)

upload_parser = reqparse.RequestParser()
upload_parser.add_argument('content_base64', type=str, required=True)
upload_parser.add_argument('content_type', type=str, required=True)

patch_user_parser = reqparse.RequestParser()
patch_user_parser.add_argument('username', type=length(*lens["username"], help_str="username"))
patch_user_parser.add_argument('email', type=length(*lens["email"], help_str="email"))
patch_user_parser.add_argument('password', type=length(*lens["password"], help_str="password"))
patch_user_parser.add_argument('settings', type=dict)
patch_user_parser.add_argument('pfp_base64', type=length(0, ((config.MAX_IMAGE_SIZE * 4) / 3), help_str="pfp_base64"))

reaction_parser = reqparse.RequestParser()
reaction_parser.add_argument('reaction_type_id', type=length(*lens["id"], help_str="reaction_type_id"), required=True)
