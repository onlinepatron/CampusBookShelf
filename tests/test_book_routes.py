import unittest
from app import create_app, db
from models import Book

class TestBookRoutes(unittest.TestCase):
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

    def test_get_books(self):
        with self.app.app_context():
            book1 = Book(title='Book1', author='Author1', genre='Genre1', synopsis='Synopsis1')
            book2 = Book(title='Book2', author='Author2', genre='Genre2', synopsis='Synopsis2')
            db.session.add(book1)
            db.session.add(book2)
            db.session.commit()

        response = self.client.get('/books')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Book1', response.data)
        self.assertIn(b'Book2', response.data)

    def test_add_book(self):
        response = self.client.post('/add_book', data=dict(
            title='New Book', author='New Author', genre='New Genre', synopsis='New Synopsis', image_url=''
        ))
        self.assertEqual(response.status_code, 302)  # Redirect to books list

        with self.app.app_context():
            book = Book.query.filter_by(title='New Book').first()
            self.assertIsNotNone(book)
            self.assertEqual(book.author, 'New Author')

    def test_get_book(self):
        with self.app.app_context():
            book = Book(title='Book1', author='Author1', genre='Genre1', synopsis='Synopsis1')
            db.session.add(book)
            db.session.commit()
            book_id = book.id

        response = self.client.get(f'/book/{book_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Book1', response.data)

    def test_update_book(self):
        with self.app.app_context():
            book = Book(title='Book1', author='Author1', genre='Genre1', synopsis='Synopsis1')
            db.session.add(book)
            db.session.commit()
            book_id = book.id

        response = self.client.post(f'/update_book/{book_id}', data=dict(
            title='Updated Book', author='Updated Author', genre='Updated Genre', synopsis='Updated Synopsis', image_url=''
        ))
        self.assertEqual(response.status_code, 302)  # Redirect to the updated book

        with self.app.app_context():
            updated_book = Book.query.get(book_id)
            self.assertEqual(updated_book.title, 'Updated Book')
            self.assertEqual(updated_book.author, 'Updated Author')

    def test_delete_book(self):
        with self.app.app_context():
            book = Book(title='Book1', author='Author1', genre='Genre1', synopsis='Synopsis1')
            db.session.add(book)
            db.session.commit()
            book_id = book.id

        response = self.client.post(f'/delete_book/{book_id}')
        self.assertEqual(response.status_code, 302)  # Redirect to books list

        with self.app.app_context():
            deleted_book = Book.query.get(book_id)
            self.assertIsNone(deleted_book)

if __name__ == '__main__':
    unittest.main()
