import re
from flask import abort
from itertools import zip_longest
from services.media import ByteImage, ByteVideo
from config import config

email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
username_regex = re.compile(r"\W")


def validate_email(email):
    return bool(email_regex.match(email))


def validate_username(username):
    return not username_regex.findall(username)


def validate_and_upload_pfp(base_64_str):
    try:
        img = ByteImage(base_64_str, config.PFP_IMAGE_FORMAT)
        if not round(img.aspect_ratio, 0) == 1:
            print("wrong ratio")
            return False
        if img.size != config.PFP_SIZE:
            img.resize()
        result = img.upload()
    except (AssertionError, RuntimeError) as ex:
        print(ex)
        return False
    else:
        return result


def validate_and_upload_media(media_type, base_64_str):
    try:
        result = None
        if media_type == "image":
            img = ByteImage(base_64_str, config.PFP_IMAGE_FORMAT)
            result = img.upload()
        elif media_type == "video":
            vid = ByteVideo(base_64_str)
            result = vid.upload()
    except (AssertionError, RuntimeError):
        return False
    else:
        return result


def validate_and_inject(queries):
    def decorator(func):
        def wrapper(**kwargs):
            if not kwargs:
                return abort(404, "Invalid arguments")
            result = []
            for query, arg in zip_longest(queries, kwargs.values()):
                if query:
                    item = query(arg)
                    if not item:
                        return abort(404, "arguments don't exist on DB")
                    result.append(item)
                else:
                    result.append(arg)
            return func(*result)
        return wrapper
    return decorator
