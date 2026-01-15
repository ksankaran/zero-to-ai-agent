# From: Zero to AI Agent, Chapter 8, Section 8.5
# File: exercise_3_8_5_solution.py

"""Detect and respond to user mood"""

class MoodDetector:
    """Analyze user sentiment and mood"""
    
    def __init__(self):
        self.mood_keywords = {
            'happy': {
                'words': ['happy', 'great', 'awesome', 'wonderful', 'love', 'excited'],
                'emojis': ['😊', '😄', '🎉', '❤️'],
                'response_style': "enthusiastic and cheerful"
            },
            'sad': {
                'words': ['sad', 'depressed', 'unhappy', 'crying', 'terrible'],
                'emojis': ['😢', '😔', '😭'],
                'response_style': "gentle and supportive"
            },
            'angry': {
                'words': ['angry', 'mad', 'frustrated', 'annoyed', 'hate'],
                'emojis': ['😡', '😠', '🤬'],
                'response_style': "calm and understanding"
            },
            'confused': {
                'words': ['confused', "don't understand", 'unclear', 'lost'],
                'emojis': ['😕', '🤔', '❓'],
                'response_style': "clear and patient"
            },
            'neutral': {
                'words': [],
                'emojis': [],
                'response_style': "balanced and helpful"
            }
        }
        self.current_mood = 'neutral'
        self.mood_history = []
    
    def detect_mood(self, message):
        """Detect mood from message"""
        message_lower = message.lower()
        mood_scores = {}
        
        for mood, indicators in self.mood_keywords.items():
            score = 0
            # Check words
            for word in indicators['words']:
                if word in message_lower:
                    score += 2
            # Check emojis
            for emoji in indicators['emojis']:
                if emoji in message:
                    score += 3
            
            if score > 0:
                mood_scores[mood] = score
        
        # Determine mood
        if mood_scores:
            self.current_mood = max(mood_scores, key=mood_scores.get)
        else:
            self.current_mood = 'neutral'
        
        self.mood_history.append(self.current_mood)
        return self.current_mood
    
    def get_response_style(self):
        """Get appropriate response style for current mood"""
        return self.mood_keywords[self.current_mood]['response_style']
    
    def get_adjusted_prompt(self, base_prompt):
        """Adjust system prompt based on mood"""
        style = self.get_response_style()
        return f"{base_prompt} Be {style} in your response."
