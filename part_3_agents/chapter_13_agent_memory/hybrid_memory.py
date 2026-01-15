# From: AI Agents Book - Chapter 13, Section 13.3
# File: hybrid_memory.py

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI


class HybridMemory:
    """
    Combines multiple memory strategies:
    - Full history for persistence/auditing
    - Active context for LLM (with summarization)
    - Extracted key facts for quick reference
    """
    
    def __init__(self, system_prompt=None, max_active_messages=30):
        self.client = OpenAI()
        self.full_history = []          # Complete record (for persistence)
        self.active_context = []        # What we send to LLM
        self.summaries = []             # Generated summaries
        self.key_facts = {}             # Extracted important facts
        self.max_active = max_active_messages
        
        if system_prompt:
            msg = {"role": "system", "content": system_prompt}
            self.full_history.append(msg)
            self.active_context.append(msg)
    
    def _extract_facts(self, content):
        """Extract key facts from content (placeholder for entity extraction)."""
        # In a full implementation, this would use NLP or LLM to extract
        # entities, preferences, and key information
        # See section 13.4 for full entity extraction
        pass
    
    def _should_summarize(self):
        non_system = [m for m in self.active_context if m["role"] != "system"]
        return len(non_system) > self.max_active
    
    def _summarize(self):
        """Summarize older messages in active context."""
        system_msgs = [m for m in self.active_context 
                       if m["role"] == "system" and "Summary" not in m["content"]]
        conversation = [m for m in self.active_context if m["role"] != "system"]
        
        # Keep recent messages
        keep_recent = 10
        to_summarize = conversation[:-keep_recent]
        to_keep = conversation[-keep_recent:]
        
        if not to_summarize:
            return
        
        # Generate summary
        text = "\n".join(f"{m['role']}: {m['content']}" for m in to_summarize)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": f"Summarize concisely:\n\n{text}"
            }],
            max_tokens=300
        )
        summary = response.choices[0].message.content
        self.summaries.append(summary)
        
        # Rebuild active context
        summary_msg = {"role": "system", "content": f"Earlier conversation summary:\n{summary}"}
        self.active_context = system_msgs + [summary_msg] + to_keep
    
    def _trim_if_needed(self):
        """Final safety trim if still too long after summarization."""
        max_total = self.max_active + 15  # Buffer for summaries
        while len(self.active_context) > max_total:
            # Remove oldest non-system message
            for i, m in enumerate(self.active_context):
                if m["role"] != "system":
                    self.active_context.pop(i)
                    break
    
    def process_message(self, role, content):
        """Process and store a message."""
        msg = {"role": role, "content": content}
        
        # Always store full history
        self.full_history.append(msg)
        self.active_context.append(msg)
        
        # Extract key facts
        self._extract_facts(content)
        
        # Summarize if needed
        if self._should_summarize():
            self._summarize()
        
        # Token-trim if still too long
        self._trim_if_needed()
    
    def chat(self, user_input):
        """Chat with the assistant."""
        self.process_message("user", user_input)
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.active_context
        )
        
        reply = response.choices[0].message.content
        self.process_message("assistant", reply)
        
        return reply
    
    def get_full_history(self):
        """Return complete conversation history."""
        return self.full_history
    
    def get_active_context_size(self):
        """Return current active context size."""
        return len(self.active_context)
    
    def get_key_facts(self):
        """Return extracted key facts."""
        return self.key_facts


# Example usage
if __name__ == "__main__":
    memory = HybridMemory(
        system_prompt="You are a helpful assistant.",
        max_active_messages=15
    )
    
    print(memory.chat("My name is Alice and I love hiking."))
    print(f"Active context: {memory.get_active_context_size()} messages")
    print(f"Full history: {len(memory.get_full_history())} messages")
