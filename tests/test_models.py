import unittest
from app import create_app, db
from models import User, Review

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
        user = User(username='testuser')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        self.assertIsNotNone(user.id)
        self.assertTrue(user.check_password('password123'))

    def test_review_model(self):
        review = Review(user_id=1, book_id=1, text='Great book!', rating=5)
        db.session.add(review)
        db.session.commit()
        self.assertIsNotNone(review.id)

if __name__ == '__main__':
    unittest.main()
