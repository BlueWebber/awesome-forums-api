from utils.getters import fetch_result
from extensions import extension_db
from MySQLdb.cursors import DictCursor


cursor = extension_db.cursor(cursorclass=DictCursor)


@fetch_result(cursor.fetchone, cursor.nextset)
def create_post(author_id, title, body):
    cursor.callproc('create_post', (author_id, title, body))


@fetch_result(cursor.fetchall, cursor.nextset)
def get_paginated_posts(page, posts_per_page, sort_column):
    cursor.callproc('get_paginated_posts', (page, posts_per_page, sort_column))


@fetch_result(cursor.fetchone, cursor.nextset)
def get_number_of_posts():
    cursor.callproc('get_number_of_posts')


@fetch_result(cursor.fetchone, cursor.nextset)
def get_post(post_id):
    cursor.callproc('get_post', (post_id,))


def edit_post(post_id, title, body):
    cursor.callproc('edit_post', (post_id, title, body))


def delete_post(post_id):
    cursor.callproc('delete_post', (post_id,))


@fetch_result(cursor.fetchone, cursor.nextset)
def get_user(user_id):
    cursor.callproc('get_user', (user_id,))


@fetch_result(cursor.fetchone, cursor.nextset)
def edit_user(user_id, username, email, password, settings, permission_level, pfp_link, **kwargs):
    cursor.callproc('edit_user', (user_id, username, email, password, settings, permission_level, pfp_link))


@fetch_result(cursor.fetchone, cursor.nextset)
def get_user_by_email(email):
    cursor.callproc('get_user_by_email', (email,))


@fetch_result(cursor.fetchone, cursor.nextset)
def get_user_by_username(username):
    cursor.callproc('get_user_by_username', (username,))


@fetch_result(cursor.fetchone, cursor.nextset)
def create_user(username, email, hashed_pw, pfp_link):
    cursor.callproc('create_user', (username, email, hashed_pw, pfp_link))


@fetch_result(cursor.fetchone, cursor.nextset)
def get_post_reply(reply_id):
    cursor.callproc('get_post_reply', (reply_id,))


@fetch_result(cursor.fetchall, cursor.nextset)
def get_paginated_post_replies(post_id, page, replies_per_page, sort_column):
    cursor.callproc('get_paginated_post_replies', (post_id, page, replies_per_page, sort_column))


@fetch_result(cursor.fetchone, cursor.nextset)
def create_post_reply(post_id, author_id, body):
    cursor.callproc('create_post_reply', (post_id, author_id, body))


def edit_post_reply(reply_id, body):
    cursor.callproc('edit_post_reply', (reply_id, body))


def delete_post_reply(reply_id):
    cursor.callproc('delete_post_reply', (reply_id,))


@fetch_result(cursor.fetchall, cursor.nextset)
def create_post_reaction(reaction_id, post_id, creator_id):
    cursor.callproc('create_post_reaction', (reaction_id, post_id, creator_id))


@fetch_result(cursor.fetchall, cursor.nextset)
def create_reply_reaction(reaction_id, reply_id, creator_id):
    cursor.callproc('create_reply_reaction', (reaction_id, reply_id, creator_id))


def delete_reply_reaction(reaction_id):
    cursor.callproc('delete_reply_reaction', (reaction_id,))


def delete_post_reaction(reaction_id):
    cursor.callproc('delete_post_reactions', (reaction_id,))


@fetch_result(cursor.fetchall, cursor.nextset)
def get_reply_reactions(reply_id):
    cursor.callproc('get_reply_reactions', (reply_id,))


@fetch_result(cursor.fetchall, cursor.nextset)
def get_post_reactions(post_id):
    cursor.callproc('get_post_reactions', (post_id,))
