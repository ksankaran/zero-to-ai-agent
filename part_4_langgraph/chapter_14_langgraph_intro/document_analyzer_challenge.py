# From: Building AI Agents, Chapter 14 Challenge Project
# Save as: document_analyzer_challenge.py
# Challenge: Build a Multi-Stage Document Analyzer

"""
CHAPTER 14 CHALLENGE: Multi-Stage Document Analyzer

Build a sophisticated document analysis agent that demonstrates everything
you learned in Chapter 14:
- State design with TypedDict and Annotated[list, add]
- Multiple nodes (at least 6)
- Multi-way branching (4+ document types)
- Quality-check loops with iteration limits
- Debugging support

REQUIREMENTS:
1. Classify documents into 4+ types (technical, business, legal, academic)
2. Route to specialized extraction nodes based on type
3. Evaluate extraction quality and retry if needed (max 2 retries)
4. Accumulate extracted information using Annotated[list, add]
5. Include debug output for tracing execution

YOUR TASKS:
1. Complete the State definition
2. Implement all node functions
3. Create the routing function
4. Build and compile the graph
5. Test with the sample documents provided

Good luck! 🚀
"""

import os
from typing import TypedDict, Annotated, Literal
from operator import add
from dotenv import load_dotenv

load_dotenv()

# Uncomment when ready to use LLM
# from langchain_openai import ChatOpenAI
# from langgraph.graph import StateGraph, START, END

# =============================================================================
# DEBUG FLAG - Set to True to see execution trace
# =============================================================================
DEBUG = True

def debug_print(*args, **kwargs):
    """Print only when DEBUG is True."""
    if DEBUG:
        print(*args, **kwargs)


# =============================================================================
# STATE DEFINITION
# =============================================================================

class DocumentState(TypedDict):
    """State for the document analyzer.
    
    TODO: Complete this state definition with:
    - document: str - The input document text
    - doc_type: str - Classification result (technical/business/legal/academic)
    - extracted_info: Annotated[list, add] - Accumulated extractions
    - quality_score: float - Quality of extraction (0.0 to 1.0)
    - iteration_count: int - Number of extraction attempts
    - max_iterations: int - Maximum allowed attempts
    - final_summary: str - Final analysis summary
    """
    # TODO: Add your state fields here
    pass


# =============================================================================
# NODE FUNCTIONS
# =============================================================================

def classify_document(state: DocumentState) -> dict:
    """Classify the document into one of 4 types.
    
    Types:
    - technical: Research papers, technical docs, API documentation
    - business: Reports, memos, financial documents
    - legal: Contracts, agreements, legal notices
    - academic: Essays, thesis, scholarly articles
    
    TODO: Implement classification logic
    - Use keywords or LLM to classify
    - Return {"doc_type": "technical|business|legal|academic"}
    """
    debug_print(f"\n{'='*50}")
    debug_print("🔵 ENTERING: classify_document")
    debug_print(f"{'='*50}")
    
    document = state.get("document", "")
    
    # TODO: Implement classification
    # Hint: Look for keywords like "abstract", "whereas", "quarterly", "methodology"
    
    doc_type = "technical"  # Placeholder
    
    debug_print(f"📄 Classified as: {doc_type}")
    return {"doc_type": doc_type}


def extract_technical(state: DocumentState) -> dict:
    """Extract information from technical documents.
    
    Extract:
    - Methods/approaches used
    - Key findings
    - Technologies mentioned
    
    TODO: Implement extraction logic
    - Return {"extracted_info": [list of extracted items]}
    - Increment iteration_count
    """
    debug_print(f"\n{'='*50}")
    debug_print("🔵 ENTERING: extract_technical")
    debug_print(f"{'='*50}")
    
    # TODO: Implement technical extraction
    
    return {
        "extracted_info": ["[Technical extraction placeholder]"],
        "iteration_count": state.get("iteration_count", 0) + 1
    }


def extract_business(state: DocumentState) -> dict:
    """Extract information from business documents.
    
    Extract:
    - Key metrics and numbers
    - Decisions made
    - Action items
    
    TODO: Implement extraction logic
    """
    debug_print(f"\n{'='*50}")
    debug_print("🔵 ENTERING: extract_business")
    debug_print(f"{'='*50}")
    
    # TODO: Implement business extraction
    
    return {
        "extracted_info": ["[Business extraction placeholder]"],
        "iteration_count": state.get("iteration_count", 0) + 1
    }


def extract_legal(state: DocumentState) -> dict:
    """Extract information from legal documents.
    
    Extract:
    - Parties involved
    - Key obligations
    - Important dates
    
    TODO: Implement extraction logic
    """
    debug_print(f"\n{'='*50}")
    debug_print("🔵 ENTERING: extract_legal")
    debug_print(f"{'='*50}")
    
    # TODO: Implement legal extraction
    
    return {
        "extracted_info": ["[Legal extraction placeholder]"],
        "iteration_count": state.get("iteration_count", 0) + 1
    }


def extract_academic(state: DocumentState) -> dict:
    """Extract information from academic documents.
    
    Extract:
    - Main thesis/argument
    - Methodology
    - Conclusions
    
    TODO: Implement extraction logic
    """
    debug_print(f"\n{'='*50}")
    debug_print("🔵 ENTERING: extract_academic")
    debug_print(f"{'='*50}")
    
    # TODO: Implement academic extraction
    
    return {
        "extracted_info": ["[Academic extraction placeholder]"],
        "iteration_count": state.get("iteration_count", 0) + 1
    }


def evaluate_quality(state: DocumentState) -> dict:
    """Evaluate the quality of extraction.
    
    TODO: Implement quality evaluation
    - Check if extracted_info is meaningful
    - Return {"quality_score": 0.0 to 1.0}
    
    Quality criteria:
    - At least 3 items extracted
    - Items are not placeholders
    - Items are relevant to doc_type
    """
    debug_print(f"\n{'='*50}")
    debug_print("🔵 ENTERING: evaluate_quality")
    debug_print(f"{'='*50}")
    
    extracted = state.get("extracted_info", [])
    
    # TODO: Implement quality scoring
    # Placeholder: simple length-based score
    quality_score = min(len(extracted) / 5, 1.0)
    
    debug_print(f"📊 Quality score: {quality_score}")
    debug_print(f"📊 Iteration: {state.get('iteration_count', 0)}")
    
    return {"quality_score": quality_score}


def generate_summary(state: DocumentState) -> dict:
    """Generate final summary of the analysis.
    
    TODO: Implement summary generation
    - Combine all extracted information
    - Create a coherent summary
    - Return {"final_summary": "..."}
    """
    debug_print(f"\n{'='*50}")
    debug_print("🔵 ENTERING: generate_summary")
    debug_print(f"{'='*50}")
    
    doc_type = state.get("doc_type", "unknown")
    extracted = state.get("extracted_info", [])
    
    # TODO: Generate a meaningful summary
    summary = f"Analysis of {doc_type} document. Found {len(extracted)} items."
    
    debug_print(f"📝 Summary generated")
    return {"final_summary": summary}


# =============================================================================
# ROUTING FUNCTIONS
# =============================================================================

def route_by_doc_type(state: DocumentState) -> Literal["extract_technical", "extract_business", "extract_legal", "extract_academic"]:
    """Route to appropriate extraction node based on document type.
    
    TODO: Implement routing logic
    - Read doc_type from state
    - Return the appropriate node name
    """
    debug_print(f"\n🔀 ROUTING: route_by_doc_type")
    
    doc_type = state.get("doc_type", "technical")
    
    # TODO: Implement routing
    route_map = {
        "technical": "extract_technical",
        "business": "extract_business",
        "legal": "extract_legal",
        "academic": "extract_academic"
    }
    
    destination = route_map.get(doc_type, "extract_technical")
    debug_print(f"   → Going to: {destination}")
    
    return destination


def route_quality_check(state: DocumentState) -> Literal["generate_summary", "retry_extraction"]:
    """Decide whether to retry extraction or proceed to summary.
    
    TODO: Implement quality check routing
    - If quality_score >= 0.7, go to generate_summary
    - If iteration_count >= max_iterations, go to generate_summary (give up)
    - Otherwise, go to retry_extraction
    """
    debug_print(f"\n🔀 ROUTING: route_quality_check")
    
    quality = state.get("quality_score", 0)
    iterations = state.get("iteration_count", 0)
    max_iter = state.get("max_iterations", 2)
    
    # TODO: Implement routing logic
    if quality >= 0.7:
        debug_print(f"   ✅ Quality sufficient ({quality}), proceeding to summary")
        return "generate_summary"
    elif iterations >= max_iter:
        debug_print(f"   ⚠️ Max iterations reached ({iterations}), proceeding anyway")
        return "generate_summary"
    else:
        debug_print(f"   🔄 Quality low ({quality}), retrying extraction")
        return "retry_extraction"


# =============================================================================
# GRAPH CONSTRUCTION
# =============================================================================

def build_document_analyzer():
    """Build the document analyzer graph.
    
    TODO: Implement the graph structure
    
    Graph structure:
    START → classify_document → [route_by_doc_type] → extract_* → evaluate_quality
                                                                        ↓
                                                        [route_quality_check]
                                                           ↓           ↓
                                              generate_summary    retry (loop back)
                                                      ↓
                                                     END
    
    Hints:
    1. Create StateGraph with DocumentState
    2. Add all nodes
    3. Add edge from START to classify_document
    4. Add conditional edges for routing
    5. Add edge from generate_summary to END
    6. Handle retry loop (goes back to appropriate extract_* node)
    """
    
    # TODO: Build your graph here
    # 
    # graph = StateGraph(DocumentState)
    # 
    # # Add nodes
    # graph.add_node("classify_document", classify_document)
    # graph.add_node("extract_technical", extract_technical)
    # ... add more nodes ...
    # 
    # # Add edges
    # graph.add_edge(START, "classify_document")
    # graph.add_conditional_edges(
    #     "classify_document",
    #     route_by_doc_type,
    #     {...}
    # )
    # ... add more edges ...
    # 
    # return graph.compile()
    
    print("TODO: Implement build_document_analyzer()")
    return None


# =============================================================================
# TEST DOCUMENTS
# =============================================================================

SAMPLE_DOCUMENTS = {
    "technical": """
    Abstract: This paper presents a novel approach to natural language processing
    using transformer architectures. We implement a BERT-based model with custom
    attention mechanisms. Our methodology involves fine-tuning on domain-specific
    data. Key findings show 15% improvement in accuracy. Technologies used include
    PyTorch, Hugging Face Transformers, and CUDA for GPU acceleration.
    """,
    
    "business": """
    Q3 2024 Performance Report
    
    Revenue increased 23% year-over-year to $4.2M. The board has decided to
    expand into European markets. Action items: 1) Hire regional sales manager
    by Dec 1, 2) Complete compliance audit by Nov 15, 3) Launch marketing
    campaign in January. Customer acquisition cost decreased to $45.
    """,
    
    "legal": """
    SERVICE AGREEMENT
    
    This Agreement is entered into between ABC Corporation ("Provider") and
    XYZ Inc. ("Client") effective January 1, 2025. Provider agrees to deliver
    consulting services as described in Exhibit A. Client shall pay $10,000
    monthly. This agreement shall terminate on December 31, 2025. Either party
    may terminate with 30 days written notice.
    """,
    
    "academic": """
    Introduction: This thesis examines the impact of social media on political
    discourse. The central argument posits that algorithmic curation creates
    echo chambers. Our methodology combines quantitative analysis of 10,000
    posts with qualitative interviews of 50 participants. We conclude that
    platform design significantly influences information diversity. Future
    research should explore intervention strategies.
    """
}


# =============================================================================
# MAIN - Test your implementation
# =============================================================================

def main():
    """Test the document analyzer with sample documents."""
    
    print("=" * 60)
    print("📄 DOCUMENT ANALYZER CHALLENGE")
    print("=" * 60)
    
    # Build the graph
    analyzer = build_document_analyzer()
    
    if analyzer is None:
        print("\n❌ Graph not implemented yet!")
        print("Complete the TODO items and try again.")
        return
    
    # Test with each document type
    for doc_type, document in SAMPLE_DOCUMENTS.items():
        print(f"\n{'='*60}")
        print(f"📄 Testing {doc_type.upper()} document")
        print(f"{'='*60}")
        
        initial_state = {
            "document": document,
            "doc_type": "",
            "extracted_info": [],
            "quality_score": 0.0,
            "iteration_count": 0,
            "max_iterations": 2,
            "final_summary": ""
        }
        
        try:
            result = analyzer.invoke(initial_state)
            
            print(f"\n✅ RESULTS:")
            print(f"   Document type: {result.get('doc_type')}")
            print(f"   Items extracted: {len(result.get('extracted_info', []))}")
            print(f"   Quality score: {result.get('quality_score')}")
            print(f"   Iterations: {result.get('iteration_count')}")
            print(f"   Summary: {result.get('final_summary', '')[:100]}...")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*60}")
    print("🏁 Challenge complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()