from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, Goal, User

# Create blueprint
goals_bp = Blueprint('goals', __name__)


@goals_bp.route('/create', methods=['POST'])
def create_goal():
    """Create a new goal"""
    try:
        data = request.get_json()
        
        goal = Goal(
            user_id=data.get('user_id'),
            name=data.get('name'),
            description=data.get('description'),
            category=data.get('category', 'general'),
            target_date=datetime.fromisoformat(data.get('target_date')) if data.get('target_date') else None,
            status=data.get('status', 'active')
        )
        
        db.session.add(goal)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Goal created successfully',
            'goal': goal.to_dict()
        }), 201
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error creating goal: {str(e)}'
        }), 500


@goals_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_goals(user_id):
    """Get all goals for a specific user"""
    try:
        # Get optional filter
        status = request.args.get('status')
        category = request.args.get('category')
        
        query = Goal.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        if category:
            query = query.filter_by(category=category)
        
        goals = query.order_by(Goal.created_at.desc()).all()
        
        return jsonify({
            'status': 'success',
            'count': len(goals),
            'goals': [g.to_dict() for g in goals]
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error fetching goals: {str(e)}'
        }), 500


@goals_bp.route('/<int:goal_id>', methods=['GET'])
def get_goal(goal_id):
    """Get a specific goal"""
    try:
        goal = Goal.query.get(goal_id)
        
        if not goal:
            return jsonify({
                'status': 'error',
                'message': 'Goal not found'
            }), 404
        
        return jsonify({
            'status': 'success',
            'goal': goal.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error fetching goal: {str(e)}'
        }), 500


@goals_bp.route('/<int:goal_id>', methods=['PUT'])
def update_goal(goal_id):
    """Update a goal"""
    try:
        goal = Goal.query.get(goal_id)
        
        if not goal:
            return jsonify({
                'status': 'error',
                'message': 'Goal not found'
            }), 404
        
        data = request.get_json()
        
        # Update fields
        if 'name' in data:
            goal.name = data['name']
        if 'description' in data:
            goal.description = data['description']
        if 'category' in data:
            goal.category = data['category']
        if 'progress' in data:
            goal.progress = min(100, max(0, data['progress']))  # Ensure 0-100
        if 'status' in data:
            goal.status = data['status']
        if 'target_date' in data and data['target_date']:
            goal.target_date = datetime.fromisoformat(data['target_date'])
        
        # Mark as completed if progress is 100
        if goal.progress == 100 and goal.status == 'active':
            goal.status = 'completed'
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Goal updated successfully',
            'goal': goal.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error updating goal: {str(e)}'
        }), 500


@goals_bp.route('/<int:goal_id>/progress', methods=['PUT'])
def update_goal_progress(goal_id):
    """Update only the progress of a goal"""
    try:
        goal = Goal.query.get(goal_id)
        
        if not goal:
            return jsonify({
                'status': 'error',
                'message': 'Goal not found'
            }), 404
        
        data = request.get_json()
        progress = min(100, max(0, data.get('progress', 0)))  # Ensure 0-100
        
        goal.progress = progress
        
        # Auto-complete when progress reaches 100
        if progress == 100 and goal.status == 'active':
            goal.status = 'completed'
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Goal progress updated',
            'goal': goal.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error updating goal progress: {str(e)}'
        }), 500


@goals_bp.route('/<int:goal_id>', methods=['DELETE'])
def delete_goal(goal_id):
    """Delete a goal"""
    try:
        goal = Goal.query.get(goal_id)
        
        if not goal:
            return jsonify({
                'status': 'error',
                'message': 'Goal not found'
            }), 404
        
        db.session.delete(goal)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Goal deleted successfully'
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error deleting goal: {str(e)}'
        }), 500


@goals_bp.route('/user/<int:user_id>/stats', methods=['GET'])
def get_user_goal_stats(user_id):
    """Get goal statistics for a user"""
    try:
        from sqlalchemy import func
        
        all_goals = Goal.query.filter_by(user_id=user_id).all()
        
        total = len(all_goals)
        completed = len([g for g in all_goals if g.status == 'completed'])
        active = len([g for g in all_goals if g.status == 'active'])
        abandoned = len([g for g in all_goals if g.status == 'abandoned'])
        
        # Calculate completion rate
        completion_rate = (completed / total * 100) if total > 0 else 0
        
        # Get average progress
        avg_progress = db.session.query(func.avg(Goal.progress)).filter_by(user_id=user_id).scalar() or 0
        
        # Goals by category
        categories = db.session.query(Goal.category, func.count(Goal.id)).filter_by(user_id=user_id).group_by(Goal.category).all()
        category_counts = {cat: count for cat, count in categories}
        
        return jsonify({
            'status': 'success',
            'stats': {
                'total_goals': total,
                'completed_goals': completed,
                'active_goals': active,
                'abandoned_goals': abandoned,
                'completion_rate': round(completion_rate, 2),
                'average_progress': round(float(avg_progress), 2),
                'by_category': category_counts
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error fetching goal stats: {str(e)}'
        }), 500
