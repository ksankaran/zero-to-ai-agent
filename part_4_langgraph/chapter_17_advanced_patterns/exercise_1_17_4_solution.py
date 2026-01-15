# From: Zero to AI Agent, Chapter 17, Section 17.4
# Save as: exercise_1_17_4_solution.py
# Exercise 1: Content Processing Pipeline

from typing import TypedDict, Optional
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

# Shared state schema for all subgraphs
class ContentState(TypedDict):
    raw_content: str
    # Validation fields
    is_valid: bool
    content_length: int
    detected_language: str
    validation_message: str
    # Enrichment fields
    metadata: dict
    entities: list[str]
    # Output fields
    formatted_output: str
    output_format: str  # "json", "markdown", "plain"
    # Config
    skip_enrichment: bool

# === SUBGRAPH 1: Input Validator ===

def build_input_validator():
    """Validates content length and detects language."""
    
    def check_length(state: ContentState) -> dict:
        content = state["raw_content"]
        length = len(content)
        
        is_valid = 10 <= length <= 10000
        message = "Content length OK" if is_valid else f"Invalid length: {length} chars"
        
        return {
            "content_length": length,
            "is_valid": is_valid,
            "validation_message": message
        }
    
    def detect_language(state: ContentState) -> dict:
        if not state["is_valid"]:
            return {"detected_language": "unknown"}
        
        response = llm.invoke(
            f"What language is this text written in? "
            f"Respond with just the language name:\n{state['raw_content'][:200]}"
        )
        return {"detected_language": response.content.strip()}
    
    graph = StateGraph(ContentState)
    graph.add_node("check_length", check_length)
    graph.add_node("detect_language", detect_language)
    
    graph.add_edge(START, "check_length")
    graph.add_edge("check_length", "detect_language")
    graph.add_edge("detect_language", END)
    
    return graph.compile()

# === SUBGRAPH 2: Content Enricher ===

def build_content_enricher():
    """Adds metadata and extracts entities."""
    
    def add_metadata(state: ContentState) -> dict:
        response = llm.invoke(
            f"Analyze this content and provide metadata.\n"
            f"Return: topic, category, reading_level (basic/intermediate/advanced)\n"
            f"Format: topic: X, category: Y, reading_level: Z\n\n"
            f"Content: {state['raw_content'][:500]}"
        )
        
        # Parse simple metadata
        metadata = {"raw": response.content}
        for part in response.content.split(","):
            if ":" in part:
                key, val = part.split(":", 1)
                metadata[key.strip().lower()] = val.strip()
        
        return {"metadata": metadata}
    
    def extract_entities(state: ContentState) -> dict:
        response = llm.invoke(
            f"Extract key entities (people, places, organizations, concepts) "
            f"from this text. Return as comma-separated list:\n{state['raw_content'][:500]}"
        )
        
        entities = [e.strip() for e in response.content.split(",") if e.strip()]
        return {"entities": entities[:10]}  # Limit to 10
    
    graph = StateGraph(ContentState)
    graph.add_node("add_metadata", add_metadata)
    graph.add_node("extract_entities", extract_entities)
    
    graph.add_edge(START, "add_metadata")
    graph.add_edge("add_metadata", "extract_entities")
    graph.add_edge("extract_entities", END)
    
    return graph.compile()

# === SUBGRAPH 3: Output Formatter ===

def build_output_formatter():
    """Formats content for different output types."""
    
    def format_output(state: ContentState) -> dict:
        fmt = state.get("output_format", "plain")
        content = state["raw_content"]
        metadata = state.get("metadata", {})
        entities = state.get("entities", [])
        
        if fmt == "json":
            import json
            output = json.dumps({
                "content": content,
                "language": state.get("detected_language", "unknown"),
                "length": state.get("content_length", 0),
                "metadata": metadata,
                "entities": entities
            }, indent=2)
        
        elif fmt == "markdown":
            output = f"""# Processed Content

## Original Content
{content}

## Metadata
- **Language**: {state.get('detected_language', 'unknown')}
- **Length**: {state.get('content_length', 0)} characters
- **Topic**: {metadata.get('topic', 'N/A')}
- **Category**: {metadata.get('category', 'N/A')}

## Extracted Entities
{chr(10).join(['- ' + e for e in entities]) if entities else 'None extracted'}
"""
        
        else:  # plain
            output = f"""Content Processing Results
{'=' * 40}
Content: {content[:200]}...
Language: {state.get('detected_language', 'unknown')}
Length: {state.get('content_length', 0)} chars
Entities: {', '.join(entities[:5]) if entities else 'None'}
"""
        
        return {"formatted_output": output}
    
    graph = StateGraph(ContentState)
    graph.add_node("format", format_output)
    graph.add_edge(START, "format")
    graph.add_edge("format", END)
    
    return graph.compile()

# === PARENT GRAPH: Content Processing Pipeline ===

def build_content_pipeline():
    """Compose all subgraphs into a pipeline."""
    
    validator = build_input_validator()
    enricher = build_content_enricher()
    formatter = build_output_formatter()
    
    def maybe_enrich(state: ContentState) -> str:
        """Decide whether to run enrichment."""
        if not state["is_valid"]:
            return "format"
        if state.get("skip_enrichment", False):
            return "format"
        return "enrich"
    
    pipeline = StateGraph(ContentState)
    
    pipeline.add_node("validate", validator)
    pipeline.add_node("enrich", enricher)
    pipeline.add_node("format", formatter)
    
    pipeline.add_edge(START, "validate")
    pipeline.add_conditional_edges(
        "validate",
        maybe_enrich,
        ["enrich", "format"]
    )
    pipeline.add_edge("enrich", "format")
    pipeline.add_edge("format", END)
    
    return pipeline.compile()

def run_content_pipeline():
    pipeline = build_content_pipeline()
    
    sample_content = """
    OpenAI released GPT-4 in March 2023, marking a significant advancement
    in artificial intelligence. The model demonstrated improved reasoning
    capabilities and was quickly adopted by Microsoft for integration into
    Bing and Office products. Researchers at Stanford University noted that
    GPT-4 showed emergent abilities not present in earlier versions.
    """
    
    # Test 1: Full pipeline with JSON output
    print("📊 Test 1: Full Pipeline (JSON)")
    print("=" * 50)
    
    result = pipeline.invoke({
        "raw_content": sample_content,
        "is_valid": False,
        "content_length": 0,
        "detected_language": "",
        "validation_message": "",
        "metadata": {},
        "entities": [],
        "formatted_output": "",
        "output_format": "json",
        "skip_enrichment": False
    })
    
    print(result["formatted_output"])
    
    # Test 2: Skip enrichment
    print("\n" + "=" * 50)
    print("📊 Test 2: Skip Enrichment (Markdown)")
    print("=" * 50)
    
    result = pipeline.invoke({
        "raw_content": sample_content,
        "is_valid": False,
        "content_length": 0,
        "detected_language": "",
        "validation_message": "",
        "metadata": {},
        "entities": [],
        "formatted_output": "",
        "output_format": "markdown",
        "skip_enrichment": True
    })
    
    print(result["formatted_output"])

if __name__ == "__main__":
    run_content_pipeline()
