# From: Zero to AI Agent, Chapter 8, Section 8.5
# File: commands.py

"""Command handling for chatbots"""

class CommandHandler:
    """Handle special commands in chat"""
    
    def __init__(self):
        self.commands = {
            '/help': self.show_help,
            '/stats': self.show_stats,
            '/clear': self.clear_chat
        }
        self.bot = None  # Set by chatbot
    
    def set_bot(self, bot):
        """Connect to a chatbot instance"""
        self.bot = bot
    
    def handle(self, input_text):
        """Check if input is a command and handle it"""
        if not input_text.startswith('/'):
            return None
        
        command = input_text.split()[0]
        return self.commands.get(command, self.unknown_command)()
    
    def show_help(self):
        """Show available commands"""
        return """Available commands:
  /help  - Show this help
  /stats - Show conversation stats
  /clear - Clear conversation"""
    
    def show_stats(self):
        """Show conversation statistics"""
        if self.bot and hasattr(self.bot, 'get_stats'):
            stats = self.bot.get_stats()
            return f"Messages: {stats['total_messages']}, Context: {stats['context_size']}"
        return "Stats not available"
    
    def clear_chat(self):
        """Clear conversation"""
        if self.bot and hasattr(self.bot, 'messages'):
            self.bot.messages = self.bot.messages[:1]
            return "Conversation cleared!"
        return "Cannot clear"
    
    def unknown_command(self):
        """Handle unknown commands"""
        return "Unknown command. Type /help for available commands."
