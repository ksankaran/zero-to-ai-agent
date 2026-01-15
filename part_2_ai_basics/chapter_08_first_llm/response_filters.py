# From: Zero to AI Agent, Chapter 8, Section 8.5
# File: response_filters.py

"""Filter and modify chatbot responses"""

class ResponseFilter:
    """Modify responses before showing to user"""
    
    @staticmethod
    def make_brief(response, max_length=100):
        """Shorten long responses"""
        if len(response) <= max_length:
            return response
        return response[:max_length-3] + "..."
    
    @staticmethod
    def add_emoji(response):
        """Add relevant emoji to responses"""
        emoji_map = {
            'happy': '😊', 'sad': '😔', 'hello': '👋',
            'yes': '✅', 'no': '❌', 'think': '🤔',
            'love': '❤️', 'great': '🎉', 'sorry': '😅'
        }
        
        response_lower = response.lower()
        for word, emoji in emoji_map.items():
            if word in response_lower:
                return f"{emoji} {response}"
        return response
    
    @staticmethod
    def make_uppercase(response):
        """MAKE RESPONSE LOUDER!"""
        return response.upper()
