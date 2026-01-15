# From: Zero to AI Agent, Chapter 10, Challenge Project
# File: agent_challenge_starter.py

"""
Chapter 10 Challenge: Personal Research Assistant

Build an agent that demonstrates the key differences between chatbots and agents.
This is a conceptual implementation - we'll build real agents with LangChain in Chapter 11!
"""

import time
from typing import List, Dict, Optional
from datetime import datetime


class ResearchAgent:
    """
    A simple research agent that demonstrates core agent concepts.
    This is a simulation - real implementation comes in Chapter 11.
    """
    
    def __init__(self, autonomy_level: int = 3):
        """
        Initialize the research agent.
        
        Args:
            autonomy_level: 1-5, determines how autonomous the agent is
        """
        # Memory components
        self.memory = []  # Store research findings
        self.entities = {}  # Track entities mentioned
        self.conversation_history = []
        
        # Agent state
        self.current_topic = None
        self.subtopics = []
        self.iteration_count = 0
        self.max_iterations = 10
        self.autonomy_level = autonomy_level
        
        # Cost tracking (simulated)
        self.total_tokens = 0
        self.actions_taken = []
        
        # Knowledge base (simulated data for demonstration)
        self.knowledge_base = {
            "benefits of exercise": {
                "physical health": "Regular exercise improves cardiovascular health, strengthens muscles, and boosts immunity.",
                "mental health": "Exercise releases endorphins, reduces stress, and improves mood.",
                "longevity": "Studies show regular exercise can add years to your life.",
                "cognitive function": "Physical activity enhances memory and thinking skills.",
                "sleep quality": "Regular exercise helps you fall asleep faster and deepen sleep."
            },
            "artificial intelligence": {
                "definition": "AI is the simulation of human intelligence by machines.",
                "types": "Narrow AI, General AI, and Superintelligence are the main categories.",
                "applications": "AI is used in healthcare, finance, transportation, and more.",
                "challenges": "Ethics, bias, and job displacement are major concerns.",
                "future": "AI is expected to transform every industry in the coming decades."
            }
        }
    
    def observe(self, user_input: str) -> Dict:
        """
        OBSERVE phase: Understand the current situation.
        """
        observation = {
            "timestamp": datetime.now(),
            "user_request": user_input,
            "current_knowledge": len(self.memory),
            "iterations_used": self.iteration_count,
            "remaining_iterations": self.max_iterations - self.iteration_count
        }
        
        print(f"\n🔍 OBSERVE: Processing request about '{user_input}'")
        print(f"   Current knowledge items: {observation['current_knowledge']}")
        
        return observation
    
    def think(self, observation: Dict) -> Dict:
        """
        THINK phase: Reason about what to do next.
        """
        thought_process = {
            "needs_research": len(self.memory) < 3,
            "subtopics_to_explore": [],
            "confidence_level": len(self.memory) / 5.0,  # 0 to 1
            "should_continue": self.iteration_count < self.max_iterations
        }
        
        # Identify subtopics (simulated reasoning)
        if self.current_topic in self.knowledge_base:
            thought_process["subtopics_to_explore"] = list(self.knowledge_base[self.current_topic].keys())
        
        print(f"\n💭 THINK: Need more research? {thought_process['needs_research']}")
        print(f"   Confidence level: {thought_process['confidence_level']:.1%}")
        
        # Decision based on autonomy level
        if self.autonomy_level <= 2:
            print("   [Level 2: Suggesting action to user]")
        elif self.autonomy_level == 3:
            print("   [Level 3: Will act with confirmation]")
        else:
            print("   [Level 4: Acting autonomously]")
        
        return thought_process
    
    def act(self, action_plan: Dict) -> Optional[Dict]:
        """
        ACT phase: Execute the decided action.
        """
        if not action_plan["should_continue"]:
            return None
        
        print(f"\n🎯 ACT: Researching subtopics...")
        
        # Simulate research action
        results = {}
        if self.current_topic in self.knowledge_base:
            for subtopic in action_plan["subtopics_to_explore"][:2]:  # Limit to 2 per iteration
                if subtopic in self.knowledge_base[self.current_topic]:
                    results[subtopic] = self.knowledge_base[self.current_topic][subtopic]
                    print(f"   ✓ Found information about: {subtopic}")
                    
                    # Simulate token usage
                    self.total_tokens += len(results[subtopic].split()) * 2
        
        # Track action
        self.actions_taken.append({
            "iteration": self.iteration_count,
            "action": "research",
            "results_found": len(results)
        })
        
        return results
    
    def reflect(self, action_results: Optional[Dict]) -> bool:
        """
        REFLECT phase: Evaluate progress and decide if complete.
        """
        if action_results is None:
            return True  # No results means we're done
        
        # Evaluate completeness
        total_findings = len(self.memory) + len(action_results)
        is_sufficient = total_findings >= 4
        hit_iteration_limit = self.iteration_count >= self.max_iterations - 1
        
        print(f"\n🤔 REFLECT: Evaluating progress...")
        print(f"   Total findings: {total_findings}")
        print(f"   Sufficient? {is_sufficient}")
        print(f"   At iteration limit? {hit_iteration_limit}")
        
        return is_sufficient or hit_iteration_limit
    
    def learn(self, new_information: Dict):
        """
        LEARN phase: Update memory with new information.
        """
        if new_information:
            print(f"\n📚 LEARN: Storing {len(new_information)} new findings")
            for topic, info in new_information.items():
                self.memory.append({
                    "topic": topic,
                    "information": info,
                    "timestamp": datetime.now()
                })
                
                # Extract entities (simple simulation)
                for word in topic.split():
                    if word.capitalize() == word:  # Simple entity detection
                        self.entities[word] = self.entities.get(word, 0) + 1
    
    def research_loop(self, topic: str) -> str:
        """
        Main agent loop: Observe → Think → Act → Reflect → Learn
        """
        print("\n" + "="*60)
        print(f"🚀 STARTING RESEARCH AGENT (Autonomy Level {self.autonomy_level})")
        print("="*60)
        
        self.current_topic = topic.lower()
        self.conversation_history.append({"role": "user", "content": topic})
        
        # Check for user confirmation if autonomy level requires it
        if self.autonomy_level == 3:
            response = input("\n❓ Proceed with research? (y/n): ")
            if response.lower() != 'y':
                return "Research cancelled by user."
        
        while self.iteration_count < self.max_iterations:
            print(f"\n{'='*40}")
            print(f"🔄 ITERATION {self.iteration_count + 1}/{self.max_iterations}")
            print('='*40)
            
            # OBSERVE
            observation = self.observe(topic)
            
            # THINK
            thought = self.think(observation)
            
            # ACT
            results = self.act(thought)
            
            # REFLECT
            is_complete = self.reflect(results)
            
            # LEARN
            if results:
                self.learn(results)
            
            self.iteration_count += 1
            
            # Check if we should stop
            if is_complete:
                print("\n✅ Research complete!")
                break
            
            # Simulate processing time
            time.sleep(0.5)
        
        # Compile and return report
        return self.compile_report()
    
    def compile_report(self) -> str:
        """
        Compile all research findings into a comprehensive report.
        """
        print("\n" + "="*60)
        print("📝 COMPILING RESEARCH REPORT")
        print("="*60)
        
        report = f"\n📊 Research Report: {self.current_topic.title()}\n"
        report += "="*50 + "\n\n"
        
        # Summary section
        report += "📋 SUMMARY:\n"
        report += f"• Total iterations: {self.iteration_count}\n"
        report += f"• Information items found: {len(self.memory)}\n"
        report += f"• Entities identified: {len(self.entities)}\n"
        report += f"• Simulated token usage: {self.total_tokens}\n"
        report += f"• Estimated cost: ${self.total_tokens * 0.00002:.4f}\n\n"
        
        # Findings section
        report += "🔍 FINDINGS:\n"
        for i, finding in enumerate(self.memory, 1):
            report += f"\n{i}. {finding['topic'].title()}:\n"
            report += f"   {finding['information']}\n"
        
        # Entities section
        if self.entities:
            report += "\n🏷️ KEY ENTITIES:\n"
            for entity, count in sorted(self.entities.items(), key=lambda x: x[1], reverse=True):
                report += f"   • {entity}: mentioned {count} times\n"
        
        # Agent behavior analysis
        report += "\n🤖 AGENT BEHAVIOR ANALYSIS:\n"
        report += f"• Autonomy level: {self.autonomy_level}\n"
        report += f"• Actions taken: {len(self.actions_taken)}\n"
        report += f"• Average findings per iteration: {len(self.memory)/max(self.iteration_count, 1):.1f}\n"
        
        # Demonstration of agent vs chatbot
        report += "\n💡 AGENT vs CHATBOT DEMONSTRATION:\n"
        report += "• Chatbot would: Simply provide a pre-trained response\n"
        report += "• This agent did: Iteratively researched, tracked progress, and compiled findings\n"
        report += "• Key difference: Agent maintained state, used memory, and pursued goal to completion\n"
        
        return report
    
    def demonstrate_challenges(self):
        """
        Demonstrate common agent challenges from Chapter 10.7
        """
        print("\n⚠️ DEMONSTRATING COMMON CHALLENGES:")
        
        # Challenge 1: Infinite Loop Prevention
        print("\n1. Infinite Loop Prevention:")
        print(f"   Max iterations set to: {self.max_iterations}")
        print(f"   Current iteration: {self.iteration_count}")
        print("   ✓ Loop will terminate even if goal not achieved")
        
        # Challenge 2: Cost Tracking
        print("\n2. Cost Management:")
        print(f"   Tokens used: {self.total_tokens}")
        print(f"   Estimated cost: ${self.total_tokens * 0.00002:.4f}")
        print("   ✓ Tracking usage for cost awareness")
        
        # Challenge 3: State Management
        print("\n3. State Management:")
        print(f"   Memory items: {len(self.memory)}")
        print(f"   Conversation history: {len(self.conversation_history)} messages")
        print("   ✓ Maintaining state across iterations")
        
        # Challenge 4: Error Handling
        print("\n4. Error Handling:")
        print("   ✓ Graceful handling of missing information")
        print("   ✓ Fallback to available data")
        print("   ✓ Clear completion criteria")


def compare_with_chatbot(topic: str):
    """
    Demonstrate the difference between a chatbot and an agent.
    """
    print("\n" + "🔄"*30)
    print("CHATBOT vs AGENT COMPARISON")
    print("🔄"*30)
    
    # Chatbot approach
    print("\n📱 CHATBOT APPROACH:")
    print("-"*40)
    print(f"User: Tell me about {topic}")
    print(f"Chatbot: {topic.title()} is an important subject. It has many benefits and applications.")
    print("Result: Generic, single response, no research")
    
    # Agent approach
    print("\n🤖 AGENT APPROACH:")
    print("-"*40)
    agent = ResearchAgent(autonomy_level=4)
    report = agent.research_loop(topic)
    print(report)
    
    # Show challenges handled
    agent.demonstrate_challenges()


def main():
    """
    Main function to run the challenge project.
    """
    print("\n" + "🎯"*30)
    print("CHAPTER 10 CHALLENGE: PERSONAL RESEARCH ASSISTANT")
    print("🎯"*30)
    
    print("\n📚 This demonstrates the key concepts from Chapter 10:")
    print("• Agent vs Chatbot differences")
    print("• The agent loop (Observe → Think → Act → Reflect → Learn)")
    print("• Different autonomy levels")
    print("• Common challenges and solutions")
    
    # Get user input
    print("\n" + "-"*60)
    print("Choose a demo option:")
    print("1. Research 'benefits of exercise' (pre-loaded data)")
    print("2. Research 'artificial intelligence' (pre-loaded data)")
    print("3. Compare chatbot vs agent approach")
    print("4. Test different autonomy levels")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        agent = ResearchAgent(autonomy_level=4)
        report = agent.research_loop("benefits of exercise")
        print(report)
        
    elif choice == "2":
        agent = ResearchAgent(autonomy_level=4)
        report = agent.research_loop("artificial intelligence")
        print(report)
        
    elif choice == "3":
        compare_with_chatbot("benefits of exercise")
        
    elif choice == "4":
        topic = "benefits of exercise"
        for level in [2, 3, 4]:
            print(f"\n{'='*60}")
            print(f"Testing Autonomy Level {level}")
            print('='*60)
            agent = ResearchAgent(autonomy_level=level)
            agent.research_loop(topic)
            time.sleep(1)
    
    else:
        print("Invalid choice. Running default demo...")
        agent = ResearchAgent()
        report = agent.research_loop("benefits of exercise")
        print(report)
    
    print("\n" + "🎉"*30)
    print("Challenge complete! You've demonstrated key agent concepts.")
    print("Next step: Build real agents with LangChain in Chapter 11!")
    print("🎉"*30)


if __name__ == "__main__":
    main()