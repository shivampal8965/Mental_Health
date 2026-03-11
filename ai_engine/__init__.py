"""
AI Engine Module
Advanced ML and AI components for mental health analysis
"""

from .emotion_detection import emotion_detector, detect_emotion, is_in_crisis
from .stress_prediction import stress_predictor, predict_stress, get_stress_trend
from .chatbot_model import chatbot, chat, get_wellness_tips, get_crisis_resources

__all__ = [
    'emotion_detector',
    'detect_emotion',
    'is_in_crisis',
    'stress_predictor',
    'predict_stress',
    'get_stress_trend',
    'chatbot',
    'chat',
    'get_wellness_tips',
    'get_crisis_resources'
]
