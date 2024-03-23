import models
from extensions import extension_db as db
from utils.filters import remove_unnecessary_user_data
from utils.serializer import serialize


def create_post(author_id, title, body):
    result = models.Post(title=title, body=body, author_id=author_id)
    db.session.add(result)
    db.session.commit()
    return get_post(result.post_id)


@remove_unnecessary_user_data
@serialize
def get_paginated_posts(page, posts_per_page):
    return models.Post.query.join(models.User).filter(
        models.User.user_id == models.Post.author_id
    ).offset(page * posts_per_page).limit(posts_per_page).all()


def get_number_of_posts():
    return models.Post.query.count()


@remove_unnecessary_user_data
@serialize
def get_post(post_id):
    return db.session.query(models.Post, models.User).filter(models.Post.author_id == models.User.user_id).filter(
        models.Post.post_id == post_id
    ).one_or_none()


def patch_post(post_id, **kwargs):
    # kwargs are title and body
    post = models.Post.query.filter(models.Post.post_id == post_id).one_or_none()
    [setattr(post, key, val) for key, val in kwargs.items() if val]
    db.session.commit()


def delete_post(post_id):
    models.Post.query.filter(models.Post.post_id == post_id).delete()
    db.session.commit()


@serialize
def get_user(user_id):
    return models.User.query.filter(models.User.user_id == user_id).one_or_none()


@serialize
def get_user_by_email(email):
    return models.User.query.filter(models.User.email == email).one_or_none()


@serialize
def get_user_by_username(username):
    return models.User.query.filter(models.User.username == username).one_or_none()


@serialize
def create_user(username, email, hashed_pw):
    user = models.User(username=username, email=email, password=hashed_pw, settings={})
    db.session.add(user)
    db.session.commit()
    return user


@remove_unnecessary_user_data
@serialize
def get_post_reply(reply_id):
    return models.PostReply.query.join(models.User).filter(
        models.PostReply.author_id == models.User.user_id).filter(models.PostReply.reply_id == reply_id).all()


@remove_unnecessary_user_data
@serialize
def get_paginated_post_replies(post_id, page, replies_per_page):
    return models.PostReply.query.join(models.User).filter(
        models.User.user_id == models.PostReply.author_id
    ).filter(models.PostReply.post_id == post_id).offset(page * replies_per_page).limit(replies_per_page).all()


def create_post_reply(post_id, author_id, body):
    reply = models.PostReply(post_id=post_id, author_id=author_id, body=body)
    db.session.add(reply)
    db.session.commit()
    return get_post_reply(reply.reply_id)


def edit_post_reply(reply_id, body):
    reply = models.PostReply.query.filter(models.PostReply.reply_id == reply_id).one_or_none()
    reply.body = body
    db.session.commit()


def delete_post_reply(reply_id):
    models.PostReply.query.filter(models.PostReply.reply_id == reply_id).delete()
    db.session.commit()
