import unittest
from app import create_app, db
from models import User

class TestReviewRoutes(unittest.TestCase):
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

    def test_add_review(self):
        with self.app.app_context():
            # Add review test code here
            pass

    def test_delete_review(self):
        with self.app.app_context():
            # Delete review test code here
            pass

    def test_get_review_by_id(self):
        with self.app.app_context():
            # Get review by id test code here
            pass

    def test_get_reviews(self):
        with self.app.app_context():
            # Get reviews test code here
            pass

if __name__ == '__main__':
    unittest.main()
