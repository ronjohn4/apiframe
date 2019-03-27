import unittest
from app import create_app, db
from app.models import User
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user(self):
        # create four users
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')

        db.session.add_all([u1, u2])

        self.assertEqual(u1, u1)
        self.assertNotEqual(u1, u2)

    def test_user_always_fails(self):
        self.assertEqual(1, 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
