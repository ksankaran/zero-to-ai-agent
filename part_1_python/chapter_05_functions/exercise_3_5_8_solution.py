# From: Zero to AI Agent, Chapter 5, Section 5.8
# Exercise 3: Simple Chatbot Class

class Chatbot:
    """A simple chatbot with keyword-based responses and mood"""

    def __init__(self, name):
        self.name = name
        self.mood = "neutral"  # can be: happy, neutral, sad
        self.response_count = 0

        # Dictionary of keyword responses
        self.responses = {
            "hello": "Hi there! Nice to meet you!",
            "hi": "Hello! How can I help you today?",
            "how are you": "I'm doing great, thanks for asking!",
            "bye": "Goodbye! Have a wonderful day!",
            "thanks": "You're welcome! Happy to help!",
            "help": "I can chat with you! Try saying hello or asking how I am.",
            "joke": "Why do programmers prefer dark mode? Because light attracts bugs!",
            "python": "Python is amazing! It's my favorite programming language!",
            "sad": "I'm sorry to hear that. Things will get better!",
            "happy": "That's wonderful! Your happiness makes me happy too!",
        }

    def respond(self, message):
        """Generate a response based on the user's message"""
        self.response_count += 1
        message_lower = message.lower()

        # Check for keywords and update mood
        if "sad" in message_lower or "bad" in message_lower:
            self.mood = "sad"
        elif "happy" in message_lower or "great" in message_lower or "good" in message_lower:
            self.mood = "happy"

        # Look for keyword matches
        for keyword, response in self.responses.items():
            if keyword in message_lower:
                return self._format_response(response)

        # Default responses based on mood
        if self.mood == "happy":
            return self._format_response("I'm glad we're having a nice chat!")
        elif self.mood == "sad":
            return self._format_response("I'm here if you want to talk.")
        else:
            return self._format_response("Interesting! Tell me more about that.")

    def _format_response(self, response):
        """Format the response with the bot's name"""
        return f"{self.name}: {response}"

    def get_mood(self):
        """Return the chatbot's current mood"""
        return self.mood

    def get_stats(self):
        """Display chatbot statistics"""
        print(f"\n--- {self.name}'s Stats ---")
        print(f"Responses given: {self.response_count}")
        print(f"Current mood: {self.mood}")
        print("-" * 25)


# Interactive chatbot
print("=" * 40)
print("SIMPLE CHATBOT")
print("=" * 40)

bot = Chatbot("PyBot")
print(f"Chat with {bot.name}! Type 'quit' to exit.\n")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "quit":
        print(bot.respond("bye"))
        bot.get_stats()
        break

    if user_input:
        response = bot.respond(user_input)
        print(response)
