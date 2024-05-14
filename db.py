from app import db

def get_db():
    return db

def close_db(e=None):
    db.session.remove()
