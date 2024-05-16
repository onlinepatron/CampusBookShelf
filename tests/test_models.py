import unittest
from models import User, Book, Review

class TestModels(unittest.TestCase):
    
    def test_user_model(self):
        user = User(username='testuser', password='password123')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.password, 'password123')
    
    def test_book_model(self):
        book = Book(title='Test Book', author='Test Author')
        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.author, 'Test Author')
    
    def test_review_model(self):
        review = Review(user_id=1, book_id=1, rating=5, comment='Great book!')
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'Great book!')

if __name__ == '__main__':
    unittest.main()
