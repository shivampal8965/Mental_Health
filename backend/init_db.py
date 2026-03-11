"""
Database Initialization Script
Initialize database with sample data
"""

import sys
sys.path.insert(0, '.')

from app import app, db, User, MoodEntry, ChatMessage
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def init_database():
    """Initialize database with sample data"""
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created")
        
        # Check if sample user exists
        if User.query.filter_by(username='demo_user').first():
            print("⚠️  Sample data already exists. Skipping initialization.")
            return
        
        # Create sample user
        sample_user = User(
            username='demo_user',
            email='demo@mindcare.ai',
            password=generate_password_hash('demo123')
        )
        db.session.add(sample_user)
        db.session.commit()
        print("✅ Sample user created (username: demo_user, password: demo123)")
        
        # Create sample mood entries
        for i in range(7):
            mood_entry = MoodEntry(
                user_id=sample_user.id,
                mood=3 + (i % 3) - 1,  # Vary between 2-4
                energy_level=5 + (i % 5) - 2,  # Vary between 3-7
                stress_level=5 + (i % 4) - 2,  # Vary between 3-7
                sleep_quality=3 + (i % 3) - 1,  # Vary between 2-4
                notes=f"Sample mood entry {i+1}",
                activities="exercise,meditation" if i % 2 == 0 else "work,reading",
                created_at=datetime.utcnow() - timedelta(days=i)
            )
            db.session.add(mood_entry)
        
        db.session.commit()
        print("✅ Sample mood entries created")
        
        # Create sample chat messages
        for i in range(3):
            chat_msg = ChatMessage(
                user_id=sample_user.id,
                user_message=f"I'm feeling {['anxious', 'stressed', 'happy'][i]} today",
                bot_response=f"Thank you for sharing. Here are some helpful tips for managing {['anxiety', 'stress', 'happiness'][i]}...",
                created_at=datetime.utcnow() - timedelta(hours=i)
            )
            db.session.add(chat_msg)
        
        db.session.commit()
        print("✅ Sample chat messages created")
        
        print("\n" + "="*50)
        print("🎉 Database initialization complete!")
        print("="*50)
        print("\n📝 Test Credentials:")
        print("   Username: demo_user")
        print("   Password: demo123")
        print("   Email: demo@mindcare.ai")
        print("\n🚀 You can now log in and explore the system!")
        print("="*50 + "\n")

if __name__ == '__main__':
    init_database()
