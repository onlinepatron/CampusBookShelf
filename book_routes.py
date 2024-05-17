from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from models import Book, Review
from flask_login import login_required, current_user

book_bp = Blueprint('book', __name__)

@book_bp.route('/books')
def get_books():
    books = Book.query.all()
    return render_template('books.html', books=books)

@book_bp.route('/book/<int:book_id>')
def get_book(book_id):
    book = db.session.get(Book, book_id)
    return render_template('book.html', book=book)

@book_bp.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        genre = request.form.get('genre')
        synopsis = request.form.get('synopsis', '')
        image_url = request.form.get('image_url', '')
        new_book = Book(title=title, author=author, genre=genre, synopsis=synopsis, image_url=image_url)
        db.session.add(new_book)
        db.session.commit()
        flash('Book added successfully', 'success')
        return redirect(url_for('book.get_books'))
    return render_template('add_book.html')

@book_bp.route('/update_book/<int:book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    book = db.session.get(Book, book_id)
    if request.method == 'POST':
        book.title = request.form.get('title')
        book.author = request.form.get('author')
        book.genre = request.form.get('genre')
        book.synopsis = request.form.get('synopsis', '')
        book.image_url = request.form.get('image_url', '')
        db.session.commit()
        flash('Book updated successfully', 'success')
        return redirect(url_for('book.get_book', book_id=book.id))
    return render_template('update_book.html', book=book)

@book_bp.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = db.session.get(Book, book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully', 'success')
    return redirect(url_for('book.get_books'))

@book_bp.route('/createRequest', methods=['GET', 'POST'])
def create_request():
    title = request.args.get('title')
    author = request.args.get('author')
    genre = request.args.get('genre')
    if title and author and genre:
        return render_template('createRequest.html', title=title, author=author, genre=genre)
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        genre = request.form.get('genre')
        message = request.form.get('message', '')
        book_type = request.form.get('type', 'PDF')

        new_book = Book(title=title, author=author, genre=genre, synopsis=message)
        db.session.add(new_book)
        db.session.commit()

        flash('Your book request has been successfully submitted!', 'success')
        return redirect(url_for('index'))  # Redirect to the home page

    return render_template('createRequest.html')    
@book_bp.route('/rate-books', methods=['GET', 'POST'])
@login_required
def rate_books():
    if request.method == 'POST':
        book_id = request.form.get('book_id')
        rating = request.form.get('rating')
        review_text = request.form.get('review')
        book = Book.query.get(book_id)
        if not book:
            flash('Book not found', 'danger')
            return redirect(url_for('book.rate_books'))
        review = Review(user_id=current_user.id, book_id=book.id, rating=rating, text=review_text)
        db.session.add(review)
        db.session.commit()
        flash('Your review has been submitted', 'success')
        return redirect(url_for('book.get_books'))
    books = Book.query.all()
    return render_template('rateBooks.html', books=books)
