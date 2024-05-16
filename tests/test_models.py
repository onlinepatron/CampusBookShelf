import unittest
from app import create_app, db
from models import User

class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_model(self):
        with self.app.app_context():
            user = User(username='testuser', email='testuser@example.com', password_hash='testpassword')
            db.session.add(user)
            db.session.commit()
            queried_user = User.query.filter_by(username='testuser').first()
            self.assertEqual(queried_user.username, 'testuser')

if __name__ == '__main__':
    unittest.main()
