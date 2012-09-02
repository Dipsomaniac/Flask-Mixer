.. _quickstart:

Quickstart
==========

.. currentmodule:: flask.ext.mixer

Flask-Mixer is easy to use and realy fun for testing applications.  For the complete guide, checkout out the API documentation on the :class:`Mixer` class.


Base example
------------
::

        from flask import Flask
        from flask.ext.mixer import Mixer
        from flask.ext.sqlalchemy import SQLAlchemy
        from datetime import datetime

        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db = SQLAlchemy()
        db.init_app(app)

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

        class Profile(db.Model):
            __tablename__ = 'profile'
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String(20), nullable=False)
            user = db.relationship("User", uselist=False, backref="profile")


        mixer = Mixer(app, session_commit=True)

        with app.test_request_context():
            db.create_all()

            # Simple model generation
            user1 = mixer.blend(User)
            assert user1.id and user1.username and user1.created_at
            assert user1.score == 50
            assert user.profile.user == user

            # Model would be defined as string
            role1 = mixer.blend('app.models.Role')
            assert role1.user
            assert role1.user_id == role1.user.id


Blend models with values
------------------------
::

            # Generate model with some values
            user2 = mixer.blend(User, username='test')
            assert user2.username == 'test'

            # Generate model with reference
            role1 = mixer.blend(Role, user__username='test2')
            assert role2.user.username == 'test2'

            # Value can be callable
            user = mixer.blend(User, username=lambda:'callable_value')
            assert user.username == 'callable_value'


Set values from db
------------------
::

            # Set related values from db by random
            profiles = Profile.query.all()
            user = mixer.blend(User, profile=mixer.random)
            assert user.profile in profiles

            # By default, column with defvalue will be to init as them
            # but you can still force set it to random value
            user = mixer.blend(User, score=mixer.random)
            assert user.score != 50

