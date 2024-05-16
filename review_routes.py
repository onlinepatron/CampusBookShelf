from flask import Blueprint, jsonify, request
from app import db
from models import Review

review_bp = Blueprint('review', __name__)

@review_bp.route('/book/<int:book_id>/review', methods=['POST'])
def add_review(book_id):
    data = request.get_json()
    new_review = Review(user_id=data['user_id'], book_id=book_id, text=data['text'], rating=data['rating'])
    db.session.add(new_review)
    db.session.commit()
    return jsonify({'message': 'Review added successfully'}), 201

@review_bp.route('/book/<int:book_id>/reviews', methods=['GET'])
def get_reviews(book_id):
    reviews = Review.query.filter_by(book_id=book_id).all()
    reviews_list = [{'id': review.id, 'user_id': review.user_id, 'book_id': review.book_id, 'text': review.text, 'rating': review.rating} for review in reviews]
    return jsonify(reviews_list)

@review_bp.route('/review/<int:review_id>', methods=['GET'])
def get_review_by_id(review_id):
    review = Review.query.get_or_404(review_id)
    return jsonify({'id': review.id, 'user_id': review.user_id, 'book_id': review.book_id, 'text': review.text, 'rating': review.rating})

@review_bp.route('/review/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = Review.query.get(review_id)
    if review is None:
        return jsonify({'error': 'Review not found'}), 404
    db.session.delete(review)
    db.session.commit()
    return jsonify({'message': 'Review deleted successfully'})
