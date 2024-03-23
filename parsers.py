from flask_restful import reqparse
from wtforms import ValidationError
from config import config
from utils.validators import validate_username, validate_email

lens = config.LENS_MAP


def length(min_len, max_len, help_str, with_strip=False, validator=None, validator_help_str=None):
    abs_len = max_len if min_len == max_len else None

    def validate(s):
        str_length = len(s)
        if abs_len and str_length != abs_len:
            raise ValidationError(f"{help_str} must be {max_len} characters long")
        if str_length > max_len:
            raise ValidationError(f"{help_str} must be shorter than {max_len} characters")
        if str_length < min_len:
            raise ValidationError(f"{help_str} must be longer than {min_len} characters")
        if with_strip:
            s = " ".join(s.split())
        if callable(validator):
            if not validator(s):
                raise ValidationError(f"{help_str} {validator_help_str}")
        return s
    return validate


new_post_parser = reqparse.RequestParser()
new_post_parser.add_argument('title', type=length(*lens["title"], help_str="title", with_strip=True), required=True)
new_post_parser.add_argument('body', type=length(*lens["body"], help_str="body", with_strip=True), required=True)

patch_post_parser = reqparse.RequestParser()
patch_post_parser.add_argument('title', type=length(*lens["title"], help_str="title", with_strip=True))
patch_post_parser.add_argument('body', type=length(*lens["body"], help_str="body", with_strip=True))

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str, required=True)
login_parser.add_argument('password', type=str, required=True)

register_parser = reqparse.RequestParser()
register_parser.add_argument('username', type=length(*lens["username"], help_str="username",
                             validator=validate_username, validator_help_str="must be alphanumeric"),
                             required=True)
register_parser.add_argument('email', type=length(*lens["email"], help_str="email",
                             validator=validate_email, validator_help_str="is not a valid email"), required=True)
register_parser.add_argument('password', type=length(*lens["password"], help_str="password"), required=True)
register_parser.add_argument('pfp_base64', type=length(0, ((config.MAX_IMAGE_SIZE * 4) / 3), help_str="pfp_base64"))

new_post_reply_parser = reqparse.RequestParser()
new_post_reply_parser.add_argument('body', type=length(*lens["body"], help_str="body", with_strip=True),
                                   required=True)

upload_parser = reqparse.RequestParser()
upload_parser.add_argument('content_base64', type=str, required=True)
upload_parser.add_argument('content_type', type=str, required=True)

patch_user_parser = reqparse.RequestParser()
patch_user_parser.add_argument('username', type=length(*lens["username"], help_str="username",
                               validator=validate_username, validator_help_str="must be alphanumeric"))
patch_user_parser.add_argument('email', type=length(*lens["email"], help_str="email",
                               validator=validate_email, validator_help_str="is not a valid email"))
patch_user_parser.add_argument('password', type=length(*lens["password"], help_str="password"))
patch_user_parser.add_argument('settings', type=dict)
patch_user_parser.add_argument('pfp_base64', type=length(0, ((config.MAX_IMAGE_SIZE * 4) / 3), help_str="pfp_base64"))

reaction_parser = reqparse.RequestParser()
reaction_parser.add_argument('reaction_type_id', type=length(*lens["id"], help_str="reaction_type_id"), required=True)
