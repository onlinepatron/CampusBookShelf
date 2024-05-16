import unittest
from app import create_app, db
from models import User

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            # Create a test user
            test_user = User(username='testuser', email='testuser@example.com')
            test_user.set_password('correctpassword')
            db.session.add(test_user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_login_success(self):
        response = self.client.post('/login', data=dict(username='testuser', password='correctpassword'))
        self.assertEqual(response.status_code, 302)  # Redirect to the main page
        self.assertIn('/main', response.location)

    def test_login_failure(self):
        response = self.client.post('/login', data=dict(username='testuser', password='wrongpassword'))
        self.assertEqual(response.status_code, 200)  # Stay on the login page
        self.assertIn(b'Invalid username or password', response.data)

    def test_signup(self):
        response = self.client.post('/sign-up', data=dict(
            username='newuser',
            email='newuser@example.com',
            password='newpassword',
            confirmPassword='newpassword'
        ))
        self.assertEqual(response.status_code, 302)  # Redirect to the main page
        self.assertIn('/main', response.location)

    def test_logout(self):
        self.client.post('/login', data=dict(username='testuser', password='correctpassword'))
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)  # Redirect to the login page
        self.assertIn('/login', response.location)

if __name__ == '__main__':
    unittest.main()
