from flask import Blueprint, request, jsonify
import json

chatbot_bp = Blueprint('chatbot', __name__)

# Chatbot knowledge base
CHATBOT_RESPONSES = {
    'anxious': "I understand you're feeling anxious. That's completely valid. Try these techniques:\n\n✓ Deep breathing: 4 counts in, hold for 4, exhale for 4\n✓ Ground yourself: 5-4-3-2-1 sensory technique\n✓ Progressive muscle relaxation\n\nRemember, anxiety is temporary. You're stronger than you think. Would you like to learn more?",
    
    'stressed': "Stress is a common experience. Here are some immediate relief techniques:\n\n✓ Take a 10-minute break\n✓ Practice deep breathing exercises\n✓ Go for a short walk\n✓ Listen to calming music\n✓ Practice gratitude\n\nWhat's causing your stress today?",
    
    'sad': "I'm sorry you're feeling sad. It's important to acknowledge these feelings. Here's what might help:\n\n✓ Talk to someone you trust\n✓ Do activities you enjoy\n✓ Get sunlight and fresh air\n✓ Practice self-compassion\n✓ Consider reaching out to a professional\n\nYou're not alone. I'm here for you. 💙",
    
    'motivation': "Here's some inspiration for you:\n\n💪 Remember why you started\n🎯 Break goals into smaller steps\n✨ Celebrate small wins\n🌱 Progress over perfection\n💙 Be kind to yourself\n\nYou have the strength within you!",
    
    'sleep': "Better sleep tips:\n\n🌙 Same sleep schedule daily\n📱 No screens 1 hour before bed\n🌡️ Cool bedroom (60-67°F)\n📖 Try relaxing activities\n☕ No caffeine after 2 PM\n\nSleep well! 😴",
    
    'exercise': "Exercise benefits your mental health:\n\n🏃 30 minutes daily\n🧘 Mix cardio with strength training\n🚴 Choose activities you enjoy\n👥 Exercise with friends\n⏰ Morning exercise boosts mood\n\nLet's get moving! 💪",
    
    'depression': "I'm concerned about what you're experiencing. Depression is serious, and you deserve support:\n\n✓ Reach out to a mental health professional\n✓ Talk to someone you trust\n✓ National Suicide Prevention Lifeline: 988\n✓ Crisis Text Line: Text HOME to 741741\n\nYour life has value. Help is available. 💙",
    
    'suicide': "If you're having thoughts of suicide:\n\n🚨 IMMEDIATE HELP:\n• National Suicide Prevention Lifeline: 988 (US)\n• Crisis Text Line: Text HOME to 741741\n• Go to nearest emergency room\n• Call 911\n\nYou matter. Your life is valuable. Please reach out now. 💙",
    
    'help': "I'm here to support your mental health journey. I can help with:\n\n💭 Talk about your feelings\n😰 Anxiety and stress management\n😢 Sadness and depression\n💪 Motivation and goals\n💤 Sleep tips\n🏃 Exercise advice\n🧘 Mindfulness techniques\n\nWhat would you like to discuss?",
    
    'default': "Thank you for sharing that with me. I'm here to support you. Remember:\n\n✓ Your feelings are valid\n✓ You're not alone\n✓ Seeking help is strength\n✓ Healing takes time\n\nWhat else can I help you with today?"
}


def get_bot_response(user_message):
    """Generate bot response based on user message"""
    message_lower = user_message.lower()
    
    # Check for critical keywords first
    if any(word in message_lower for word in ['suicide', 'kill myself', 'end it', 'suicidal']):
        return CHATBOT_RESPONSES['suicide']
    
    # Check other keywords
    for keyword, response in CHATBOT_RESPONSES.items():
        if keyword != 'default' and keyword in message_lower:
            return response
    
    # Default response
    return CHATBOT_RESPONSES['default']


@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    """Send a message to the chatbot"""
    from app import db, ChatMessage, User
    data = request.get_json()
    user_id = data.get('user_id')
    user_message = data.get('message')
    
    if not user_id or not user_message:
        return jsonify({'error': 'Missing user_id or message'}), 400
    
    # Validate user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get bot response
    bot_response = get_bot_response(user_message)
    
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
        'chat_id': chat_msg.id
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
