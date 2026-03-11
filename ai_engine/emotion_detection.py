"""
Emotion Detection Module
Detects emotions from text and facial expressions (mock implementation)
"""

import re
from typing import Dict, Tuple

class EmotionDetector:
    """Detects emotions from text input"""
    
    # Emotion keywords for text analysis
    EMOTION_KEYWORDS = {
        'happy': ['happy', 'joyful', 'excited', 'excellent', 'amazing', 'wonderful', 'great', 'love', '😊', '😄'],
        'sad': ['sad', 'unhappy', 'depressed', 'down', 'blue', 'miserable', 'terrible', 'awful', '😢', '😞'],
        'anxious': ['anxious', 'nervous', 'worried', 'stressed', 'panic', 'fear', 'scared', 'tense', '😰', '😟'],
        'angry': ['angry', 'mad', 'furious', 'frustrated', 'hostile', 'annoyed', 'irritated', '😠', '😡'],
        'calm': ['calm', 'peaceful', 'relaxed', 'serene', 'tranquil', 'chill', 'zen', '😌', '☮️'],
        'neutral': ['ok', 'fine', 'alright', 'normal', 'okay', 'average', '😐', '🙂']
    }
    
    # Intensity multipliers
    INTENSITY_WORDS = {
        'very': 1.5,
        'extremely': 2.0,
        'so': 1.5,
        'really': 1.5,
        'quite': 1.3,
        'slightly': 0.7,
        'little': 0.7
    }
    
    def __init__(self):
        self.emotion_scores = {}
    
    def analyze_text(self, text: str) -> Dict[str, float]:
        """
        Analyze text and return emotion scores
        
        Args:
            text: User input text
            
        Returns:
            Dictionary of emotions with confidence scores
        """
        text_lower = text.lower()
        self.emotion_scores = {emotion: 0.0 for emotion in self.EMOTION_KEYWORDS}
        
        # Tokenize text
        words = re.findall(r'\b\w+\b', text_lower)
        
        for i, word in enumerate(words):
            # Check intensity multiplier
            intensity = 1.0
            if i > 0 and words[i-1] in self.INTENSITY_WORDS:
                intensity = self.INTENSITY_WORDS[words[i-1]]
            
            # Check emotion keywords
            for emotion, keywords in self.EMOTION_KEYWORDS.items():
                if word in keywords:
                    self.emotion_scores[emotion] += intensity
        
        # Normalize scores
        total = sum(self.emotion_scores.values())
        if total > 0:
            self.emotion_scores = {
                emotion: score / total for emotion, score in self.emotion_scores.items()
            }
        
        return self.emotion_scores
    
    def detect_primary_emotion(self, text: str) -> Tuple[str, float]:
        """
        Detect the primary emotion from text
        
        Args:
            text: User input text
            
        Returns:
            Tuple of (emotion, confidence)
        """
        scores = self.analyze_text(text)
        
        if not scores or max(scores.values()) == 0:
            return 'neutral', 0.5
        
        primary_emotion = max(scores, key=scores.get)
        confidence = scores[primary_emotion]
        
        return primary_emotion, confidence
    
    def detect_emotion_intensity(self, text: str) -> Dict[str, any]:
        """
        Detect emotion and its intensity
        
        Args:
            text: User input text
            
        Returns:
            Dictionary with emotion, intensity (1-10), and confidence
        """
        emotion, confidence = self.detect_primary_emotion(text)
        
        # Calculate intensity (1-10)
        intensity = max(1, min(10, int(confidence * 10)))
        
        return {
            'emotion': emotion,
            'intensity': intensity,
            'confidence': confidence,
            'all_scores': self.emotion_scores
        }
    
    def detect_crisis_indicators(self, text: str) -> bool:
        """
        Detect crisis indicators (suicide, self-harm, etc.)
        
        Args:
            text: User input text
            
        Returns:
            Boolean indicating if crisis indicators are present
        """
        crisis_keywords = [
            'suicide', 'kill myself', 'end it', 'suicidal',
            'self harm', 'self-harm', 'hurt myself', 'die',
            'no point', 'not worth it', 'give up'
        ]
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in crisis_keywords)
    
    def get_emotion_emoji(self, emotion: str) -> str:
        """Get emoji representation of emotion"""
        emoji_map = {
            'happy': '😊',
            'sad': '😢',
            'anxious': '😰',
            'angry': '😠',
            'calm': '😌',
            'neutral': '😐'
        }
        return emoji_map.get(emotion, '🤔')
    
    def get_emotion_color(self, emotion: str) -> str:
        """Get color representation of emotion"""
        color_map = {
            'happy': '#10b981',      # green
            'sad': '#0ea5e9',        # blue
            'anxious': '#f59e0b',    # amber
            'angry': '#ef4444',      # red
            'calm': '#8b5cf6',       # purple
            'neutral': '#64748b'     # slate
        }
        return color_map.get(emotion, '#6366f1')


# Initialize emotion detector
emotion_detector = EmotionDetector()


def detect_emotion(text: str) -> Dict:
    """
    Detect emotion from text
    
    Args:
        text: Input text to analyze
        
    Returns:
        Dictionary with emotion analysis results
    """
    return emotion_detector.detect_emotion_intensity(text)


def is_in_crisis(text: str) -> bool:
    """
    Check if user is in crisis
    
    Args:
        text: User input text
        
    Returns:
        Boolean indicating crisis status
    """
    return emotion_detector.detect_crisis_indicators(text)
