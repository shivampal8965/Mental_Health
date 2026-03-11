/**
 * MindCare Frontend - Main JavaScript File
 * Handles frontend interactions and API calls
 */

// Configuration
const API_BASE_URL = 'http://localhost:5000/api';
let currentUserId = null;
let authToken = null;

/**
 * Initialize the application
 */
function initApp() {
    console.log('🧠 MindCare Mental Health System Initialized');
    
    // Check if user is authenticated
    const savedToken = localStorage.getItem('authToken');
    if (savedToken) {
        authToken = savedToken;
        currentUserId = localStorage.getItem('userId');
    }
}

/**
 * Make API call
 */
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.status} ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Call Error:', error);
        throw error;
    }
}

/**
 * User Registration
 */
async function registerUser(username, email, password) {
    try {
        const response = await apiCall('/users/register', 'POST', {
            username: username,
            email: email,
            password: password
        });
        
        console.log('✅ User registered:', response);
        alert('Registration successful! Please login.');
        return response;
    } catch (error) {
        console.error('Registration error:', error);
        alert('❌ Registration failed: ' + error.message);
    }
}

/**
 * User Login
 */
async function loginUser(username, password) {
    try {
        const response = await apiCall('/users/login', 'POST', {
            username: username,
            password: password
        });
        
        // Save authentication data
        authToken = response.token;
        currentUserId = response.user.id;
        
        localStorage.setItem('authToken', authToken);
        localStorage.setItem('userId', currentUserId);
        localStorage.setItem('username', response.user.username);
        
        console.log('✅ Login successful:', response);
        alert('✅ Welcome back, ' + response.user.username + '!');
        
        // Redirect to dashboard
        window.location.href = 'dashboard.html';
        
        return response;
    } catch (error) {
        console.error('Login error:', error);
        alert('❌ Login failed: Invalid credentials');
    }
}

/**
 * Logout User
 */
function logoutUser() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userId');
    localStorage.removeItem('username');
    
    authToken = null;
    currentUserId = null;
    
    console.log('✅ Logged out successfully');
    window.location.href = 'index.html';
}

/**
 * Get User Profile
 */
async function getUserProfile() {
    try {
        const response = await apiCall(`/users/${currentUserId}`, 'GET');
        return response.user;
    } catch (error) {
        console.error('Error fetching user profile:', error);
    }
}

/**
 * Log Mood Entry
 */
async function logMood(moodData) {
    try {
        const response = await apiCall('/moods/log', 'POST', {
            user_id: currentUserId,
            ...moodData
        });
        
        console.log('✅ Mood logged:', response);
        alert('✅ Mood entry saved successfully!');
        return response;
    } catch (error) {
        console.error('Error logging mood:', error);
        alert('❌ Failed to save mood entry');
    }
}

/**
 * Get User Moods
 */
async function getUserMoods(days = 7) {
    try {
        const response = await apiCall(`/moods/user/${currentUserId}?days=${days}`, 'GET');
        return response.moods;
    } catch (error) {
        console.error('Error fetching moods:', error);
    }
}

/**
 * Get Mood Statistics
 */
async function getMoodStats(days = 30) {
    try {
        const response = await apiCall(`/moods/stats/user/${currentUserId}?days=${days}`, 'GET');
        return response.stats;
    } catch (error) {
        console.error('Error fetching stats:', error);
    }
}

/**
 * Send Chatbot Message
 */
async function sendChatMessage(message) {
    try {
        const response = await apiCall('/chatbot/chat', 'POST', {
            user_id: currentUserId,
            message: message
        });
        
        return response;
    } catch (error) {
        console.error('Error sending chat message:', error);
        throw error;
    }
}

/**
 * Get Chat History
 */
async function getChatHistory(limit = 50) {
    try {
        const response = await apiCall(`/chatbot/history/${currentUserId}?limit=${limit}`, 'GET');
        return response.messages;
    } catch (error) {
        console.error('Error fetching chat history:', error);
    }
}

/**
 * Get Wellness Tips
 */
async function getWellnessTips() {
    try {
        const response = await apiCall('/chatbot/wellness-tips', 'GET');
        return response.tips;
    } catch (error) {
        console.error('Error fetching wellness tips:', error);
    }
}

/**
 * Utility: Check if user is authenticated
 */
function isAuthenticated() {
    return authToken !== null && currentUserId !== null;
}

/**
 * Utility: Redirect if not authenticated
 */
function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = 'index.html';
        return false;
    }
    return true;
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    const alertClass = `alert alert-${type}`;
    const alertHTML = `<div class="${alertClass}" role="alert">${message}</div>`;
    
    // Insert at top of page
    document.body.insertAdjacentHTML('afterbegin', alertHTML);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        document.querySelector('.alert')?.remove();
    }, 5000);
}

/**
 * Submit a rating/feedback
 */
async function submitRating(ratingData) {
    try {
        const response = await apiCall('/ratings/submit', 'POST', {
            user_id: currentUserId,
            overall: ratingData.overall,
            mood_tracking: ratingData.moodTracking,
            chatbot: ratingData.chatbot,
            ui: ratingData.ui,
            analytics: ratingData.analytics,
            recommend: ratingData.recommend,
            comments: ratingData.comments,
            email: ratingData.email
        });
        
        console.log('✅ Rating submitted:', response);
        return response;
    } catch (error) {
        console.error('Rating submission error:', error);
        alert('❌ Failed to submit rating: ' + error.message);
    }
}

/**
 * Get all ratings
 */
async function getAllRatings(limit = 50) {
    try {
        const response = await apiCall(`/ratings/all?limit=${limit}`, 'GET');
        console.log('✅ Ratings fetched:', response);
        return response;
    } catch (error) {
        console.error('Error fetching ratings:', error);
    }
}

/**
 * Get rating statistics
 */
async function getRatingStats() {
    try {
        const response = await apiCall('/ratings/stats', 'GET');
        console.log('✅ Rating stats fetched:', response);
        return response;
    } catch (error) {
        console.error('Error fetching rating stats:', error);
    }
}

/**
 * Create a new goal
 */
async function createGoal(goalData) {
    try {
        const response = await apiCall('/goals/create', 'POST', {
            user_id: currentUserId,
            name: goalData.name,
            description: goalData.description,
            category: goalData.category,
            target_date: goalData.targetDate,
            status: goalData.status || 'active'
        });
        
        console.log('✅ Goal created:', response);
        return response;
    } catch (error) {
        console.error('Goal creation error:', error);
        alert('❌ Failed to create goal: ' + error.message);
    }
}

/**
 * Get user's goals
 */
async function getUserGoals(userId = null, status = null) {
    try {
        const id = userId || currentUserId;
        let endpoint = `/goals/user/${id}`;
        
        if (status) {
            endpoint += `?status=${status}`;
        }
        
        const response = await apiCall(endpoint, 'GET');
        console.log('✅ User goals fetched:', response);
        return response;
    } catch (error) {
        console.error('Error fetching goals:', error);
    }
}

/**
 * Get a specific goal
 */
async function getGoal(goalId) {
    try {
        const response = await apiCall(`/goals/${goalId}`, 'GET');
        console.log('✅ Goal fetched:', response);
        return response;
    } catch (error) {
        console.error('Error fetching goal:', error);
    }
}

/**
 * Update a goal
 */
async function updateGoal(goalId, goalData) {
    try {
        const response = await apiCall(`/goals/${goalId}`, 'PUT', {
            name: goalData.name,
            description: goalData.description,
            category: goalData.category,
            progress: goalData.progress,
            status: goalData.status,
            target_date: goalData.targetDate
        });
        
        console.log('✅ Goal updated:', response);
        return response;
    } catch (error) {
        console.error('Goal update error:', error);
        alert('❌ Failed to update goal: ' + error.message);
    }
}

/**
 * Update goal progress
 */
async function updateGoalProgress(goalId, progress) {
    try {
        const response = await apiCall(`/goals/${goalId}/progress`, 'PUT', {
            progress: progress
        });
        
        console.log('✅ Goal progress updated:', response);
        return response;
    } catch (error) {
        console.error('Goal progress update error:', error);
        alert('❌ Failed to update goal progress: ' + error.message);
    }
}

/**
 * Delete a goal
 */
async function deleteGoal(goalId) {
    try {
        const response = await apiCall(`/goals/${goalId}`, 'DELETE');
        console.log('✅ Goal deleted:', response);
        return response;
    } catch (error) {
        console.error('Goal deletion error:', error);
        alert('❌ Failed to delete goal: ' + error.message);
    }
}

/**
 * Get user's goal statistics
 */
async function getUserGoalStats(userId = null) {
    try {
        const id = userId || currentUserId;
        const response = await apiCall(`/goals/user/${id}/stats`, 'GET');
        console.log('✅ Goal stats fetched:', response);
        return response;
    } catch (error) {
        console.error('Error fetching goal stats:', error);
    }
}

/**
 * Format date
 */
function formatDate(date) {
    if (typeof date === 'string') {
        date = new Date(date);
    }
    
    const options = {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    
    return date.toLocaleDateString('en-US', options);
}

/**
 * Get emotion emoji
 */
function getEmotionEmoji(mood) {
    const emojis = {
        0: '😭',  // Overwhelmed
        1: '😢',  // Very Sad
        2: '😔',  // Sad
        3: '😐',  // Neutral
        4: '😊',  // Happy
        5: '😄'   // Excited
    };
    return emojis[mood] || '🤔';
}

/**
 * Format mood name
 */
function getMoodName(mood) {
    const names = {
        0: 'Overwhelmed',
        1: 'Very Sad',
        2: 'Sad',
        3: 'Neutral',
        4: 'Happy',
        5: 'Excited'
    };
    return names[mood] || 'Unknown';
}

// Initialize app on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
} else {
    initApp();
}
