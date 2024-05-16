import unittest
from app import create_app, db
from models import User

class TestDB(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            # Create a test user
            test_user = User(username='testuser', email='testuser@example.com')
            test_user.set_password('correctpassword')
            db.session.add(test_user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_add_user(self):
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)

    def test_get_user(self):
        user = User.query.filter_by(username='testuser').first()
        self.assertEqual(user.username, 'testuser')

    def test_remove_user(self):
        user = User.query.filter_by(username='testuser').first()
        db.session.delete(user)
        db.session.commit()
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNone(user)

if __name__ == '__main__':
    unittest.main()
