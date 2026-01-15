# From: Zero to AI Agent, Chapter 11 Challenge Project
# File: challenge_project_starter.py
# Smart Study Assistant - Starter Code

"""
Chapter 11 Challenge Project: Smart Study Assistant

This starter code provides the structure for your study assistant.
Your job is to implement all the methods and add the features!

Requirements to implement:
1. Multi-provider support (GPT-3.5, GPT-4, local models)
2. Smart conversation modes (Teacher, Quiz, Summary, Discussion)
3. Memory management (persistent between sessions)
4. Structured output (parsed study materials)
5. Production quality (error handling, monitoring, debugging)
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import PydanticOutputParser
from langchain_classic.memory import ConversationBufferMemory
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from dotenv import load_dotenv
import json
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# ============================================================================
# DATA MODELS - Define structured outputs
# ============================================================================

class KeyPoint(BaseModel):
    """Model for a key learning point"""
    concept: str = Field(description="The main concept or term")
    explanation: str = Field(description="Clear explanation of the concept")
    example: Optional[str] = Field(description="An example if relevant")

class StudyNotes(BaseModel):
    """Model for structured study notes"""
    topic: str = Field(description="The main topic")
    key_points: List[KeyPoint] = Field(description="Key learning points")
    summary: str = Field(description="Brief summary of the topic")

class QuizQuestion(BaseModel):
    """Model for quiz questions"""
    question: str = Field(description="The question")
    answer: str = Field(description="The correct answer")
    difficulty: str = Field(description="easy, medium, or hard")

# ============================================================================
# SMART STUDY ASSISTANT CLASS
# ============================================================================

class SmartStudyAssistant:
    """Your intelligent study assistant that helps you learn effectively"""
    
    def __init__(self):
        """Initialize the study assistant with all components"""
        
        # TODO: Initialize models (GPT-3.5, GPT-4, and fallback)
        self.models = {
            'simple': None,  # TODO: Initialize GPT-3.5
            'complex': None,  # TODO: Initialize GPT-4
            'private': None  # TODO: Initialize local model (optional)
        }
        
        # TODO: Initialize memory system
        self.memory = None  # TODO: Setup ConversationBufferMemory
        
        # TODO: Initialize conversation modes with different prompts
        self.mode_prompts = {
            'teacher': None,  # TODO: Create teacher mode prompt
            'quiz': None,     # TODO: Create quiz mode prompt
            'summary': None,  # TODO: Create summary mode prompt
            'discussion': None # TODO: Create discussion mode prompt
        }
        
        # TODO: Initialize output parsers
        self.parsers = {
            'notes': None,    # TODO: PydanticOutputParser for StudyNotes
            'quiz': None      # TODO: PydanticOutputParser for QuizQuestion
        }
        
        # Current state
        self.current_mode = 'teacher'
        self.current_topic = None
        self.session_data = {
            'topics_covered': [],
            'total_messages': 0,
            'session_start': datetime.now().isoformat(),
            'cost_tracking': {'gpt-3.5': 0, 'gpt-4': 0}
        }
        
        # Debug mode
        self.debug_mode = False
        
        print("🎓 Smart Study Assistant Initialized!")
        print("Commands: /mode, /topic, /save, /load, /stats, /help, /quit")
        print("-" * 60)
    
    # ========================================================================
    # CORE METHODS TO IMPLEMENT
    # ========================================================================
    
    def classify_complexity(self, user_input: str) -> str:
        """
        Classify if the input requires simple or complex model
        
        TODO: Implement logic to determine complexity
        - Simple questions → 'simple'
        - Complex topics → 'complex'  
        - Private data → 'private'
        """
        # TODO: Implement complexity classification
        return 'simple'  # Default for now
    
    def select_model(self, complexity: str):
        """
        Select the appropriate model based on complexity
        
        TODO: Return the right model from self.models
        TODO: Add fallback logic if primary model fails
        """
        # TODO: Implement model selection with fallback
        pass
    
    def create_mode_prompts(self):
        """
        Create specialized prompts for each learning mode
        
        TODO: Create ChatPromptTemplate for each mode:
        - Teacher: Patient explanations with examples
        - Quiz: Generate questions to test knowledge
        - Summary: Create concise study notes
        - Discussion: Socratic dialogue
        """
        # TODO: Implement all mode prompts
        pass
    
    def process_message(self, user_input: str) -> str:
        """
        Process user message and generate response
        
        TODO: Main processing logic:
        1. Classify complexity
        2. Select appropriate model
        3. Use current mode's prompt
        4. Include memory context
        5. Parse output if structured
        6. Handle errors gracefully
        """
        try:
            # TODO: Implement complete message processing
            
            # Update session data
            self.session_data['total_messages'] += 1
            
            # Placeholder response
            return "TODO: Implement message processing"
            
        except Exception as e:
            if self.debug_mode:
                print(f"Debug: Error in process_message: {e}")
            return "I encountered an error. Let me try a different approach..."
    
    def save_session(self, filename: str = None):
        """
        Save current session to file
        
        TODO: Save:
        - Conversation memory
        - Session data
        - Current topic and mode
        """
        if not filename:
            filename = f"study_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # TODO: Implement session saving
        print(f"Session saved to {filename}")
    
    def load_session(self, filename: str):
        """
        Load a previous session
        
        TODO: Load:
        - Conversation memory
        - Session data
        - Topic and mode
        """
        # TODO: Implement session loading
        print(f"Session loaded from {filename}")
    
    def generate_study_notes(self, topic: str) -> StudyNotes:
        """
        Generate structured study notes for a topic
        
        TODO: Use the notes parser to create structured output
        """
        # TODO: Implement study notes generation
        pass
    
    def generate_quiz(self, topic: str, difficulty: str = 'medium') -> List[QuizQuestion]:
        """
        Generate quiz questions on a topic
        
        TODO: Create quiz questions with the quiz parser
        """
        # TODO: Implement quiz generation
        pass
    
    def show_statistics(self):
        """Show session statistics"""
        print("\n📊 Session Statistics:")
        print(f"Topics covered: {', '.join(self.session_data['topics_covered'])}")
        print(f"Total messages: {self.session_data['total_messages']}")
        print(f"Session duration: {datetime.now() - datetime.fromisoformat(self.session_data['session_start'])}")
        
        # Cost estimation
        total_cost = sum(self.session_data['cost_tracking'].values())
        print(f"Estimated cost: ${total_cost:.4f}")
        
        for model, cost in self.session_data['cost_tracking'].items():
            if cost > 0:
                print(f"  {model}: ${cost:.4f}")
    
    def show_help(self):
        """Show available commands"""
        help_text = """
        📚 Available Commands:
        
        /mode [teacher|quiz|summary|discussion] - Change learning mode
        /topic [topic_name] - Set current study topic
        /save [filename] - Save current session
        /load [filename] - Load previous session
        /notes - Generate study notes for current topic
        /quiz [easy|medium|hard] - Generate quiz questions
        /stats - Show session statistics
        /debug - Toggle debug mode
        /help - Show this help message
        /quit - Exit the assistant
        
        Just type normally to have a conversation in the current mode!
        """
        print(help_text)
    
    # ========================================================================
    # MAIN INTERACTION LOOP
    # ========================================================================
    
    def run(self):
        """Main interaction loop"""
        print("🎓 Welcome to your Smart Study Assistant!")
        print("What would you like to learn about today?")
        print("(Type /help for commands)")
        print("-" * 60)
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                # Handle commands
                if user_input.startswith('/'):
                    if user_input == '/quit':
                        print("👋 Thanks for studying! Goodbye!")
                        break
                    
                    elif user_input.startswith('/mode'):
                        # TODO: Implement mode switching
                        parts = user_input.split()
                        if len(parts) > 1:
                            new_mode = parts[1]
                            if new_mode in self.mode_prompts:
                                self.current_mode = new_mode
                                print(f"✅ Switched to {new_mode} mode")
                            else:
                                print("❌ Invalid mode. Choose: teacher, quiz, summary, discussion")
                    
                    elif user_input.startswith('/topic'):
                        # TODO: Implement topic setting
                        parts = user_input.split(maxsplit=1)
                        if len(parts) > 1:
                            self.current_topic = parts[1]
                            self.session_data['topics_covered'].append(self.current_topic)
                            print(f"✅ Studying: {self.current_topic}")
                    
                    elif user_input == '/stats':
                        self.show_statistics()
                    
                    elif user_input == '/help':
                        self.show_help()
                    
                    elif user_input == '/debug':
                        self.debug_mode = not self.debug_mode
                        print(f"Debug mode: {'ON' if self.debug_mode else 'OFF'}")
                    
                    elif user_input.startswith('/save'):
                        # TODO: Implement save command
                        parts = user_input.split(maxsplit=1)
                        filename = parts[1] if len(parts) > 1 else None
                        self.save_session(filename)
                    
                    elif user_input.startswith('/load'):
                        # TODO: Implement load command
                        parts = user_input.split(maxsplit=1)
                        if len(parts) > 1:
                            self.load_session(parts[1])
                    
                    elif user_input == '/notes':
                        # TODO: Generate study notes
                        if self.current_topic:
                            print(f"📝 Generating notes for: {self.current_topic}")
                            # notes = self.generate_study_notes(self.current_topic)
                            print("TODO: Implement notes generation")
                        else:
                            print("❌ Please set a topic first with /topic")
                    
                    elif user_input.startswith('/quiz'):
                        # TODO: Generate quiz
                        if self.current_topic:
                            parts = user_input.split()
                            difficulty = parts[1] if len(parts) > 1 else 'medium'
                            print(f"📝 Generating {difficulty} quiz for: {self.current_topic}")
                            # questions = self.generate_quiz(self.current_topic, difficulty)
                            print("TODO: Implement quiz generation")
                        else:
                            print("❌ Please set a topic first with /topic")
                    
                    else:
                        print("❌ Unknown command. Type /help for available commands")
                
                else:
                    # Regular conversation
                    response = self.process_message(user_input)
                    print(f"\n🤖 Assistant ({self.current_mode} mode): {response}")
            
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                if self.debug_mode:
                    import traceback
                    traceback.print_exc()

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Create and run the assistant
    assistant = SmartStudyAssistant()
    
    # TODO: Initialize all components properly
    # assistant.create_mode_prompts()
    # assistant.setup_memory()
    # assistant.setup_parsers()
    
    # Run the main loop
    assistant.run()