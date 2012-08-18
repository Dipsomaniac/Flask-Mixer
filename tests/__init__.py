from unittest import TestCase


class BaseTest(TestCase):

    def test_mixer(self):
        from flask import Flask
        from flask_mixer import Mixer
        from .models import db, User, Profile

        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.init_app(app)
        mixer = Mixer(app, session_commit=True)

        with app.test_request_context():

            db.create_all()

            role = mixer.blend('tests.models.Role')
            self.assertTrue(role.user)
            self.assertEqual(role.user_id, role.user.id)

            user = mixer.blend(User)
            self.assertTrue(user.id)
            self.assertTrue(user.username)
            self.assertEqual(user.score, 50)
            self.assertTrue(user.created_at)
            self.assertTrue(user.profile)
            self.assertEqual(user.profile.user, user)

            user = mixer.blend(User, username='test')
            self.assertEqual(user.username, 'test')

            role = mixer.blend('tests.models.Role', user__username='test2')
            self.assertEqual(role.user.username, 'test2')

            profile = mixer.blend('tests.models.Profile')
            user = mixer.blend(User, profile=profile)
            self.assertEqual(user.profile, profile)

            profiles = Profile.query.all()
            user = mixer.blend(User, profile=mixer.random)
            self.assertTrue(user.profile in profiles)

            user = mixer.blend(User, score=mixer.random)
            self.assertNotEqual(user.score, 50)

            user = mixer.blend(User, username=lambda: 'callable_value')
            self.assertEqual(user.username, 'callable_value')
