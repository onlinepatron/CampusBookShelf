import unittest
from book_routes import get_books, add_book, get_book_by_id

class TestBookRoutes(unittest.TestCase):
    
    def test_get_books(self):
        books = get_books()
        self.assertIsInstance(books, list)
    
    def test_add_book(self):
        result = add_book('New Book', 'New Author')
        self.assertTrue(result)
    
    def test_get_book_by_id(self):
        book = get_book_by_id(1)
        self.assertIsNotNone(book)
        self.assertEqual(book.id, 1)

if __name__ == '__main__':
    unittest.main()
