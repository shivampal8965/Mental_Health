"""
Stress Prediction Module
Predicts stress levels based on mood data and patterns
"""

from typing import List, Dict
from datetime import datetime, timedelta
import statistics

class StressPredictor:
    """Predicts stress levels and provides recommendations"""
    
    # Stress thresholds
    STRESS_LEVELS = {
        'low': (0, 3),
        'moderate': (3, 6),
        'high': (6, 8),
        'critical': (8, 10)
    }
    
    # Activity impact on stress
    ACTIVITY_IMPACT = {
        'exercise': -0.3,      # Reduces stress
        'meditation': -0.4,
        'socializing': -0.2,
        'work': 0.2,           # Increases stress
        'family_time': -0.25,
        'hobbies': -0.35,
        'sleep_good': -0.3,
        'sleep_bad': 0.4
    }
    
    def __init__(self):
        self.historical_data = []
    
    def add_mood_entry(self, mood_data: Dict) -> None:
        """
        Add a mood entry to historical data
        
        Args:
            mood_data: Dictionary containing mood information
        """
        self.historical_data.append({
            'timestamp': datetime.utcnow(),
            'mood': mood_data.get('mood'),
            'energy': mood_data.get('energy_level'),
            'stress': mood_data.get('stress_level'),
            'sleep': mood_data.get('sleep_quality'),
            'activities': mood_data.get('activities', [])
        })
    
    def calculate_stress_trend(self, days: int = 7) -> Dict[str, float]:
        """
        Calculate stress trend over N days
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Dictionary with trend information
        """
        if not self.historical_data:
            return {
                'trend': 'stable',
                'average_stress': 0,
                'max_stress': 0,
                'min_stress': 0,
                'change': 0
            }
        
        recent_data = [
            d for d in self.historical_data
            if (datetime.utcnow() - d['timestamp']).days <= days
        ]
        
        if not recent_data:
            return {
                'trend': 'stable',
                'average_stress': 0,
                'max_stress': 0,
                'min_stress': 0,
                'change': 0
            }
        
        stress_values = [d['stress'] for d in recent_data if d['stress']]
        
        if not stress_values:
            return {
                'trend': 'stable',
                'average_stress': 0,
                'max_stress': 0,
                'min_stress': 0,
                'change': 0
            }
        
        average_stress = statistics.mean(stress_values)
        max_stress = max(stress_values)
        min_stress = min(stress_values)
        
        # Calculate trend
        if len(stress_values) > 1:
            change = stress_values[-1] - stress_values[0]
            if change > 0.5:
                trend = 'increasing'
            elif change < -0.5:
                trend = 'decreasing'
            else:
                trend = 'stable'
        else:
            trend = 'stable'
            change = 0
        
        return {
            'trend': trend,
            'average_stress': round(average_stress, 2),
            'max_stress': max_stress,
            'min_stress': min_stress,
            'change': round(change, 2),
            'data_points': len(stress_values)
        }
    
    def predict_stress(self, current_data: Dict) -> Dict[str, any]:
        """
        Predict stress level based on current data
        
        Args:
            current_data: Current mood/activity data
            
        Returns:
            Prediction with recommendations
        """
        # Base stress from input
        base_stress = current_data.get('stress_level', 5)
        
        # Adjust based on activities
        activities = current_data.get('activities', [])
        activity_adjustment = sum(
            self.ACTIVITY_IMPACT.get(activity, 0) for activity in activities
        )
        
        # Adjust based on sleep
        sleep_quality = current_data.get('sleep_quality', 3)
        sleep_adjustment = (5 - sleep_quality) * 0.2
        
        # Adjust based on energy
        energy_level = current_data.get('energy_level', 5)
        energy_adjustment = (10 - energy_level) * 0.1
        
        # Calculate predicted stress
        predicted_stress = max(1, min(10, base_stress + activity_adjustment + sleep_adjustment + energy_adjustment))
        
        # Determine stress level category
        stress_category = self._categorize_stress(predicted_stress)
        
        return {
            'predicted_stress': round(predicted_stress, 2),
            'category': stress_category,
            'base_stress': base_stress,
            'activity_adjustment': round(activity_adjustment, 2),
            'sleep_adjustment': round(sleep_adjustment, 2),
            'energy_adjustment': round(energy_adjustment, 2),
            'recommendations': self._get_recommendations(predicted_stress, current_data)
        }
    
    def _categorize_stress(self, stress_level: float) -> str:
        """Categorize stress level"""
        for category, (min_val, max_val) in self.STRESS_LEVELS.items():
            if min_val <= stress_level <= max_val:
                return category
        return 'critical'
    
    def _get_recommendations(self, stress_level: float, data: Dict) -> List[str]:
        """Get stress management recommendations"""
        recommendations = []
        
        if stress_level > 7:
            recommendations.append('🚨 Your stress level is high. Consider immediate stress relief activities.')
            recommendations.append('💬 Try talking to someone you trust about what\'s bothering you.')
        
        if data.get('sleep_quality', 3) < 3:
            recommendations.append('😴 Improve sleep quality: maintain consistent sleep schedule.')
            recommendations.append('📱 Avoid screens 1 hour before bedtime.')
        
        if data.get('energy_level', 5) < 3:
            recommendations.append('🏃 Low energy detected. Try light exercise or yoga.')
            recommendations.append('🥗 Make sure you\'re eating balanced meals.')
        
        if stress_level > 5:
            recommendations.append('🧘 Practice 10 minutes of meditation or deep breathing.')
            recommendations.append('🚶 Take a 15-minute walk in nature.')
            recommendations.append('🎵 Listen to calming music.')
        
        if not recommendations:
            recommendations.append('✨ Keep up the good work! You\'re managing stress well.')
            recommendations.append('💪 Continue with activities that make you feel good.')
        
        return recommendations
    
    def get_stress_patterns(self) -> Dict:
        """
        Identify stress patterns
        
        Returns:
            Dictionary with stress patterns and insights
        """
        if not self.historical_data:
            return {'patterns': []}
        
        # Find patterns
        patterns = []
        
        # Morning vs evening stress
        morning_stress = [
            d['stress'] for d in self.historical_data
            if d['timestamp'].hour < 12 and d['stress']
        ]
        evening_stress = [
            d['stress'] for d in self.historical_data
            if d['timestamp'].hour >= 12 and d['stress']
        ]
        
        if morning_stress and evening_stress:
            morning_avg = statistics.mean(morning_stress)
            evening_avg = statistics.mean(evening_stress)
            
            if morning_avg > evening_avg:
                patterns.append('High stress levels in the morning')
            elif evening_avg > morning_avg:
                patterns.append('High stress levels in the evening')
        
        return {
            'patterns': patterns,
            'total_entries': len(self.historical_data),
            'morning_stress_avg': round(statistics.mean(morning_stress), 2) if morning_stress else 0,
            'evening_stress_avg': round(statistics.mean(evening_stress), 2) if evening_stress else 0
        }


# Initialize stress predictor
stress_predictor = StressPredictor()


def predict_stress(mood_data: Dict) -> Dict:
    """
    Predict stress level
    
    Args:
        mood_data: Mood and activity data
        
    Returns:
        Stress prediction results
    """
    return stress_predictor.predict_stress(mood_data)


def get_stress_trend(days: int = 7) -> Dict:
    """
    Get stress trend analysis
    
    Args:
        days: Number of days to analyze
        
    Returns:
        Stress trend information
    """
    return stress_predictor.calculate_stress_trend(days)
