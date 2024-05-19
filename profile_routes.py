from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Review, BookRequest, Comment

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/my-profile')
@login_required
def my_profile():
    reviews = Review.query.filter_by(user_id=current_user.id).all()
    book_requests = BookRequest.query.filter(BookRequest.comments.any(user_id=current_user.id)).all()
    comments = Comment.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', reviews=reviews, book_requests=book_requests, comments=comments)