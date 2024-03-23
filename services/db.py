from itertools import groupby
from extensions import request_db_connection
from MySQLdb.cursors import DictCursor
from config import config


def fetch_result(fetch_all, mapper=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            with request_db_connection() as connection:
                cursor = connection.cursor(cursorclass=DictCursor)
                func(cursor, *args, **kwargs)
                if fetch_all:
                    result = cursor.fetchall()
                elif fetch_all is False:
                    result = cursor.fetchone()
                else:
                    result = None

                if mapper:
                    result = mapper(result)
                return result
        return wrapper
    return decorator

cursor = extension_db.cursor(cursorclass=DictCursor)


posts_per_page = config.NUMBER_OF_POST_PAGES
replies_per_page = config.NUMBER_OF_REPLY_PAGES
notifications_per_page = config.NUMBER_OF_NOTIFICATION_PAGES


def group_reactions(reactions):
    if reactions and 'reaction_name' in reactions[0].keys():
        return {key: list(value) for key, value in groupby(reactions, lambda x: x["reaction_name"])}
    return reactions


@fetch_result(False)
def create_post(cursor, author_id, title, body, is_pinned):
    cursor.callproc('create_post', (author_id, title, body, int(bool(is_pinned))))


@fetch_result(True)
def get_paginated_posts(cursor, page, sort_column):
    cursor.callproc('get_paginated_posts', (page, posts_per_page, sort_column))


@fetch_result(True)
def search_paginated_posts(cursor, search_query, page, sort_column):
    cursor.callproc('search_paginated_posts', (search_query, page, posts_per_page, sort_column))


@fetch_result(False)
def get_number_of_posts(cursor):
    cursor.callproc('get_number_of_posts')


@fetch_result(False)
def get_number_of_searched_posts(cursor, search_query):
    cursor.callproc('get_number_of_searched_posts', (search_query,))


@fetch_result(False)
def get_number_of_post_replies(cursor, post_id):
    cursor.callproc('get_number_of_post_replies', (post_id,))


@fetch_result(False)
def get_post(cursor, post_id):
    cursor.callproc('get_post', (post_id,))


@fetch_result(None)
def edit_post(cursor, post_id, title, body, is_pinned, **kwargs):
    cursor.callproc('edit_post', (post_id, title, body, int(bool(is_pinned))))


@fetch_result(None)
def delete_post(cursor, post_id):
    cursor.callproc('delete_post', (post_id,))


@fetch_result(False)
def get_user(cursor, user_id):
    cursor.callproc('get_user', (user_id,))


@fetch_result(None)
def edit_user(cursor, user_id, username, email, password, settings, permission_level, pfp_link, **kwargs):
    cursor.callproc('edit_user', (user_id, username, email, password, settings, permission_level, pfp_link))


@fetch_result(False)
def get_user_by_email(cursor, email):
    cursor.callproc('get_user_by_email', (email,))


@fetch_result(False)
def get_user_by_username(cursor, username):
    cursor.callproc('get_user_by_username', (username,))


@fetch_result(False)
def create_user(cursor, username, email, hashed_pw, pfp_link):
    cursor.callproc('create_user', (username, email, hashed_pw, pfp_link))


@fetch_result(False)
def get_post_reply(cursor, reply_id):
    cursor.callproc('get_post_reply', (reply_id,))


@fetch_result(True)
def get_paginated_post_replies(cursor, post_id, page, sort_column):
    cursor.callproc('get_paginated_post_replies', (post_id, page, replies_per_page, sort_column))


@fetch_result(False)
def create_post_reply(cursor, post_id, author_id, body):
    cursor.callproc('create_post_reply', (post_id, author_id, body))


@fetch_result(None)
def edit_post_reply(cursor, reply_id, body):
    cursor.callproc('edit_post_reply', (reply_id, body))


@fetch_result(None)
def delete_post_reply(cursor, reply_id):
    cursor.callproc('delete_post_reply', (reply_id,))


@fetch_result(False)
def create_post_reaction(cursor, reaction_id, post_id, creator_id):
    cursor.callproc('create_post_reaction', (reaction_id, post_id, creator_id))


@fetch_result(False)
def create_reply_reaction(cursor, reaction_id, reply_id, creator_id):
    cursor.callproc('create_reply_reaction', (reaction_id, reply_id, creator_id))


@fetch_result(None)
def delete_reply_reaction(cursor, reaction_id):
    cursor.callproc('delete_reply_reaction', (reaction_id,))


@fetch_result(None)
def delete_post_reaction(cursor, reaction_id):
    cursor.callproc('delete_post_reaction', (reaction_id,))


@fetch_result(True, mapper=lambda result: group_reactions(result))
def get_reply_reactions(cursor, reply_id):
    cursor.callproc('get_reply_reactions', (reply_id,))


@fetch_result(True, mapper=lambda result: group_reactions(result))
def get_post_reactions(cursor, post_id):
    cursor.callproc('get_post_reactions', (post_id,))


@fetch_result(True)
def get_reactions(cursor):
    cursor.callproc('get_reactions', ())


@fetch_result(False)
def get_reaction(cursor, reaction_id):
    cursor.callproc('get_reaction', (reaction_id,))


@fetch_result(False)
def get_post_reaction(cursor, reaction_id):
    cursor.callproc('get_post_reaction', (reaction_id,))


@fetch_result(False)
def get_reply_reaction(cursor, reaction_id):
    cursor.callproc('get_reply_reaction', (reaction_id,))


@fetch_result(False)
def get_user_post_reaction(cursor, user_id, post_id):
    cursor.callproc('get_user_post_reaction', (user_id, post_id))


@fetch_result(False)
def get_user_reply_reaction(cursor, user_id, post_id):
    cursor.callproc('get_user_reply_reaction', (user_id, post_id))


@fetch_result(None)
def create_post_notification(cursor, user_id, author_id, post_id, notification_body):
    cursor.callproc('create_post_notification', (user_id, author_id, post_id, notification_body,))


@fetch_result(None)
def create_reply_notification(cursor, user_id, author_id, post_id, reply_id, notification_body):
    cursor.callproc('create_reply_notification', (user_id, author_id, post_id, reply_id, notification_body,))


@fetch_result(False)
def get_notification(cursor, notification_id):
    cursor.callproc('get_notification', (notification_id,))


@fetch_result(None)
def edit_notification_is_read(cursor, notification_id, is_read):
    cursor.callproc('edit_notification_is_read', (notification_id, int(bool(is_read))))


@fetch_result(None)
def delete_notification(cursor, notification_id):
    cursor.callproc('delete_notification', (notification_id,))


@fetch_result(True)
def get_paginated_user_notifications(cursor, user_id, page):
    cursor.callproc('get_paginated_user_notifications', (user_id, page, notifications_per_page))


@fetch_result(False)
def get_number_of_user_notifications(cursor, user_id):
    cursor.callproc('get_number_of_user_notifications', (user_id,))


@fetch_result(False)
def get_number_of_unread_user_notifications(cursor, user_id):
    cursor.callproc('get_number_of_unread_user_notifications', (user_id,))


@fetch_result(None)
def mark_user_notifications_as_read(cursor, user_id):
    cursor.callproc('mark_user_notifications_as_read', (user_id,))

