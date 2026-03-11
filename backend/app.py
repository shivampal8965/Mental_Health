from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mental-health-secret-key-2026'

# Set database path - create absolute path if running from different directory
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'db.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)

# Database Models
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    moods = db.relationship('MoodEntry', backref='user', lazy=True, cascade='all, delete-orphan')
    chats = db.relationship('ChatMessage', backref='user', lazy=True, cascade='all, delete-orphan')
    goals = db.relationship('Goal', backref='user', lazy=True, cascade='all, delete-orphan')
    ratings = db.relationship('Rating', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }


class MoodEntry(db.Model):
    __tablename__ = 'mood_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mood = db.Column(db.Integer, nullable=False)  # 0-5 scale
    energy_level = db.Column(db.Integer, nullable=True)  # 1-10
    stress_level = db.Column(db.Integer, nullable=True)  # 1-10
    sleep_quality = db.Column(db.Integer, nullable=True)  # 1-5
    notes = db.Column(db.Text, nullable=True)
    activities = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'mood': self.mood,
            'energy_level': self.energy_level,
            'stress_level': self.stress_level,
            'sleep_quality': self.sleep_quality,
            'notes': self.notes,
            'activities': self.activities,
            'created_at': self.created_at.isoformat()
        }


class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_message': self.user_message,
            'bot_response': self.bot_response,
            'created_at': self.created_at.isoformat()
        }


class Goal(db.Model):
    __tablename__ = 'goals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), default='general')  # daily routine, exercise, mental health, etc.
    target_date = db.Column(db.DateTime, nullable=True)
    progress = db.Column(db.Integer, default=0)  # 0-100
    status = db.Column(db.String(50), default='active')  # active, completed, abandoned
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'target_date': self.target_date.isoformat() if self.target_date else None,
            'progress': self.progress,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Rating(db.Model):
    __tablename__ = 'ratings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    overall = db.Column(db.Integer, nullable=False)  # 1-5
    mood_tracking = db.Column(db.Integer, nullable=True)  # 1-5
    chatbot = db.Column(db.Integer, nullable=True)  # 1-5
    ui = db.Column(db.Integer, nullable=True)  # 1-5
    analytics = db.Column(db.Integer, nullable=True)  # 1-5
    recommend = db.Column(db.String(50), nullable=True)  # yes, maybe, no
    comments = db.Column(db.Text, nullable=True)
    email = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'overall': self.overall,
            'mood_tracking': self.mood_tracking,
            'chatbot': self.chatbot,
            'ui': self.ui,
            'analytics': self.analytics,
            'recommend': self.recommend,
            'comments': self.comments,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }


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
