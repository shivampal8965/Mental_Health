# 🚀 Quick Start Guide - MindCare Mental Health System

Get your Mental Health System up and running in 5 minutes!

---

## 📥 Option 1: Quick Start (Recommended for Beginners)

### Step 1: Install Python
- Download Python 3.9+ from https://www.python.org/downloads/
- During installation, **check "Add Python to PATH"**

### Step 2: Extract the Project
- Extract the Mental Health folder to your desired location

### Step 3: Open Terminal/Command Prompt
```powershell
# On Windows, press Win + R and type: cmd
# Navigate to the project folder:
cd "path\to\Mental Health"
```

### Step 4: Create Virtual Environment
```powershell
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux
```

### Step 5: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 6: Start Backend Server
```powershell
cd backend
python app.py
```

**Backend is now running at:** `http://localhost:5000`

### Step 7: Start Frontend (New Terminal)
```powershell
# New terminal tab while backend is running
cd frontend
python -m http.server 8000
```

**Frontend is now available at:** `http://localhost:8000`

---

## 🐳 Option 2: Docker Quick Start (For Advanced Users)

### Step 1: Install Docker
- Download Docker Desktop from https://www.docker.com/products/docker-desktop
- Install and start Docker

### Step 2: Navigate to Project
```bash
cd "path\to\Mental Health"
```

### Step 3: Run Docker Compose
```bash
docker-compose up -d
```

**Services are now running:**
- Frontend: http://localhost
- Backend API: http://localhost:5000
- Database: localhost:5432

### Step 4: Stop Services
```bash
docker-compose down
```

---

## 🎯 Using the Application

### 1. **Visit the Website**
   - Open your browser
   - Go to `http://localhost:8000` (local) or appropriate URL
   - Read about MindCare features

### 2. **Register Account**
   - Click "Get Started"
   - Enter username, email, password
   - Complete registration

### 3. **Login**
   - Use your credentials to login
   - Access your personal dashboard

### 4. **Track Mood**
   - Go to "Mood Tracker"
   - Select your current emotion
   - Rate energy (1-10) and stress (1-10)
   - Add notes and activities
   - Save entry

### 5. **View Dashboard**
   - See mood trends in charts
   - Check statistics
   - Review recent activities

### 6. **Chat with AI**
   - Go to "AI Chatbot"
   - Ask questions or select quick options
   - Get personalized mental health support
   - Access wellness tips

---

## 📊 API Testing

### Test with cURL or Postman

```bash
# Register User
curl -X POST http://localhost:5000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'

# Login
curl -X POST http://localhost:5000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'

# Log Mood
curl -X POST http://localhost:5000/api/moods/log \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "mood": 3,
    "energy_level": 7,
    "stress_level": 4,
    "sleep_quality": 4,
    "notes": "Feeling good today!"
  }'

# Get Moods
curl -X GET http://localhost:5000/api/moods/user/1

# Chat
curl -X POST http://localhost:5000/api/chatbot/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "message": "I feel anxious"
  }'
```

---

## 🔧 Common Issues & Solutions

### Issue: "Python not found"
**Solution:** 
- Reinstall Python with "Add Python to PATH" enabled
- Restart terminal after installation

### Issue: Port 5000 already in use
**Solution:**
```bash
# Find and kill process on port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :5000
kill -9 <PID>
```

### Issue: "ModuleNotFoundError"
**Solution:**
```bash
# Make sure virtual environment is activated
# Then reinstall requirements
pip install -r requirements.txt --upgrade
```

### Issue: Database locked
**Solution:**
```bash
# Delete database and restart
rm backend/database/db.sqlite
python -c "from app import db; db.create_all()"
```

### Issue: Frontend not loading
**Solution:**
- Make sure both backend and frontend servers are running
- Check terminal for error messages
- Clear browser cache (Ctrl+Shift+Delete)

---

## 📁 Project Structure Quick Reference

```
Mental Health/
├── frontend/              # Web UI
│   ├── index.html        # Landing page
│   ├── dashboard.html    # Main dashboard
│   ├── mood_tracker.html # Mood logging
│   ├── chatbot.html      # AI chatbot
│   ├── styles.css        # Styling
│   └── app.js            # Frontend logic
│
├── backend/              # REST API
│   ├── app.py           # Flask server
│   ├── routes/          # API endpoints
│   └── database/        # SQLite DB
│
├── ai_engine/           # AI/ML Components
│   ├── emotion_detection.py
│   ├── stress_prediction.py
│   └── chatbot_model.py
│
└── requirements.txt     # Python dependencies
```

---

## 🔐 Security Notes

- ⚠️ **Never commit `.env` file with secrets**
- 🔑 **Change SECRET_KEY in production**
- 🛡️ **Use HTTPS in production**
- 📝 **Keep dependencies updated**
- 🚨 **Always validate user input**

---

## 📚 Next Steps

1. **Read Full Documentation**
   - See README.md for detailed documentation

2. **Customize the System**
   - Modify chatbot responses in `ai_engine/chatbot_model.py`
   - Change UI colors in `frontend/styles.css`
   - Add database fields in `backend/app.py`

3. **Deploy to Production**
   - Follow deployment guide in README.md
   - Use Docker for containerized deployment
   - Deploy to Heroku, AWS, or Google Cloud

4. **Add Features**
   - Mobile app support
   - Email notifications
   - Advanced analytics
   - Integration with professional services

---

## 💡 Tips

- 📖 **Learn Flask:** https://flask.palletsprojects.com/
- 🎨 **Web Design:** https://www.w3schools.com/
- 🤖 **AI/ML:** https://scikit-learn.org/
- 🐳 **Docker:** https://docs.docker.com/

---

## 🆘 Need Help?

- 📖 Check README.md for detailed documentation
- 🐛 Look for error messages in terminal
- 💬 Check the Issues section on GitHub
- 📧 Contact support

---

## ✅ Checklist

- [ ] Python 3.9+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Backend running (port 5000)
- [ ] Frontend running (port 8000)
- [ ] Can access http://localhost:8000
- [ ] Can register new user
- [ ] Can log in
- [ ] Can track mood
- [ ] Can chat with AI

**Congratulations! You're ready to use MindCare! 🎉**

---

Made with ❤️ for mental health
