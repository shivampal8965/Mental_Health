from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, Rating, User

# Create blueprint
ratings_bp = Blueprint('ratings', __name__)


@ratings_bp.route('/submit', methods=['POST'])
def submit_rating():
    """Submit a new rating/feedback"""
    try:
        data = request.get_json()
        
        rating = Rating(
            user_id=data.get('user_id'),
            overall=data.get('overall', 0),
            mood_tracking=data.get('mood_tracking'),
            chatbot=data.get('chatbot'),
            ui=data.get('ui'),
            analytics=data.get('analytics'),
            recommend=data.get('recommend'),
            comments=data.get('comments'),
            email=data.get('email')
        )
        
        db.session.add(rating)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Rating submitted successfully',
            'rating': rating.to_dict()
        }), 201
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error submitting rating: {str(e)}'
        }), 500


@ratings_bp.route('/all', methods=['GET'])
def get_all_ratings():
    """Get all ratings with optional filtering"""
    try:
        # Get query parameters for filtering
        limit = request.args.get('limit', default=50, type=int)
        sort_by = request.args.get('sort_by', default='created_at')
        
        ratings = Rating.query.order_by(
            getattr(Rating, sort_by).desc()
        ).limit(limit).all()
        
        return jsonify({
            'status': 'success',
            'count': len(ratings),
            'ratings': [r.to_dict() for r in ratings]
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error fetching ratings: {str(e)}'
        }), 500


@ratings_bp.route('/stats', methods=['GET'])
def get_rating_stats():
    """Get rating statistics"""
    try:
        from sqlalchemy import func
        
        total_ratings = Rating.query.count()
        
        if total_ratings == 0:
            return jsonify({
                'status': 'success',
                'total_ratings': 0,
                'average_rating': 0,
                'recommendation_rate': 0
            }), 200
        
        avg_overall = db.session.query(func.avg(Rating.overall)).scalar() or 0
        avg_mood = db.session.query(func.avg(Rating.mood_tracking)).scalar() or 0
        avg_chatbot = db.session.query(func.avg(Rating.chatbot)).scalar() or 0
        avg_ui = db.session.query(func.avg(Rating.ui)).scalar() or 0
        avg_analytics = db.session.query(func.avg(Rating.analytics)).scalar() or 0
        
        recommend_yes = Rating.query.filter_by(recommend='yes').count()
        recommend_rate = (recommend_yes / total_ratings) * 100 if total_ratings > 0 else 0
        
        return jsonify({
            'status': 'success',
            'total_ratings': total_ratings,
            'average_overall': round(float(avg_overall), 2),
            'average_mood_tracking': round(float(avg_mood), 2),
            'average_chatbot': round(float(avg_chatbot), 2),
            'average_ui': round(float(avg_ui), 2),
            'average_analytics': round(float(avg_analytics), 2),
            'recommendation_rate': round(recommend_rate, 2),
            'recommend_counts': {
                'yes': recommend_yes,
                'maybe': Rating.query.filter_by(recommend='maybe').count(),
                'no': Rating.query.filter_by(recommend='no').count()
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error fetching rating stats: {str(e)}'
        }), 500


@ratings_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_ratings(user_id):
    """Get all ratings submitted by a specific user"""
    try:
        ratings = Rating.query.filter_by(user_id=user_id).all()
        
        return jsonify({
            'status': 'success',
            'count': len(ratings),
            'ratings': [r.to_dict() for r in ratings]
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error fetching user ratings: {str(e)}'
        }), 500


@ratings_bp.route('/<int:rating_id>', methods=['GET'])
def get_rating(rating_id):
    """Get a specific rating"""
    try:
        rating = Rating.query.get(rating_id)
        
        if not rating:
            return jsonify({
                'status': 'error',
                'message': 'Rating not found'
            }), 404
        
        return jsonify({
            'status': 'success',
            'rating': rating.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error fetching rating: {str(e)}'
        }), 500


@ratings_bp.route('/<int:rating_id>', methods=['DELETE'])
def delete_rating(rating_id):
    """Delete a rating"""
    try:
        rating = Rating.query.get(rating_id)
        
        if not rating:
            return jsonify({
                'status': 'error',
                'message': 'Rating not found'
            }), 404
        
        db.session.delete(rating)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Rating deleted successfully'
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error deleting rating: {str(e)}'
        }), 500
