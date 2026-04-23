from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import os
import sys

# Add project root to sys.path for ai_engine imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import db, User, MoodEntry, ChatMessage, Goal, Rating

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mental-health-secret-key-2026'

# Set database path - create absolute path if running from different directory
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'db.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
CORS(app)

# Root endpoint
@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'message': 'Welcome to MindCare Mental Health System API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health',
            'users': '/api/users',
            'moods': '/api/moods',
            'chatbot': '/api/chatbot',
            'ratings': '/api/ratings',
            'goals': '/api/goals'
        }
    }), 200


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500


# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'message': 'Mental Health System is running'}), 200


# Import and register blueprints
from routes.user import user_bp
from routes.mood import mood_bp
from routes.chatbot import chatbot_bp
from routes.ratings import ratings_bp
from routes.goals import goals_bp

app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(mood_bp, url_prefix='/api/moods')
app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')
app.register_blueprint(ratings_bp, url_prefix='/api/ratings')
app.register_blueprint(goals_bp, url_prefix='/api/goals')


if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
