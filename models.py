from extensions import extension_db as db
from uuid import uuid4


class BaseModel:
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Post(db.Model, BaseModel):
    __tablename__ = 'posts'
    post_id = db.Column(db.CHAR(36), primary_key=True, default=uuid4)
    title = db.Column(db.VARCHAR(150), nullable=False)
    body = db.Column(db.VARCHAR(15000), nullable=False)
    date = db.Column(db.DATETIME, nullable=False, server_default='CURRENT_TIMESTAMP')
    author_id = db.Column(db.ForeignKey('users.user_id'))
    number_of_replies = db.Column(db.INTEGER, nullable=False, default=0)

    def __repr__(self):
        return '<Post %r>' % self.post_id


class User(db.Model, BaseModel):
    __tablename__ = 'users'
    user_id = db.Column(db.CHAR(36), primary_key=True, default=uuid4)
    username = db.Column(db.VARCHAR(45), nullable=False, unique=True)
    email = db.Column(db.VARCHAR(355), nullable=False, unique=True)
    password = db.Column(db.BLOB, nullable=False)
    date = db.Column(db.DATETIME, nullable=False, server_default='CURRENT_TIMESTAMP')
    settings = db.Column(db.JSON, nullable=False)
    permission_level = db.Column(db.INTEGER, nullable=False, default=1)

    def __repr__(self):
        return '<User %r>' % self.user_id


class PostReply(db.Model, BaseModel):
    __tablename__ = 'post_replies'
    reply_id = db.Column(db.CHAR(36), primary_key=True, default=uuid4)
    body = db.Column(db.VARCHAR(10000), nullable=False)
    date = db.Column(db.DATETIME, nullable=False, server_default='CURRENT_TIMESTAMP')
    author_id = db.Column(db.CHAR(36), db.ForeignKey('users.user_id'))
    post_id = db.Column(db.CHAR(36), db.ForeignKey('posts.post_id'))

    def __repr__(self):
        return '<PostReply %r>' % self.reply_id
