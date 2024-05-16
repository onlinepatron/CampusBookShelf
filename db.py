from app import db
from models import User

def get_user(username):
    return User.query.filter_by(username=username).first()

def add_user(username, password):
    if get_user(username):
        return False
    new_user = User(username=username)
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
