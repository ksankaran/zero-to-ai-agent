# From: AI Agents Book - Chapter 13, Section 13.3
# File: summary_memory.py

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI


class SummaryMemory:
    def __init__(self, system_prompt=None, max_messages=30, keep_recent=10):
        self.client = OpenAI()
        self.max_messages = max_messages
        self.keep_recent = keep_recent
        self.messages = []
        self.summaries = []  # Track all summaries for debugging
        
        if system_prompt:
            self.messages.append({
                "role": "system",
                "content": system_prompt
            })
    
    def _count_non_system(self):
        return len([m for m in self.messages if m["role"] != "system"])
    
    def _should_summarize(self):
        return self._count_non_system() > self.max_messages
    
    def _generate_summary(self, messages_to_summarize):
        conversation_text = "\n".join(
            f"{m['role'].upper()}: {m['content']}" 
            for m in messages_to_summarize
        )
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": f"""Summarize this conversation concisely, keeping key facts, 
decisions, and context needed to continue the discussion:

{conversation_text}

Provide a clear, structured summary:"""
            }],
            max_tokens=400
        )
        return response.choices[0].message.content
    
    def _perform_summarization(self):
        # Separate system messages from conversation
        system_msgs = [m for m in self.messages if m["role"] == "system" 
                       and "Summary of earlier" not in m["content"]]
        conversation = [m for m in self.messages if m["role"] != "system"
                        or "Summary of earlier" in m["content"]]
        
        # Select what to summarize vs keep
        to_summarize = conversation[:-self.keep_recent]
        to_keep = conversation[-self.keep_recent:]
        
        # Generate summary
        summary = self._generate_summary(to_summarize)
        self.summaries.append(summary)
        
        # Rebuild messages
        summary_msg = {
            "role": "system",
            "content": f"Summary of earlier conversation:\n{summary}"
        }
        self.messages = system_msgs + [summary_msg] + to_keep
        
        print(f"📝 Summarized {len(to_summarize)} messages into {len(summary.split())} words")
    
    def chat(self, user_input):
        # Add user message
        self.messages.append({"role": "user", "content": user_input})
        
        # Check if summarization needed
        if self._should_summarize():
            self._perform_summarization()
        
        # Make API call
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        
        assistant_reply = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": assistant_reply})
        
        return assistant_reply
    
    def get_message_count(self):
        return len(self.messages)
    
    def get_summaries(self):
        return self.summaries


# Example usage
if __name__ == "__main__":
    assistant = SummaryMemory(
        system_prompt="""You are a project planning assistant. Help users plan 
and track their projects. Remember details about their projects, team members, 
deadlines, and constraints.""",
        max_messages=20,
        keep_recent=8
    )
    
    # Test conversation
    test_messages = [
        "I'm starting a new mobile app project.",
        "The deadline is March 15th.",
        "My team has 2 developers and 1 designer.",
        "What should we focus on first?",
    ]
    
    for msg in test_messages:
        print(f"User: {msg}")
        response = assistant.chat(msg)
        print(f"Assistant: {response}\n")
