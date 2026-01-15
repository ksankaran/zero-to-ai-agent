# From: Zero to AI Agent, Chapter 7, Section 7.3
# File: exercise_2_7_3_solution.py

"""
Exercise 2 Solution: Context Window Planning
Strategies for managing limited context windows effectively.
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
import math


@dataclass
class ContextStrategy:
    """Strategy for managing context within token limits."""
    name: str
    approach: str
    implementation: str
    pros: List[str]
    cons: List[str]
    token_allocation: Dict[str, int]


def plan_context_strategies(context_limit: int = 4000):
    """
    Plan strategies for different context window challenges.
    
    Args:
        context_limit: Available context window in tokens
    """
    
    print("=" * 70)
    print("EXERCISE 2: CONTEXT WINDOW PLANNING")
    print("=" * 70)
    print(f"Context Window Limit: {context_limit} tokens")
    print("=" * 70)
    
    # Solve each scenario
    solve_long_conversation()
    solve_large_document()
    solve_persistent_chat()
    
    # General strategies
    show_context_management_techniques()
    
    # Best practices
    show_best_practices()


def solve_long_conversation():
    """Solution A: Having a 10,000 token conversation."""
    
    print("\n📊 SCENARIO A: 10,000 TOKEN CONVERSATION")
    print("-" * 50)
    
    strategy = ContextStrategy(
        name="Sliding Window with Summary",
        approach="Keep recent messages + summary of older ones",
        implementation="""
1. Maintain full recent context (last 2,500 tokens)
2. Summarize older messages (500 token summary)
3. Keep system prompt (100 tokens)
4. Reserve space for response (900 tokens)
        """,
        pros=[
            "Preserves recent context perfectly",
            "Maintains conversation continuity",
            "Old information still accessible via summary",
            "Efficient token usage"
        ],
        cons=[
            "Summary may lose nuance",
            "Requires periodic summarization calls",
            "Important details might be condensed"
        ],
        token_allocation={
            "System Prompt": 100,
            "Summary of Old": 500,
            "Recent Messages": 2500,
            "Response Buffer": 900,
            "Total": 4000
        }
    )
    
    print(f"Strategy: {strategy.name}")
    print(f"\nApproach: {strategy.approach}")
    print(f"\nImplementation:{strategy.implementation}")
    
    print("\n📊 Token Allocation:")
    for component, tokens in strategy.token_allocation.items():
        if component != "Total":
            percentage = (tokens / 4000) * 100
            bar = "█" * int(percentage / 2)
            print(f"  {component:20} {tokens:4} tokens ({percentage:5.1f}%) {bar}")
    
    print(f"\n✅ Pros:")
    for pro in strategy.pros:
        print(f"  • {pro}")
    
    print(f"\n❌ Cons:")
    for con in strategy.cons:
        print(f"  • {con}")
    
    # Show implementation code
    print("\n💻 Implementation Example:")
    print("""
def manage_long_conversation(messages, max_tokens=4000):
    # Calculate current token usage
    total_tokens = sum(estimate_tokens(m['content']) for m in messages)
    
    if total_tokens <= max_tokens:
        return messages  # Everything fits
    
    # Keep system message
    result = [messages[0]] if messages[0]['role'] == 'system' else []
    
    # Summarize older messages
    old_messages = messages[1:-10]  # All but last 10
    if old_messages:
        summary = summarize_messages(old_messages)
        result.append({"role": "system", "content": f"Previous conversation: {summary}"})
    
    # Add recent messages
    result.extend(messages[-10:])
    
    return result
    """)


def solve_large_document():
    """Solution B: Analyzing a 50,000 token document."""
    
    print("\n📄 SCENARIO B: 50,000 TOKEN DOCUMENT ANALYSIS")
    print("-" * 50)
    
    strategies = [
        {
            "name": "Chunking with Overlap",
            "description": "Divide into overlapping chunks",
            "chunks": math.ceil(50000 / 3000),  # 3000 tokens per chunk
            "overlap": 500,
            "process": [
                "1. Split document into 3,000 token chunks",
                "2. Keep 500 token overlap between chunks",
                "3. Process each chunk independently",
                "4. Combine results with meta-analysis"
            ]
        },
        {
            "name": "Hierarchical Summarization",
            "description": "Multi-level summary approach",
            "levels": 3,
            "process": [
                "1. Split into 10 sections (5,000 tokens each)",
                "2. Summarize each to 400 tokens",
                "3. Combine summaries (4,000 tokens)",
                "4. Generate final analysis"
            ]
        },
        {
            "name": "Extractive + Focus",
            "description": "Extract key sections then deep dive",
            "process": [
                "1. Quick scan for key sections (headers, conclusions)",
                "2. Extract most relevant 3,500 tokens",
                "3. Focused analysis on extracts",
                "4. Reference back to specific sections as needed"
            ]
        }
    ]
    
    print("Multiple Strategies Available:\n")
    
    for i, strategy in enumerate(strategies, 1):
        print(f"{i}. {strategy['name']}")
        print(f"   {strategy['description']}")
        print(f"\n   Process:")
        for step in strategy["process"]:
            print(f"   {step}")
        print()
    
    # Detailed implementation of best approach
    print("🏆 RECOMMENDED APPROACH: Chunking with Overlap")
    print("-" * 30)
    
    print("""
def analyze_large_document(document, chunk_size=3000, overlap=500):
    chunks = []
    position = 0
    
    # Create overlapping chunks
    while position < len(document):
        chunk_end = position + chunk_size
        chunk = document[position:chunk_end]
        
        chunks.append({
            'content': chunk,
            'start': position,
            'end': chunk_end
        })
        
        position += (chunk_size - overlap)
    
    # Process each chunk
    analyses = []
    for i, chunk in enumerate(chunks):
        prompt = f\"\"\"
        Analyzing part {i+1}/{len(chunks)} of document.
        Context from previous: {analyses[-1][:200] if analyses else 'None'}
        
        Text:
        {chunk['content']}
        
        Provide key points and analysis:
        \"\"\"
        
        analysis = llm_call(prompt, max_tokens=500)
        analyses.append(analysis)
    
    # Final synthesis
    final_prompt = f\"\"\"
    Synthesize these analyses into a coherent summary:
    {' '.join(analyses)}
    \"\"\"
    
    return llm_call(final_prompt)
    """)
    
    print("\n📊 Token Budget per Chunk:")
    print("  Document chunk: 3,000 tokens")
    print("  Context/prompt: 500 tokens")
    print("  Response space: 500 tokens")
    print("  Total per call: 4,000 tokens")
    print(f"\n  Total chunks needed: ~{math.ceil(50000/2500)} (with overlap)")


def solve_persistent_chat():
    """Solution C: Maintaining chat history over multiple sessions."""
    
    print("\n💬 SCENARIO C: PERSISTENT CHAT HISTORY")
    print("-" * 50)
    
    print("Strategy: Hierarchical Memory System\n")
    
    memory_layers = [
        {
            "layer": "Working Memory",
            "tokens": 2000,
            "content": "Current conversation (last 5-10 messages)",
            "persistence": "In-context"
        },
        {
            "layer": "Session Summary",
            "tokens": 500,
            "content": "Summary of current session",
            "persistence": "Generated at intervals"
        },
        {
            "layer": "Long-term Memory",
            "tokens": 300,
            "content": "Key facts, preferences, important history",
            "persistence": "Database/file storage"
        },
        {
            "layer": "Context Prompt",
            "tokens": 200,
            "content": "System prompt + user preferences",
            "persistence": "Configuration"
        },
        {
            "layer": "Response Buffer",
            "tokens": 1000,
            "content": "Space for generation",
            "persistence": "N/A"
        }
    ]
    
    print("Memory Architecture:")
    total = 0
    for layer in memory_layers:
        total += layer["tokens"]
        print(f"\n📁 {layer['layer']}")
        print(f"   Tokens: {layer['tokens']}")
        print(f"   Content: {layer['content']}")
        print(f"   Persistence: {layer['persistence']}")
    
    print(f"\n   Total: {total} tokens")
    
    print("\n💾 Implementation:")
    print("""
class PersistentChatbot:
    def __init__(self, user_id):
        self.user_id = user_id
        self.working_memory = []
        self.session_summary = ""
        self.long_term_memory = self.load_user_memory()
    
    def load_user_memory(self):
        # Load from database/file
        return {
            "name": "User's name",
            "preferences": {...},
            "key_facts": [...],
            "conversation_summaries": [...]
        }
    
    def build_context(self, new_message):
        context = []
        
        # 1. System prompt + long-term memory
        context.append({
            "role": "system",
            "content": f"You are a helpful assistant. User info: {self.long_term_memory}"
        })
        
        # 2. Session summary if exists
        if self.session_summary:
            context.append({
                "role": "system",
                "content": f"Current session summary: {self.session_summary}"
            })
        
        # 3. Recent messages (working memory)
        context.extend(self.working_memory[-10:])
        
        # 4. New message
        context.append({"role": "user", "content": new_message})
        
        return context
    
    def save_to_long_term(self):
        # Periodically extract and save important information
        important_facts = extract_key_information(self.working_memory)
        self.long_term_memory['key_facts'].extend(important_facts)
        save_to_database(self.user_id, self.long_term_memory)
    """)


def show_context_management_techniques():
    """Show various context management techniques."""
    
    print("\n" + "=" * 70)
    print("CONTEXT MANAGEMENT TECHNIQUES")
    print("=" * 70)
    
    techniques = [
        {
            "name": "Sliding Window",
            "description": "Keep only recent N messages",
            "code": "messages = messages[-20:]",
            "use_case": "Simple conversations"
        },
        {
            "name": "Summarization",
            "description": "Replace old messages with summary",
            "code": "summary = summarize(messages[:-10])\nmessages = [summary] + messages[-10:]",
            "use_case": "Long conversations"
        },
        {
            "name": "Importance Scoring",
            "description": "Keep only important messages",
            "code": "messages = [m for m in messages if m['importance'] > threshold]",
            "use_case": "Information-dense chats"
        },
        {
            "name": "Compression",
            "description": "Compress message content",
            "code": "messages = [compress(m) for m in messages]",
            "use_case": "Verbose content"
        },
        {
            "name": "Chunking",
            "description": "Process in segments",
            "code": "for chunk in chunks(document, 3000):\n    process(chunk)",
            "use_case": "Large documents"
        }
    ]
    
    for technique in techniques:
        print(f"\n📋 {technique['name']}")
        print(f"   {technique['description']}")
        print(f"   Use case: {technique['use_case']}")
        print(f"   Example:")
        for line in technique['code'].split('\n'):
            print(f"      {line}")


def show_best_practices():
    """Show best practices for context management."""
    
    print("\n" + "=" * 70)
    print("BEST PRACTICES")
    print("=" * 70)
    
    practices = [
        "🎯 Always reserve tokens for response (20-25% of limit)",
        "📊 Track token usage proactively, don't wait for errors",
        "🔄 Implement graceful degradation when approaching limits",
        "💾 Store important information externally",
        "📝 Summarize proactively, not reactively",
        "🎨 Design prompts to be context-efficient",
        "🔍 Use retrieval for reference material",
        "⚡ Cache frequently used context",
        "📈 Monitor and optimize token usage patterns",
        "🛡️ Have fallback strategies for context overflow"
    ]
    
    print("\nKey Guidelines:")
    for practice in practices:
        print(f"  {practice}")
    
    print("\n📏 Token Budgeting Formula:")
    print("  Available = Context_Limit - Response_Buffer")
    print("  Usable = Available * 0.9  (safety margin)")
    print("  Per_Message = Usable / Expected_Conversation_Length")


def main():
    """Run context window planning exercise."""
    
    plan_context_strategies(context_limit=4000)
    
    print("\n" + "=" * 70)
    print("EXERCISE 2 COMPLETE")
    print("=" * 70)
    print("\n✅ You now understand how to manage limited context windows")
    print("   for various scenarios: long chats, large docs, and persistence!")


if __name__ == "__main__":
    main()
