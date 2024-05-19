from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from app import db
from models import Book, BookRequest, Review, Comment
from flask_login import login_required, current_user

book_bp = Blueprint('book', __name__)

@book_bp.route('/books')
def get_books():
    sort_by = request.args.get('sort_by', 'title')
    genre = request.args.get('genre', '')

    if sort_by == 'rating':
        books = sorted(Book.query.all(), key=lambda book: book.average_rating, reverse=True)
    else:
        books = Book.query.order_by(Book.title).all()

    if genre:
        books = [book for book in books if genre.lower() in book.genre.lower()]

    return render_template('books.html', books=books)

@book_bp.route('/book/<int:book_id>')
def get_book(book_id):
    book = db.session.get(Book, book_id)
    return render_template('book.html', book=book)

@book_bp.route('/update_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
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
@login_required
def delete_book(book_id):
    book = db.session.get(Book, book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully', 'success')
    return redirect(url_for('book.get_books'))

@book_bp.route('/createRequest', methods=['GET', 'POST'])
@login_required
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

        new_request = BookRequest(title=title, author=author, genre=genre, message=message, book_type=book_type)
        db.session.add(new_request)
        db.session.commit()

        flash('Your book request has been successfully submitted!', 'success')
        return redirect(url_for('main'))  # Redirect to the main page

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

@book_bp.route('/findRequests')
@login_required
def find_requests_page():
    books = BookRequest.query.all()
    return render_template('findRequests.html', books=books)

@book_bp.route('/api/findRequests', methods=['GET'])
@login_required
def api_find_requests():
    genre = request.args.get('genre')
    title = request.args.get('title')
    query = BookRequest.query

    if genre:
        query = query.filter(BookRequest.genre.ilike(f"%{genre}%"))
    if title:
        query = query.filter(BookRequest.title.ilike(f"%{title}%"))

    requests = query.all()
    result = [request.serialize() for request in requests]
    return jsonify(result)

@book_bp.route('/book_request/<int:request_id>/comment', methods=['POST'])
@login_required
def add_book_request_comment(request_id):
    text = request.form.get('text')
    if not text:
        return jsonify({'error': 'Comment text is required'}), 400
    comment = Comment(user_id=current_user.id, book_id=request_id, text=text)
    db.session.add(comment)
    db.session.commit()
    comment_data = {
        'user': current_user.username,
        'text': comment.text
    }
    return jsonify({'message': 'Comment added successfully', 'comment': comment_data}), 201

