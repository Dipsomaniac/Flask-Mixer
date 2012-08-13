from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, default=50, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    username = db.Column(db.String(20), nullable=False)


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    user = db.relation(User)
