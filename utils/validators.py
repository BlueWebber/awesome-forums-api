import re
from flask import abort
from itertools import zip_longest
from utils.media import Image
from config import config

email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
username_regex = re.compile(r"\W")


def validate_email(email):
    return bool(email_regex.match(email))


def validate_username(username):
    return not username_regex.findall(username)


def validate_and_upload_pfp(base_64_str):
    img = Image(base_64_str, config.PFP_IMAGE_FORMAT)
    if 'image' not in dir(img) or not round(img.aspect_ratio, 0) == 1:
        return False
    if img.image.size != config.PFP_SIZE:
        img.resize()
    return img.upload()


def validate_and_inject(queries):
    def decorator(func):
        def wrapper(**kwargs):
            if not kwargs:
                return abort(404)
            result = []
            for query, arg in zip_longest(queries, kwargs.values()):
                if query:
                    item = query(arg)
                    if not item:
                        return abort(404)
                    result.append(item)
                else:
                    result.append(arg)
            return func(*result)
        return wrapper
    return decorator
