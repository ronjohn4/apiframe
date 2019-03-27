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
        # create test users
        u1 = User(username='john', email='john@example.com', active=True, about_me='about me text1')
        u2 = User(username='susan', email='susan@example.com', active=False, about_me='about me text2')

        db.session.add_all([u1, u2])

        self.assertEqual(u1, u1)
        self.assertNotEqual(u1, u2)

    def test_user_saved_attributes(self):
        # create test user
        u1 = User(username='john', email='john@example.com', active=True, about_me='about me text1')

        db.session.add(u1)

        u3 = User.find_by_username(u1.username)
        self.assertEqual(u3.active, u1.active)
        self.assertEqual(u3.username, u1.username)
        self.assertEqual(u3.email, u1.email)
        self.assertEqual(u3.about_me, u1.about_me)

    def test_user_security(self):
        u1 = User(username='john', email='john@example.com')
        u1.set_password('Test1Passw0rd!')

        db.session.add(u1)

        self.assertTrue(u1.check_password('Test1Passw0rd!'))
        self.assertFalse(u1.check_password('test1Passw0rd!'))

    # def test_user_always_fails(self):
    #     self.assertEqual(1, 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
