import unittest
from db import get_user, add_user, remove_user

class TestDB(unittest.TestCase):
    
    def test_get_user(self):
        user = get_user('testuser')
        self.assertIsNotNone(user)
    
    def test_add_user(self):
        result = add_user('newuser', 'newpassword')
        self.assertTrue(result)
    
    def test_remove_user(self):
        result = remove_user('testuser')
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
