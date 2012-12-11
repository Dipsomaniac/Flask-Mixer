from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

usermessages = db.Table(
    'users_usermessages',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('message_id', db.Integer, db.ForeignKey('message.id'))
)


class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    user = db.relationship("User", uselist=False, backref="profile")


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.SmallInteger, default=50, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)

    messages = db.relationship("Message", secondary=usermessages, backref="users")


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    user = db.relation(User)


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)


class Node(db.Model):
    __tablename__ = 'node'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    children = db.relation(
        'Node',
        cascade='all',
        backref=db.backref('parent', remote_side='Node.id'))
