# From: Zero to AI Agent, Chapter 11, Section 11.4
# File: exercise_3_11_4_solution.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.memory import ConversationBufferMemory
from dotenv import load_dotenv
from collections import Counter

load_dotenv()

class WritingWorkshop:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.7)
        self.memory = ConversationBufferMemory(return_messages=True)
        
        # Track writing goals and common issues
        self.writing_goals = []
        self.common_issues = Counter()
        self.improvement_history = []
        
        # Improvement style prompts
        self.improvement_styles = {
            "clarity": ChatPromptTemplate.from_template(
                """Improve this text for clarity. Make it easier to understand.
                Remove ambiguity and simplify complex sentences.
                
                Text: {text}
                
                Improved version:"""
            ),
            "creativity": ChatPromptTemplate.from_template(
                """Make this text more creative and engaging.
                Add vivid descriptions and interesting language.
                
                Text: {text}
                
                Creative version:"""
            ),
            "conciseness": ChatPromptTemplate.from_template(
                """Make this text more concise. Remove unnecessary words.
                Keep the meaning but make it shorter and punchier.
                
                Text: {text}
                
                Concise version:"""
            ),
            "professional": ChatPromptTemplate.from_template(
                """Make this text more professional and formal.
                Use appropriate business language and tone.
                
                Text: {text}
                
                Professional version:"""
            )
        }
        
        # Analysis prompt
        self.analysis_prompt = ChatPromptTemplate.from_template(
            """Analyze this text and identify the top 3 issues that need improvement.
            Be specific and constructive.
            
            Text: {text}
            
            Issues:"""
        )
        
        # Goal-aware feedback prompt
        self.feedback_prompt = ChatPromptTemplate.from_template(
            """The writer's goals are: {goals}
            
            Review this text and provide feedback focused on these goals:
            {text}
            
            Feedback:"""
        )
    
    def set_goals(self, goals):
        """Set writing goals"""
        if isinstance(goals, str):
            goals = [goals]
        self.writing_goals = goals
        return f"Goals set: {', '.join(goals)}"
    
    def improve(self, text, style="clarity"):
        """Improve text in specified style"""
        if style not in self.improvement_styles:
            return f"Unknown style. Choose: {', '.join(self.improvement_styles.keys())}"
        
        prompt = self.improvement_styles[style]
        chain = prompt | self.llm
        response = chain.invoke({"text": text})
        
        # Track improvement
        self.improvement_history.append({
            "original": text[:100],
            "style": style,
            "improved": response.content[:100]
        })
        
        # Save to memory
        self.memory.save_context(
            {"input": f"Improve ({style}): {text}"},
            {"output": response.content}
        )
        
        return response.content
    
    def analyze(self, text):
        """Analyze text for issues"""
        chain = self.analysis_prompt | self.llm
        response = chain.invoke({"text": text})
        
        # Extract and track issues
        issues = response.content
        
        # Simple issue extraction (look for numbered items)
        import re
        found_issues = re.findall(r'\d+\.\s+([^.]+)', issues)
        for issue in found_issues:
            # Track common issues
            key_words = ["clarity", "grammar", "structure", "flow", "word choice", 
                        "repetition", "passive voice", "complexity"]
            for word in key_words:
                if word.lower() in issue.lower():
                    self.common_issues[word] += 1
        
        return issues
    
    def get_feedback(self, text):
        """Get goal-focused feedback"""
        if not self.writing_goals:
            return "Set your writing goals first for personalized feedback!"
        
        chain = self.feedback_prompt | self.llm
        response = chain.invoke({
            "goals": ", ".join(self.writing_goals),
            "text": text
        })
        
        return response.content
    
    def show_patterns(self):
        """Show common issues and improvement patterns"""
        if not self.common_issues:
            return "No patterns identified yet. Analyze more text!"
        
        patterns = {
            "common_issues": dict(self.common_issues.most_common(5)),
            "improvement_styles_used": Counter(h["style"] for h in self.improvement_history),
            "total_improvements": len(self.improvement_history)
        }
        
        return patterns
    
    def suggest_focus(self):
        """Suggest what to focus on based on patterns"""
        if not self.common_issues:
            return "Analyze some text first to get suggestions!"
        
        top_issue = self.common_issues.most_common(1)[0][0]
        
        suggestions = {
            "clarity": "Focus on simplifying sentences and removing ambiguity.",
            "grammar": "Review grammar rules and use grammar checking tools.",
            "structure": "Work on paragraph organization and logical flow.",
            "flow": "Practice transitions between ideas and sentences.",
            "repetition": "Expand your vocabulary and vary sentence structures.",
            "passive voice": "Practice converting passive to active voice.",
            "complexity": "Break down complex ideas into simpler components."
        }
        
        return f"Based on your writing, focus on: {top_issue}. {suggestions.get(top_issue, 'Keep practicing!')}"

# Test the writing workshop
def demo_writing_workshop():
    workshop = WritingWorkshop()
    
    # Set goals
    print(workshop.set_goals(["clarity", "conciseness", "professional tone"]))
    
    # Sample text
    sample = """
    The thing is that we need to basically consider thinking about maybe 
    implementing a new system that could potentially help us with the process 
    of managing our workflow in a way that might be more efficient.
    """
    
    print("\nOriginal text:", sample)
    print("\n" + "="*60)
    
    # Analyze
    print("\n📊 ANALYSIS:")
    print(workshop.analyze(sample))
    
    # Improve in different styles
    print("\n✨ IMPROVEMENTS:")
    for style in ["clarity", "conciseness", "professional"]:
        print(f"\n{style.upper()}:")
        print(workshop.improve(sample, style))
    
    # Get feedback based on goals
    print("\n💬 GOAL-BASED FEEDBACK:")
    print(workshop.get_feedback(sample))
    
    # Show patterns
    print("\n📈 PATTERNS:")
    print(workshop.show_patterns())
    
    # Get suggestions
    print("\n💡 SUGGESTION:")
    print(workshop.suggest_focus())

if __name__ == "__main__":
    demo_writing_workshop()
