# From: AI Agents Book - Chapter 13, Section 13.5
# File: document_memory.py

from semantic_memory import SemanticMemory


def chunk_text(text, chunk_size=500, overlap=50):
    """Split text into overlapping chunks."""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    
    return chunks


class DocumentMemory(SemanticMemory):
    """Semantic memory that handles long documents by chunking."""
    
    def add_document(self, content, source=None):
        """Add a long document by chunking it."""
        chunks = chunk_text(content)
        
        for i, chunk in enumerate(chunks):
            self.add(
                content=chunk,
                metadata={
                    "source": source or "unknown",
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
            )
        
        return len(chunks)


# Example usage
if __name__ == "__main__":
    doc_memory = DocumentMemory()
    
    meeting_notes = """
    Project Phoenix kickoff meeting - January 10th.
    Attendees: Sarah (tech lead), Tom (backend), Alex (design), Mike (PM).
    
    We discussed the project timeline. The deadline is March 15th, giving us 
    roughly 10 weeks. Sarah raised concerns about the authentication module
    complexity. Tom suggested using Auth0 to save time.
    
    Budget was confirmed at $50,000. This needs to cover all development 
    and third-party services. Alex will present design mockups next week.
    
    Action items:
    - Sarah: Research Auth0 integration (due Jan 15)
    - Tom: Set up development environment (due Jan 12)
    - Alex: Complete wireframes (due Jan 17)
    - Mike: Create detailed project timeline (due Jan 14)
    """
    
    chunks_added = doc_memory.add_document(meeting_notes, source="kickoff_meeting")
    print(f"Added {chunks_added} chunks")
    
    # Now search across the document
    results = doc_memory.search("What are the concerns about the project?")
    print("\nSearch results:")
    for r in results[:3]:
        print(f"  - {r['content'][:100]}...")
