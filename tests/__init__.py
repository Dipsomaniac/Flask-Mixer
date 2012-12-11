from unittest import TestCase


class BaseTest(TestCase):

    def test_mixer(self):
        from flask import Flask
        from flask_mixer import Mixer
        from .models import db, User

        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.init_app(app)
        mixer = Mixer(session_commit=True)
        mixer.init_app(app)

        with app.test_request_context():

            db.create_all()

            node = mixer.blend('tests.models.Node')
            self.assertTrue(node.id)
            self.assertFalse(node.parent)

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

            users = User.query.all()
            role = mixer.blend('tests.models.Role', user=mixer.random)
            self.assertTrue(role.user in users)

            profile = mixer.blend('tests.models.Profile')
            user = mixer.blend(User, profile=profile)
            self.assertEqual(user.profile, profile)

            user = mixer.blend(User, score=mixer.random)
            self.assertNotEqual(user.score, 50)

            user = mixer.blend(User, username=lambda: 'callable_value')
            self.assertEqual(user.username, 'callable_value')
