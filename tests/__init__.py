from unittest import TestCase


class BaseTest(TestCase):

    def test_mixer(self):
        from flask import Flask
        from flask_mixer import Mixer
        from .models import db, User

        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.init_app(app)
        mixer = Mixer(app)

        with app.test_request_context():
            db.create_all()

            role = mixer.blend('tests.models.Role')
            user = mixer.blend(User)
            user2 = mixer.blend(User, username='test')
            role2 = mixer.blend('tests.models.Role', user__username='test2')
            db.session.commit()

            self.assertEqual(user.score, 50)
            self.assertTrue(user.created_at)
            self.assertTrue(role.user)
            self.assertEqual(role.user_id, role.user.id)
            self.assertEqual(role2.user.username, 'test2')
            self.assertTrue(user.id)
            self.assertTrue(user.username)
            self.assertEqual(user2.username, 'test')
