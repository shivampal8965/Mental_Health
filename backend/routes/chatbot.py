from flask import Blueprint, request, jsonify
from models import db, ChatMessage, User
from ai_engine.chatbot_model import chatbot

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    """Send a message to the chatbot"""
    data = request.get_json()
    user_id = data.get('user_id')
    user_message = data.get('message')
    
    if not user_id or not user_message:
        return jsonify({'error': 'Missing user_id or message'}), 400
    
    # Validate user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get bot response using AI Engine
    bot_response, analysis = chatbot.generate_response(user_message)
    
    # Save chat message
    chat_msg = ChatMessage(
        user_id=user_id,
        user_message=user_message,
        bot_response=bot_response
    )
    
    db.session.add(chat_msg)
    db.session.commit()
    
    return jsonify({
        'user_message': user_message,
        'bot_response': bot_response,
        'chat_id': chat_msg.id,
        'analysis': analysis
    }), 200


@chatbot_bp.route('/history/<int:user_id>', methods=['GET'])
def chat_history(user_id):
    """Get chat history for a user"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    limit = request.args.get('limit', 50, type=int)
    
    messages = ChatMessage.query.filter_by(user_id=user_id)\
        .order_by(ChatMessage.created_at.desc()).limit(limit).all()
    
    return jsonify({
        'messages': [msg.to_dict() for msg in reversed(messages)],
        'count': len(messages)
    }), 200


@chatbot_bp.route('/suggestions', methods=['GET'])
def get_suggestions():
    """Get chatbot suggestions for user"""
    suggestions = [
        {
            'emoji': '😰',
            'text': 'I feel anxious',
            'color': 'danger'
        },
        {
            'emoji': '😟',
            'text': 'I am stressed',
            'color': 'warning'
        },
        {
            'emoji': '😢',
            'text': 'I feel sad',
            'color': 'info'
        },
        {
            'emoji': '💪',
            'text': 'I need motivation',
            'color': 'success'
        },
        {
            'emoji': '😴',
            'text': 'Sleep tips',
            'color': 'primary'
        },
        {
            'emoji': '🏃',
            'text': 'Exercise advice',
            'color': 'success'
        }
    ]
    
    return jsonify({'suggestions': suggestions}), 200


@chatbot_bp.route('/wellness-tips', methods=['GET'])
def wellness_tips():
    """Get wellness tips"""
    tips = [
        {
            'emoji': '🧘',
            'title': 'Mindfulness Practice',
            'description': 'Spend 5 minutes daily in mindfulness meditation to reduce stress and improve focus.',
            'color': 'primary'
        },
        {
            'emoji': '🏃',
            'title': 'Stay Active',
            'description': 'Regular exercise boosts mood and energy levels. Aim for at least 30 minutes daily.',
            'color': 'success'
        },
        {
            'emoji': '💤',
            'title': 'Good Sleep Hygiene',
            'description': 'Maintain a consistent sleep schedule and avoid screens 1 hour before bedtime.',
            'color': 'info'
        },
        {
            'emoji': '🤝',
            'title': 'Connect Socially',
            'description': 'Maintain strong relationships and social connections for better mental health.',
            'color': 'warning'
        },
        {
            'emoji': '🥗',
            'title': 'Healthy Nutrition',
            'description': 'Balanced diet supports mental wellbeing. Include fruits, vegetables, and whole grains.',
            'color': 'success'
        },
        {
            'emoji': '📔',
            'title': 'Journal Your Thoughts',
            'description': 'Writing down thoughts helps process emotions and increase self-awareness.',
            'color': 'primary'
        }
    ]
    
    return jsonify({'tips': tips}), 200
