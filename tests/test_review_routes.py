import unittest
from review_routes import get_reviews, add_review, get_review_by_id

class TestReviewRoutes(unittest.TestCase):
    
    def test_get_reviews(self):
        reviews = get_reviews()
        self.assertIsInstance(reviews, list)
    
    def test_add_review(self):
        result = add_review(1, 1, 5, 'Great book!')
        self.assertTrue(result)
    
    def test_get_review_by_id(self):
        review = get_review_by_id(1)
        self.assertIsNotNone(review)
        self.assertEqual(review.id, 1)

if __name__ == '__main__':
    unittest.main()
