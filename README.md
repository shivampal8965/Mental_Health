# 🧠 MindCare - Mental Health System

A comprehensive AI-powered mental health support system with mood tracking, emotional intelligence, stress prediction, and an intelligent chatbot.

![MindCare Banner](https://img.shields.io/badge/Mental%20Health%20System-Professional%20Support-6366f1)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

---

## ✨ Features

### 🎯 Core Features

1. **Mood Tracking Dashboard**
   - Daily mood logging with emoji-based emotions
   - Energy and stress level tracking (1-10 scale)
   - Sleep quality assessment
   - Activity logging (exercise, meditation, socializing, etc.)
   - Historical mood data visualization
   - Weekly/Monthly trend analysis

2. **AI Chatbot** 🤖
   - 24/7 mental health support
   - Emotion detection from text
   - Crisis detection and resource guidance
   - Personalized responses
   - Conversation history
   - Wellness tips and recommendations

3. **Emotion Detection** 👁️
   - Text-based emotion analysis
   - Intensity assessment
   - Crisis indicator detection
   - Emotion patterns and trends

4. **Stress Prediction** 📊
   - Real-time stress level prediction
   - Trend analysis and forecasting
   - Activity impact assessment
   - Personalized recommendations
   - Early warning system

5. **Analytics Dashboard** 📈
   - Visual mood trends
   - Stress level charts
   - Energy patterns
   - Sleep quality metrics
   - Weekly/monthly statistics

6. **User Management** 👤
   - Secure user registration
   - JWT-based authentication
   - Profile management
   - Data privacy and encryption

---

## 🏗️ Project Structure

```
mental-health-system/
│
├── frontend/                      # React/HTML Frontend
│   ├── index.html                # Landing page
│   ├── dashboard.html            # Main dashboard
│   ├── mood_tracker.html         # Mood logging interface
│   ├── chatbot.html              # AI chatbot interface
│   └── styles.css                # Global styling
│
├── backend/                       # Flask REST API
│   ├── app.py                    # Main Flask application
│   ├── routes/
│   │   ├── user.py              # User management endpoints
│   │   ├── mood.py              # Mood tracking endpoints
│   │   └── chatbot.py           # Chatbot endpoints
│   └── database/
│       └── db.sqlite            # SQLite database
│
├── ai_engine/                    # AI/ML Components
│   ├── emotion_detection.py     # Emotion analysis
│   ├── stress_prediction.py     # Stress forecasting
│   └── chatbot_model.py         # Advanced chatbot logic
│
├── data/                         # Data files
│   └── mental_health_dataset.csv # Sample dataset
│
├── requirements.txt              # Python dependencies
├── docker-compose.yml            # Docker configuration
└── README.md                     # This file
```

---

## 💻 System Requirements

- **Python**: 3.9 or higher
- **Node.js**: 14.0 or higher (optional, for frontend build)
- **Database**: SQLite (included) or PostgreSQL (for production)
- **OS**: Windows, macOS, or Linux
- **RAM**: Minimum 2GB (4GB recommended)
- **Disk Space**: 500MB minimum

---

## 🚀 Installation

### Option 1: Local Development Setup

#### Prerequisites
```bash
# Install Python 3.9+
# Download from https://www.python.org/downloads/
```

#### Steps

1. **Clone or Download the Project**
```bash
cd "Mental Health"
```

2. **Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Run Backend Server**
```bash
cd backend
python app.py
```
The API will be available at `http://localhost:5000`

5. **Run Frontend**
```bash
# Open in browser
frontend/index.html
# Or use a local server:
python -m http.server 8000 --directory frontend
```
The frontend will be available at `http://localhost:8000`

### Option 2: Docker Setup

1. **Install Docker**
   - Download from https://www.docker.com/products/docker-desktop

2. **Run with Docker Compose**
```bash
docker-compose up -d
```

3. **Access Services**
   - Frontend: http://localhost
   - API: http://localhost:5000
   - Database: localhost:5432

---

## 📖 Usage

### Web Interface

1. **Register/Login**
   - Create an account with email and password
   - Login to access your dashboard

2. **Dashboard**
   - View mood statistics
   - Check stress trends
   - See recent activities
   - Access quick actions

3. **Mood Tracking**
   - Log daily mood (6 emotions: excited, happy, neutral, sad, very sad, overwhelmed)
   - Rate energy level (1-10)
   - Rate stress level (1-10)
   - Add notes and activities
   - View mood history

4. **AI Chatbot**
   - Chat with AI assistant 24/7
   - Use quick options for common topics
   - Get wellness tips
   - Access crisis resources if needed

### API Endpoints

#### User Management
```
POST   /api/users/register          # Register new user
POST   /api/users/login             # Login user
GET    /api/users/<id>              # Get user profile
PUT    /api/users/<id>              # Update user
DELETE /api/users/<id>              # Delete user
```

#### Mood Tracking
```
POST   /api/moods/log               # Log mood entry
GET    /api/moods/user/<id>         # Get user moods
GET    /api/moods/<id>              # Get mood entry
PUT    /api/moods/<id>              # Update mood entry
DELETE /api/moods/<id>              # Delete mood entry
GET    /api/moods/stats/user/<id>   # Get mood statistics
```

#### Chatbot
```
POST   /api/chatbot/chat            # Send message to chatbot
GET    /api/chatbot/history/<id>    # Get chat history
GET    /api/chatbot/suggestions     # Get chat suggestions
GET    /api/chatbot/wellness-tips   # Get wellness tips
```

---

## 📊 API Documentation

### Register User
```bash
POST /api/users/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password"
}

Response:
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "created_at": "2026-03-09T10:00:00"
  }
}
```

### Log Mood
```bash
POST /api/moods/log
Content-Type: application/json

{
  "user_id": 1,
  "mood": 3,
  "energy_level": 7,
  "stress_level": 4,
  "sleep_quality": 4,
  "notes": "Had a great day!",
  "activities": "exercise,meditation"
}

Response:
{
  "message": "Mood logged successfully",
  "mood_entry": {
    "id": 1,
    "mood": 3,
    "energy_level": 7,
    "stress_level": 4,
    "sleep_quality": 4,
    "notes": "Had a great day!",
    "created_at": "2026-03-09T10:00:00"
  }
}
```

### Chat with Bot
```bash
POST /api/chatbot/chat
Content-Type: application/json

{
  "user_id": 1,
  "message": "I'm feeling anxious today"
}

Response:
{
  "user_message": "I'm feeling anxious today",
  "bot_response": "I understand you're feeling anxious...",
  "chat_id": 1
}
```

---

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  username VARCHAR(80) UNIQUE NOT NULL,
  email VARCHAR(120) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Mood Entries Table
```sql
CREATE TABLE mood_entries (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  mood INTEGER NOT NULL,
  energy_level INTEGER,
  stress_level INTEGER,
  sleep_quality INTEGER,
  notes TEXT,
  activities VARCHAR(255),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(user_id) REFERENCES users(id)
);
```

### Chat Messages Table
```sql
CREATE TABLE chat_messages (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  user_message TEXT NOT NULL,
  bot_response TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(user_id) REFERENCES users(id)
);
```

---

## ⚙️ Configuration

### Environment Variables
Create a `.env` file in the backend directory:

```env
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
SQLALCHEMY_DATABASE_URI=sqlite:///database/db.sqlite
CHATBOT_MODEL=advanced
EMOTION_DETECTION_THRESHOLD=0.5
```

### Database Configuration
Update in `backend/app.py`:

```python
# SQLite (Development)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/db.sqlite'

# PostgreSQL (Production)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/db_name'
```

---

## 🐳 Deployment

### Docker Deployment

1. **Build and Run**
```bash
docker-compose up -d
```

2. **Check Services**
```bash
docker-compose ps
docker-compose logs -f backend
```

3. **Stop Services**
```bash
docker-compose down
```

### Cloud Deployment

#### Heroku
```bash
heroku create mindcare-app
heroku config:set FLASK_ENV=production
git push heroku main
```

#### AWS
```bash
# Install AWS CLI
aws configure

# Deploy using Elastic Beanstalk
eb create mindcare-env
eb deploy
```

#### Google Cloud
```bash
gcloud app deploy
gcloud app browse
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Comment complex logic

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🆘 Support

### Mental Health Resources

If you or someone you know is struggling:

- **National Suicide Prevention Lifeline (US): 988**
- **Crisis Text Line: Text HOME to 741741**
- **International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/**

### Technical Support

- 📧 Email: support@mindcare.ai
- 📝 Issues: https://github.com/yourusername/mental-health-system/issues
- 💬 Discussions: https://github.com/yourusername/mental-health-system/discussions

---

## 📊 Feature Roadmap

- [ ] Mobile app (iOS/Android)
- [ ] Video therapy integration
- [ ] Peer support groups
- [ ] Mental health professionals directory
- [ ] Prescription tracking
- [ ] Integration with wearables (Apple Watch, Fitbit)
- [ ] Offline mode support
- [ ] Multi-language support
- [ ] Data export (PDF reports)
- [ ] API rate limiting and quotas

---

## 🙏 Acknowledgments

- Inspired by the need for accessible mental health support
- Built with love and compassion for mental health
- Thanks to the open-source community

---

## ⚖️ Disclaimer

**Important:** This system is not a replacement for professional mental health treatment. If you are experiencing a mental health crisis, please contact:
- **National Suicide Prevention Lifeline: 988 (US)**
- **Crisis Text Line: Text HOME to 741741**
- **Emergency Services: 911**

Always seek professional help when needed. Your mental health matters. 💙

---

**Made with ❤️ for mental health awareness and support**

Last Updated: March 2026
