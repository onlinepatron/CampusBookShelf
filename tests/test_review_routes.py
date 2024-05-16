import unittest
from app import create_app, db
from models import Review, User, Book

class TestReviewRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            # Create test data
            user = User(username='testuser')
            user.set_password('testpassword')
            db.session.add(user)
            book = Book(title='Test Book', author='Test Author', genre='Test Genre', synopsis='Test Synopsis')
            db.session.add(book)
            db.session.commit()
            self.user_id = user.id
            self.book_id = book.id

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_get_reviews(self):
        response = self.client.get(f'/book/{self.book_id}/reviews')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_add_review(self):
        response = self.client.post(f'/book/{self.book_id}/review', json=dict(
            user_id=self.user_id, text='Great book!', rating=5
        ))
        self.assertEqual(response.status_code, 201)
        self.assertIn('Review added successfully', response.json['message'])

    def test_get_review_by_id(self):
        with self.app.app_context():
            review = Review(user_id=self.user_id, book_id=self.book_id, text='Great book!', rating=5)
            db.session.add(review)
            db.session.commit()
            review_id = review.id

        response = self.client.get(f'/review/{review_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], review_id)

    def test_delete_review(self):
        with self.app.app_context():
            review = Review(user_id=self.user_id, book_id=self.book_id, text='Great book!', rating=5)
            db.session.add(review)
            db.session.commit()
            review_id = review.id

        response = self.client.delete(f'/review/{review_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Review deleted successfully', response.json['message'])

if __name__ == '__main__':
    unittest.main()
