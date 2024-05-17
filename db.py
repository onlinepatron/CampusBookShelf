from app import db
from models import User, Book

def get_user(username):
    return User.query.filter_by(username=username).first()

def add_user(username, email, password):
    if get_user(username):
        return False
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return True

def remove_user(username):
    user = get_user(username)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False

def get_db():
    return db

def close_db(e=None):
    db.session.remove()

def add_book(title, author, genre, synopsis, image_url):
    new_book = Book(title=title, author=author, genre=genre, synopsis=synopsis, image_url=image_url)
    db.session.add(new_book)
    db.session.commit()