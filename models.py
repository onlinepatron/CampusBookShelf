from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db, login_manager
from datetime import datetime
from sqlalchemy import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    synopsis = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(200), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "synopsis": self.synopsis,
            "image_url": self.image_url
        }

    @property
    def average_rating(self):
        if self.reviews:
            return round(sum(review.rating for review in self.reviews) / len(self.reviews), 2)
        return 0

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', back_populates='reviews')
    book = db.relationship('Book', back_populates='reviews')

    def rating_description(self):
        descriptions = {1: 'Poor', 2: 'Fair', 3: 'Good', 4: 'Very Good', 5: 'Excellent'}
        return descriptions.get(self.rating, 'Unknown')

User.reviews = db.relationship('Review', back_populates='user', cascade='all, delete-orphan')
Book.reviews = db.relationship('Review', back_populates='book', cascade='all, delete-orphan')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', back_populates='comments')
    book = db.relationship('Book', back_populates='comments')

User.comments = db.relationship('Comment', back_populates='user', cascade='all, delete-orphan')
Book.comments = db.relationship('Comment', back_populates='book', cascade='all, delete-orphan')

class BookRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=True)
    book_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "message": self.message,
            "book_type": self.book_type,
            "created_at": self.created_at
        }