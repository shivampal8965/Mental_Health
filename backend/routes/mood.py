from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from models import db, MoodEntry, User

mood_bp = Blueprint('moods', __name__)

@mood_bp.route('/log', methods=['POST'])
def log_mood():
    """Log a new mood entry"""
    data = request.get_json()
    user_id = data.get('user_id')
    
    # Validate user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Create mood entry
    mood_entry = MoodEntry(
        user_id=user_id,
        mood=data.get('mood'),
        energy_level=data.get('energy_level'),
        stress_level=data.get('stress_level'),
        sleep_quality=data.get('sleep_quality'),
        notes=data.get('notes'),
        activities=data.get('activities')
    )
    
    db.session.add(mood_entry)
    db.session.commit()
    
    return jsonify({
        'message': 'Mood logged successfully',
        'mood_entry': mood_entry.to_dict()
    }), 201


@mood_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_moods(user_id):
    """Get all mood entries for a user"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get query parameters for filtering
    limit = request.args.get('limit', 30, type=int)
    days = request.args.get('days', 7, type=int)
    
    # Get moods from last N days
    start_date = datetime.utcnow() - timedelta(days=days)
    moods = MoodEntry.query.filter(
        MoodEntry.user_id == user_id,
        MoodEntry.created_at >= start_date
    ).order_by(MoodEntry.created_at.desc()).limit(limit).all()
    
    return jsonify({
        'moods': [mood.to_dict() for mood in moods],
        'count': len(moods)
    }), 200


@mood_bp.route('/<int:mood_id>', methods=['GET'])
def get_mood(mood_id):
    """Get a specific mood entry"""
    mood = MoodEntry.query.get(mood_id)
    
    if not mood:
        return jsonify({'error': 'Mood entry not found'}), 404
    
    return jsonify({'mood_entry': mood.to_dict()}), 200


@mood_bp.route('/<int:mood_id>', methods=['PUT'])
def update_mood(mood_id):
    """Update a mood entry"""
    mood = MoodEntry.query.get(mood_id)
    
    if not mood:
        return jsonify({'error': 'Mood entry not found'}), 404
    
    data = request.get_json()
    
    if 'mood' in data:
        mood.mood = data['mood']
    if 'energy_level' in data:
        mood.energy_level = data['energy_level']
    if 'stress_level' in data:
        mood.stress_level = data['stress_level']
    if 'sleep_quality' in data:
        mood.sleep_quality = data['sleep_quality']
    if 'notes' in data:
        mood.notes = data['notes']
    if 'activities' in data:
        mood.activities = data['activities']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Mood entry updated successfully',
        'mood_entry': mood.to_dict()
    }), 200


@mood_bp.route('/<int:mood_id>', methods=['DELETE'])
def delete_mood(mood_id):
    """Delete a mood entry"""
    mood = MoodEntry.query.get(mood_id)
    
    if not mood:
        return jsonify({'error': 'Mood entry not found'}), 404
    
    db.session.delete(mood)
    db.session.commit()
    
    return jsonify({'message': 'Mood entry deleted successfully'}), 200


@mood_bp.route('/stats/user/<int:user_id>', methods=['GET'])
def get_mood_stats(user_id):
    """Get mood statistics for a user"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    days = request.args.get('days', 30, type=int)
    start_date = datetime.utcnow() - timedelta(days=days)
    
    moods = MoodEntry.query.filter(
        MoodEntry.user_id == user_id,
        MoodEntry.created_at >= start_date
    ).all()
    
    if not moods:
        return jsonify({
            'stats': {
                'average_mood': 0,
                'average_energy': 0,
                'average_stress': 0,
                'total_entries': 0
            }
        }), 200
    
    stats = {
        'average_mood': sum(m.mood for m in moods) / len(moods),
        'average_energy': sum(m.energy_level or 0 for m in moods) / len(moods),
        'average_stress': sum(m.stress_level or 0 for m in moods) / len(moods),
        'total_entries': len(moods),
        'period_days': days
    }
    
    return jsonify({'stats': stats}), 200
