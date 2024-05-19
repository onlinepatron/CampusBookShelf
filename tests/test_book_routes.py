import unittest
from app import create_app, db
from models import User, Book, Review
import time

class TestBookRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a test admin user
        admin_user = User(username='adminuser', email='adminuser@example.com', password_hash='adminpassword', is_admin=True)
        admin_user.set_password('adminpassword')
        db.session.add(admin_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_books(self):
        with self.app.test_client() as client:
            book1 = Book(title='Test Book 1', author='Test Author 1', genre='Test Genre 1')
            book2 = Book(title='Test Book 2', author='Test Author 2', genre='Test Genre 2')
            db.session.add(book1)
            db.session.add(book2)
            db.session.commit()

            response = client.get('/books')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Book 1', response.data)
            self.assertIn(b'Test Book 2', response.data)

    def test_get_book(self):
        with self.app.test_client() as client:
            book = Book(title='Test Book', author='Test Author', genre='Test Genre')
            db.session.add(book)
            db.session.commit()

            response = client.get(f'/book/{book.id}')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Book', response.data)

    def test_update_book(self):
        with self.app.test_client() as client:
            # Log in as the admin user
            response = client.post('/login', data=dict(
                username='adminuser',
                password='adminpassword'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            book = Book(title='Test Book', author='Test Author', genre='Test Genre')
            db.session.add(book)
            db.session.commit()

            response = client.post(f'/update_book/{book.id}', data=dict(
                title='Updated Book',
                author='Updated Author',
                genre='Updated Genre',
                synopsis='Updated Synopsis'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Book updated successfully', response.data)

    def test_delete_book(self):
        with self.app.test_client() as client:
            # Log in as the admin user
            response = client.post('/login', data=dict(
                username='adminuser',
                password='adminpassword'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            book = Book(title='Test Book', author='Test Author', genre='Test Genre')
            db.session.add(book)
            db.session.commit()

            response = client.post(f'/delete_book/{book.id}', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Book deleted successfully', response.data)

    def test_rate_books(self):
        with self.app.test_client() as client:
            # Create a test user with a unique username and email
            timestamp = int(time.time())
            test_username = f"testuser{timestamp}"
            test_email = f"testuser{timestamp}@example.com"
            test_user = User(username=test_username, email=test_email)
            test_user.set_password('testpassword')
            db.session.add(test_user)
            db.session.commit()

            # Log in the user
            response = client.post('/login', data=dict(
                username=test_username,
                password='testpassword'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            book = Book(title='Test Book', author='Test Author', genre='Test Genre')
            db.session.add(book)
            db.session.commit()

            response = client.post('/rate-books', data=dict(
                book_id=book.id,
                rating=4,
                review='Test Review'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Your review has been submitted', response.data)

if __name__ == '__main__':
    unittest.main()