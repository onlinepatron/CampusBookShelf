from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from models import Book
from extensions import db
from werkzeug.utils import secure_filename
import os

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/upload-book', methods=['GET', 'POST'])
@login_required
def upload_book():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main'))

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        genre = request.form.get('genre')
        synopsis = request.form.get('synopsis', '')
        image = request.files.get('image')

        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.root_path, 'static', 'images', filename))
            image_url = f"/static/images/{filename}"
        else:
            image_url = None

        new_book = Book(title=title, author=author, genre=genre, synopsis=synopsis, image_url=image_url)
        db.session.add(new_book)
        db.session.commit()
        flash('Book uploaded successfully', 'success')
        return redirect(url_for('book.get_books'))

    return render_template('admin/upload_book.html')

@admin_bp.route('/admin/edit-book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main'))

    book = Book.query.get_or_404(book_id)

    if request.method == 'POST':
        book.title = request.form.get('title')
        book.author = request.form.get('author')
        book.genre = request.form.get('genre')
        book.synopsis = request.form.get('synopsis', '')
        image = request.files.get('image')

        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.root_path, 'static', 'images', filename))
            book.image_url = f"/static/images/{filename}"

        db.session.commit()
        flash('Book updated successfully', 'success')
        return redirect(url_for('book.get_book', book_id=book.id))

    return render_template('admin/edit_book.html', book=book)

@admin_bp.route('/admin/delete-book/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('main'))

    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully', 'success')
    return redirect(url_for('book.get_books'))