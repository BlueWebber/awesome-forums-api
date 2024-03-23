from sqlalchemy.inspection import inspect
from datetime import datetime
from sqlalchemy.engine.row import Row


def serialize(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print('call from', func)
        if isinstance(result, list):
            return serialize_list(result)
        if isinstance(result, Row):
            return serialize_joined(result)
        return serialize_obj(result)
    return wrapper


def serialize_obj(obj):
    print('serialize_obj')
    if not obj:
        return
    result = {}
    if isinstance(obj, dict):
        return obj
    for attr in inspect(obj).attrs.keys():
        attribute = getattr(obj, attr)
        if isinstance(attribute, datetime):
            attribute = str(attribute)
        result[attr] = attribute
    return result


def serialize_joined(tup):
    print('serialize_joined')
    result = {}
    for i in tup:
        result.update(i.as_dict())
    return result


def serialize_list(target_list):
    print('serialize_list')
    if isinstance(target_list[0], Row):
        return [serialize_joined(tup) for tup in target_list]
    return [serialize_obj(m) for m in target_list]
