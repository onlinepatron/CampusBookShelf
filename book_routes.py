from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from models import Book

book_bp = Blueprint('book', __name__)

@book_bp.route('/books')
def get_books():
    books = Book.query.all()
    return render_template('books.html', books=books)

@book_bp.route('/book/<int:book_id>')
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book.html', book=book)

@book_bp.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        synopsis = request.form['synopsis']
        image_url = request.form['image_url']
        new_book = Book(title=title, author=author, genre=genre, synopsis=synopsis, image_url=image_url)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('book.get_books'))
    return render_template('add_book.html')

@book_bp.route('/update_book/<int:book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.genre = request.form['genre']
        book.synopsis = request.form['synopsis']
        book.image_url = request.form['image_url']
        db.session.commit()
        return redirect(url_for('book.get_book', book_id=book.id))
    return render_template('update_book.html', book=book)

@book_bp.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('book.get_books'))
