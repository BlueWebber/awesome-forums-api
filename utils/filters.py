def remove_unnecessary_user_data(func):
    def remove_fields(user):
        del user['user_id']
        del user['email']
        del user['password']
        del user['settings']
        del user['date']
        return user

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if not result:
            return
        if isinstance(result, list):
            return [remove_fields(i) for i in result]
        return remove_fields(result)
    return wrapper
