import unittest
from app import create_app, db
from models import User

class TestDB(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        user = User(username='testuser', email='testuser@example.com', password_hash='testpassword')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_user(self):
        with self.app.app_context():
            user = User.query.filter_by(username='testuser').first()
            self.assertIsNotNone(user)

    def test_get_user(self):
        with self.app.app_context():
            user = User.query.filter_by(username='testuser').first()
            self.assertEqual(user.username, 'testuser')

    def test_remove_user(self):
        with self.app.app_context():
            user = User.query.filter_by(username='testuser').first()
            db.session.delete(user)
            db.session.commit()
            user = User.query.filter_by(username='testuser').first()
            self.assertIsNone(user)

if __name__ == '__main__':
    unittest.main()
