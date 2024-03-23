import re
from flask import abort
from itertools import zip_longest

email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")


def validate_email(email):
    return bool(email_regex.match(email))


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
