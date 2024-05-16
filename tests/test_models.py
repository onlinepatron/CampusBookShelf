import unittest
from app import create_app, db
from models import User

class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_user_model(self):
        user = User(username='testuser', email='testuser@example.com')
        user.set_password('correctpassword')
        db.session.add(user)
        db.session.commit()
        queried_user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(queried_user)
        self.assertTrue(queried_user.check_password('correctpassword'))

if __name__ == '__main__':
    unittest.main()
