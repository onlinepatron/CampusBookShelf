import unittest
from auth import login, signup, logout

class TestAuth(unittest.TestCase):
    
    def test_login_success(self):
        result = login('testuser', 'correctpassword')
        self.assertTrue(result)
    
    def test_login_failure(self):
        result = login('testuser', 'wrongpassword')
        self.assertFalse(result)
    
    def test_signup(self):
        result = signup('newuser', 'newpassword')
        self.assertTrue(result)
    
    def test_logout(self):
        result = logout('testuser')
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
