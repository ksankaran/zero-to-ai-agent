# From: Zero to AI Agent, Chapter 7, Section 7.1  
# File: narrow_ai_example.py

"""
Demonstrates Narrow AI - systems that excel at specific tasks
but can't generalize to other domains.
"""

class ChessAI:
    """
    Example of Narrow AI - Amazing at chess, useless at everything else.
    This illustrates how current AI systems are specialized tools,
    not general-purpose intelligence.
    """
    
    def __init__(self):
        self.name = "DeepChess"
        self.specialty = "Chess"
    
    def find_best_move(self, board):
        """
        In a real chess AI, this would analyze millions of positions.
        Can beat world champions at chess!
        """
        # Simplified for demonstration
        # Real chess AI would use minimax, alpha-beta pruning, 
        # neural networks, etc.
        return "e2-e4"  # Classic opening move
    
    def write_poetry(self):
        """
        This chess AI can't write poetry - it only knows chess.
        This is the limitation of narrow AI.
        """
        return "Error: I only know chess. Poetry is outside my domain."
    
    def translate_language(self, text):
        """Another task this narrow AI can't do."""
        return "Error: I only know chess. Translation is outside my domain."
    
    def diagnose_illness(self, symptoms):
        """Yet another task beyond this narrow AI."""
        return "Error: I only know chess. Medical diagnosis is outside my domain."
    
    def demonstrate_narrow_ai(self):
        """Shows both the strength and limitation of narrow AI."""
        print(f"Hi, I'm {self.name}, a Narrow AI specialized in {self.specialty}")
        print("\nWhat I CAN do:")
        print(f"✓ Chess move: {self.find_best_move('starting_position')}")
        print("✓ Analyze millions of chess positions per second")
        print("✓ Beat world chess champions")
        
        print("\nWhat I CAN'T do:")
        print(f"✗ Write poetry: {self.write_poetry()}")
        print(f"✗ Translate: {self.translate_language('Hello')}")
        print(f"✗ Medical diagnosis: {self.diagnose_illness('headache')}")
        
        print("\nThis is Narrow AI: Superhuman at one thing, helpless at everything else!")


# Example of how different narrow AIs specialize
class TranslationAI:
    """Another narrow AI, but for translation."""
    
    def translate(self, text, target_language):
        # Simplified - real translation AI uses complex neural networks
        translations = {
            'Hello': {'spanish': 'Hola', 'french': 'Bonjour'},
            'Thank you': {'spanish': 'Gracias', 'french': 'Merci'}
        }
        return translations.get(text, {}).get(target_language, "Unknown")
    
    def play_chess(self):
        return "Error: I only know translation. Chess is outside my domain."


if __name__ == "__main__":
    # Demonstrate narrow AI limitations
    chess_ai = ChessAI()
    chess_ai.demonstrate_narrow_ai()
    
    print("\n" + "="*50)
    print("Key Concept: Every AI today is Narrow AI")
    print("="*50)
    print("• Excel at specific tasks")
    print("• Can't generalize to other domains")
    print("• Multiple narrow AIs needed for different tasks")
    print("• AGI (Artificial General Intelligence) doesn't exist yet")
