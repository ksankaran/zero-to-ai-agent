# From: Zero to AI Agent, Chapter 11, Section 11.4
# File: exercise_2_11_4_solution.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.memory import ConversationBufferMemory
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

class LearningTracker:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.7)
        self.memory = ConversationBufferMemory(return_messages=True)
        
        # Track learning progress
        self.topics_learned = {}
        self.quiz_scores = {}
        self.total_sessions = 0
        
        # Prompts for different functions
        self.learn_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an encouraging teacher. Explain topics clearly."),
            MessagesPlaceholder(variable_name="history"),
            ("human", "Teach me about: {topic}")
        ])
        
        self.quiz_prompt = ChatPromptTemplate.from_template(
            """Create a quiz question about {topic}.
            Include the question and 4 multiple choice options (A, B, C, D).
            Mark the correct answer clearly."""
        )
        
        self.encourage_prompt = ChatPromptTemplate.from_template(
            """The student has completed {sessions} learning sessions and studied these topics: {topics}.
            Their average quiz score is {score}%.
            Give them personalized encouragement and suggest what to study next."""
        )
    
    def learn_topic(self, topic):
        """Learn about a new topic"""
        self.total_sessions += 1
        
        # Record topic
        if topic not in self.topics_learned:
            self.topics_learned[topic] = {
                "first_studied": datetime.now().isoformat(),
                "times_reviewed": 0,
                "quiz_attempts": 0
            }
        
        self.topics_learned[topic]["times_reviewed"] += 1
        
        # Get explanation
        history = self.memory.load_memory_variables({})["history"]
        chain = self.learn_prompt | self.llm
        
        response = chain.invoke({
            "history": history,
            "topic": topic
        })
        
        # Save to memory
        self.memory.save_context(
            {"input": f"Teach me about: {topic}"},
            {"output": response.content}
        )
        
        return response.content
    
    def quiz_me(self, topic=None):
        """Generate a quiz question"""
        if not topic and self.topics_learned:
            # Pick a random learned topic
            import random
            topic = random.choice(list(self.topics_learned.keys()))
        elif not topic:
            return "No topics learned yet! Learn something first."
        
        chain = self.quiz_prompt | self.llm
        response = chain.invoke({"topic": topic})
        
        # Track quiz attempt
        if topic in self.topics_learned:
            self.topics_learned[topic]["quiz_attempts"] += 1
        
        return {
            "topic": topic,
            "question": response.content
        }
    
    def record_score(self, topic, score):
        """Record quiz score"""
        if topic not in self.quiz_scores:
            self.quiz_scores[topic] = []
        self.quiz_scores[topic].append(score)
        return f"Score recorded: {score}% for {topic}"
    
    def get_progress(self):
        """Get learning progress and encouragement"""
        if not self.topics_learned:
            return "Start learning to track your progress!"
        
        # Calculate average score
        all_scores = []
        for scores in self.quiz_scores.values():
            all_scores.extend(scores)
        
        avg_score = sum(all_scores) / len(all_scores) if all_scores else 0
        
        # Get encouragement
        chain = self.encourage_prompt | self.llm
        response = chain.invoke({
            "sessions": self.total_sessions,
            "topics": ", ".join(self.topics_learned.keys()),
            "score": round(avg_score)
        })
        
        return {
            "sessions": self.total_sessions,
            "topics_learned": list(self.topics_learned.keys()),
            "average_score": avg_score,
            "encouragement": response.content
        }
    
    def review_topic(self, topic):
        """Review a previously learned topic"""
        if topic not in self.topics_learned:
            return f"You haven't learned about {topic} yet!"
        
        history = self.memory.load_memory_variables({})["history"]
        
        review_prompt = ChatPromptTemplate.from_messages([
            ("system", "Help the student review this topic they learned before."),
            MessagesPlaceholder(variable_name="history"),
            ("human", f"Help me review: {topic}")
        ])
        
        chain = review_prompt | self.llm
        response = chain.invoke({"history": history})
        
        self.topics_learned[topic]["times_reviewed"] += 1
        
        return response.content

# Interactive learning session
def run_learning_session():
    tracker = LearningTracker()
    
    print("📚 Learning Tracker Assistant")
    print("Commands: learn <topic>, quiz [topic], score <topic> <score>, progress, review <topic>, quit")
    print("="*60)
    
    while True:
        command = input("\nWhat would you like to do? ").strip().lower()
        
        if command.startswith("learn "):
            topic = command[6:]
            print(f"\n📖 Learning about {topic}...")
            print(tracker.learn_topic(topic))
            
        elif command.startswith("quiz"):
            parts = command.split(maxsplit=1)
            topic = parts[1] if len(parts) > 1 else None
            quiz = tracker.quiz_me(topic)
            print(f"\n❓ Quiz on {quiz['topic']}:")
            print(quiz['question'])
            
        elif command.startswith("score "):
            parts = command.split()
            if len(parts) >= 3:
                topic = parts[1]
                score = int(parts[2])
                print(tracker.record_score(topic, score))
            
        elif command == "progress":
            progress = tracker.get_progress()
            print(f"\n📊 Your Progress:")
            print(f"Sessions: {progress['sessions']}")
            print(f"Topics: {', '.join(progress['topics_learned'])}")
            print(f"Average Score: {progress['average_score']:.1f}%")
            print(f"\n💪 {progress['encouragement']}")
            
        elif command.startswith("review "):
            topic = command[7:]
            print(f"\n🔄 Reviewing {topic}...")
            print(tracker.review_topic(topic))
            
        elif command == "quit":
            print("\n👋 Keep learning! You're doing great!")
            break
        
        else:
            print("Unknown command. Try: learn, quiz, score, progress, review, or quit")

if __name__ == "__main__":
    run_learning_session()
