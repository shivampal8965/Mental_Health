"""
Chatbot Model Module
Advanced chatbot with NLP capabilities and mental health context
"""

from typing import Dict, List, Tuple
import re
try:
    from .emotion_detection import emotion_detector, is_in_crisis
except ImportError:
    from emotion_detection import emotion_detector, is_in_crisis

class ChatbotModel:
    """Advanced chatbot for mental health support"""
    
    def __init__(self):
        self.conversation_history = []
        self.user_context = {}
        
    # Mental health knowledge base
    KNOWLEDGE_BASE = {
        'anxiety': {
            'symptoms': ['racing heart', 'sweating', 'shortness of breath', 'panic', 'worry'],
            'techniques': [
                '🫁 Box breathing: 4 in, 4 hold, 4 out',
                '🌍 Grounding: 5 sights, 4 touches, 3 sounds, 2 smells, 1 taste',
                '💪 Progressive muscle relaxation',
                '🧘 Meditation and mindfulness',
                '🚶 Gentle exercise'
            ],
            'resources': 'If anxiety persists, consider speaking with a mental health professional.'
        },
        'depression': {
            'symptoms': ['sadness', 'hopelessness', 'loss of interest', 'fatigue', 'isolation'],
            'techniques': [
                '🚶 Get moving: even 10 minutes can help',
                '☀️ Get sunlight exposure',
                '🤝 Connect with others',
                '🎯 Set small, achievable goals',
                '💬 Talk to someone you trust'
            ],
            'resources': 'Depression is treatable. Please contact a mental health professional or crisis line.'
        },
        'stress': {
            'symptoms': ['tension', 'irritability', 'difficulty concentrating', 'sleep issues', 'fatigue'],
            'techniques': [
                '⏸️ Take regular breaks',
                '💆 Massage or stretching',
                '🎵 Listen to relaxing music',
                '🧘 Deep breathing exercises',
                '🎨 Creative activities'
            ],
            'resources': 'Chronic stress requires professional attention. Seek help if needed.'
        },
        'insomnia': {
            'symptoms': ['difficulty falling asleep', 'frequent waking', 'early morning awakening', 'poor sleep quality'],
            'techniques': [
                '⏰ Maintain consistent sleep schedule',
                '📱 No screens 1 hour before bed',
                '🌡️ Keep bedroom cool (60-67°F)',
                '📖 Read or meditate before sleep',
                '☕ Avoid caffeine after 2 PM'
            ],
            'resources': 'If sleep problems persist, consult a sleep specialist.'
        },
        'self_harm': {
            'symptoms': ['urge to hurt yourself', 'self-injury thoughts', 'emotional pain'],
            'techniques': [
                '🚨 REACH OUT NOW - Contact crisis line',
                '🧊 Hold ice cubes in your hands',
                '✏️ Draw on skin with marker instead',
                '🏃 Intense exercise to release tension',
                '💬 Talk to someone immediately'
            ],
            'resources': '🚨 Crisis Text Line: Text HOME to 741741 | National Suicide Prevention: 988'
        },
        'grief': {
            'symptoms': ['sadness', 'numbness', 'anger', 'guilt', 'loss'],
            'techniques': [
                '💭 Allow yourself to feel your emotions',
                '🗣️ Talk about the person',
                '🤝 Connect with support groups',
                '📖 Read about grief and loss',
                '📝 Write letters or journal'
            ],
            'resources': 'Grief counseling can provide valuable support during this time.'
        }
    }
    
    # Crisis hotlines and resources
    CRISIS_RESOURCES = {
        'us': {
            'suicide': '988 Suicide & Crisis Lifeline',
            'crisis_text': 'Text HOME to 741741',
            'emergency': '911'
        },
        'uk': {
            'crisis': '116 123 Samaritans',
            'urgent': '111 NHS Urgent Care'
        },
        'canada': {
            'crisis': '1-833-456-4566 National Crisis Line',
            'emergency': '911'
        }
    }
    
    def add_to_history(self, user_message: str, bot_response: str) -> None:
        """Add message to conversation history"""
        self.conversation_history.append({
            'user': user_message,
            'bot': bot_response
        })
    
    def analyze_user_input(self, text: str) -> Dict:
        """
        Analyze user input for emotion and content
        
        Args:
            text: User's message
            
        Returns:
            Analysis with emotion, topics, and crisis indicators
        """
        emotion_analysis = emotion_detector.detect_emotion_intensity(text)
        is_crisis = is_in_crisis(text)
        
        # Extract topics
        topics = self._extract_topics(text)
        
        return {
            'emotion': emotion_analysis['emotion'],
            'intensity': emotion_analysis['intensity'],
            'confidence': emotion_analysis['confidence'],
            'is_crisis': is_crisis,
            'topics': topics,
            'full_analysis': emotion_analysis
        }
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract mental health topics from text"""
        topics = []
        text_lower = text.lower()
        
        for topic in self.KNOWLEDGE_BASE.keys():
            if topic.replace('_', ' ') in text_lower or topic.replace('_', '') in text_lower.replace(' ', ''):
                topics.append(topic)
        
        return topics
    
    def generate_response(self, user_message: str) -> Tuple[str, Dict]:
        """
        Generate intelligent response
        
        Args:
            user_message: User's message
            
        Returns:
            Tuple of (response, analysis)
        """
        # Analyze input
        analysis = self.analyze_user_input(user_message)
        
        # Handle crisis
        if analysis['is_crisis']:
            response = self._get_crisis_response()
            self.add_to_history(user_message, response)
            return response, analysis
        
        # Handle specific topics
        if analysis['topics']:
            topic = analysis['topics'][0]
            response = self._get_topic_response(topic)
        else:
            # Generic supportive response
            response = self._get_generic_response(analysis)
        
        self.add_to_history(user_message, response)
        return response, analysis
    
    def _get_crisis_response(self) -> str:
        """Get crisis response"""
        return """
🚨 I'm very concerned about your safety right now.
        
IMMEDIATE HELP AVAILABLE:
📞 National Suicide Prevention Lifeline: 988 (US)
💬 Crisis Text Line: Text HOME to 741741
🏥 Go to nearest emergency room
🆘 Call 911
        
Your life has value. You matter. Please reach out NOW. 💙
        
People care about you and want to help.
"""
    
    def _get_topic_response(self, topic: str) -> str:
        """Get response for specific topic"""
        if topic not in self.KNOWLEDGE_BASE:
            return self._get_generic_response({})
        
        kb = self.KNOWLEDGE_BASE[topic]
        title = topic.replace('_', ' ').title()
        
        response = f"""
🫂 I'm here for you regarding {title}.

**Techniques that might help:**
"""
        for technique in kb['techniques']:
            response += f"\n{technique}"
        
        response += f"\n\n📚 {kb['resources']}"
        
        return response
    
    def _get_generic_response(self, analysis: Dict) -> str:
        """Get generic supportive response"""
        emotion = analysis.get('emotion', 'neutral')
        intensity = analysis.get('intensity', 5)
        
        templates = {
            'happy': "That's wonderful! 😊 Keep doing what brings you joy.",
            'sad': "I hear you. It's okay to feel sad. Would you like to talk more about it?",
            'anxious': "Anxiety is tough. Let's work through this together. Would breathing exercises help?",
            'angry': "It sounds like you're frustrated. That's valid. Want to discuss what's upsetting you?",
            'calm': "I'm glad you're feeling calm. That's a great state to be in. 🧘",
            'neutral': "I'm here to listen and support you. What's on your mind?"
        }
        
        response = templates.get(emotion, templates['neutral'])
        
        if intensity > 7:
            response += "\n\n💙 Remember: Your feelings are valid. You're not alone in this."
        
        return response
    
    def get_wellness_tips(self) -> List[str]:
        """Get daily wellness tips"""
        tips = [
            '🧘 Practice 5 minutes of mindfulness meditation',
            '🚶 Take a 15-minute walk in fresh air',
            '💧 Drink plenty of water throughout the day',
            '😊 Do one thing that makes you smile',
            '🤝 Connect with someone you care about',
            '💪 Do some light stretching or exercise',
            '📝 Write down something you\'re grateful for',
            '🎵 Listen to music that uplifts you',
            '🧠 Practice positive self-talk',
            '💤 Get 7-9 hours of quality sleep'
        ]
        return tips
    
    def get_crisis_resources(self, country: str = 'us') -> Dict:
        """Get crisis resources for country"""
        return self.CRISIS_RESOURCES.get(country, self.CRISIS_RESOURCES['us'])


# Initialize chatbot
chatbot = ChatbotModel()


def chat(user_message: str) -> Tuple[str, Dict]:
    """
    Chat with the mental health chatbot
    
    Args:
        user_message: User's message
        
    Returns:
        Tuple of (response, analysis)
    """
    return chatbot.generate_response(user_message)


def get_wellness_tips() -> List[str]:
    """Get daily wellness tips"""
    return chatbot.get_wellness_tips()


def get_crisis_resources(country: str = 'us') -> Dict:
    """Get crisis resources"""
    return chatbot.get_crisis_resources(country)
