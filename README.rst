Flask-Mixer
###########

Flask-Mixer is simply application for generate instances of SQLAlchemy models. It's useful for testing.
Fast and convenient test-data generation.

Flask-Mixer is in early development.

.. image:: https://secure.travis-ci.org/klen/Flask-Mixer.png?branch=develop
    :target: http://travis-ci.org/klen/Flask-Mixer
    :alt: Build Status

.. contents::

Requirements
=============

- python >= 2.6
- Flask >= 0.8
- Flask-SQLAlchemy>=0.16


Installation
=============

**Flask-Mixer** should be installed using pip: ::

    pip install Flask-Mixer


Usage
=====

Example: ::

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


        mixer = Mixer(app)

        with app.test_request_context():
            db.create_all()

            # Simple model generation
            user1 = mixer.blend(User)
            assert user1.id and user1.username and user1.created_at
            assert user1.score == 50
            assert user.profile.user == user

            # Generate model with some values
            user2 = mixer.blend(User, username='test')
            assert user2.username == 'test'

            # Model would be defined as string
            role1 = mixer.blend('app.models.Role')
            assert role1.user
            assert role1.user_id == role1.user.id

            # Generate model with reference
            role1 = mixer.blend(Role, user__username='test2')
            assert role2.user.username == 'test2'

            # Set related values from db by random
            profiles = Profile.query.all()
            # (Use model class as value)
            user = mixer.blend(User, profile=Profile)
            assert user.profile in profiles

            db.session.commit()


Bug tracker
===========

If you have any suggestions, bug reports or
annoyances please report them to the issue tracker
at https://github.com/klen/Flask-Mixer/issues


Contributing
============

Development of adrest happens at github: https://github.com/klen/Flask-Mixer


Contributors
=============

* klen_ (Kirill Klenov)


License
=======

Licensed under a `GNU lesser general public license`_.


.. _GNU lesser general public license: http://www.gnu.org/copyleft/lesser.html
.. _klen: http://klen.github.com/

