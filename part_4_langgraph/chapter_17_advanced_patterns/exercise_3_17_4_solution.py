# From: Zero to AI Agent, Chapter 17, Section 17.4
# Save as: exercise_3_17_4_solution.py
# Exercise 3: Document Review System (Hierarchical with 3 levels)

import operator
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)


# =============================================================================
# SHARED STATE
# =============================================================================

class ReviewState(TypedDict):
    document: str
    document_type: str  # "technical", "article", "report"
    # Technical review results
    fact_check_results: str
    code_validation_results: str
    technical_review_summary: str
    # Editorial review results
    grammar_review: str
    style_review: str
    editorial_review_summary: str
    # Final output
    all_feedback: Annotated[list[str], operator.add]
    final_review: str


# =============================================================================
# CORE FUNCTIONS (Level 3 operations - defined once, reused everywhere)
# =============================================================================

def check_facts(state: ReviewState) -> dict:
    """Check document for factual accuracy."""
    response = llm.invoke(
        f"Review this document for factual accuracy. "
        f"List any claims that need verification or seem incorrect:\n\n"
        f"{state['document'][:1000]}"
    )
    return {"fact_check_results": response.content}


def validate_code(state: ReviewState) -> dict:
    """Validate code snippets in document."""
    response = llm.invoke(
        f"Review this document for any code snippets. "
        f"Check for: syntax errors, best practices, security issues. "
        f"If no code present, note that.\n\n"
        f"{state['document'][:1000]}"
    )
    return {"code_validation_results": response.content}


def review_grammar(state: ReviewState) -> dict:
    """Review document grammar and spelling."""
    response = llm.invoke(
        f"Review this document for grammar and spelling errors. "
        f"List specific issues found:\n\n"
        f"{state['document'][:1000]}"
    )
    return {"grammar_review": response.content}


def review_style(state: ReviewState) -> dict:
    """Review document writing style."""
    response = llm.invoke(
        f"Review this document for writing style. "
        f"Comment on: clarity, tone, structure, readability:\n\n"
        f"{state['document'][:1000]}"
    )
    return {"style_review": response.content}


# =============================================================================
# LEVEL 3 SUBGRAPH WRAPPERS (for standalone/sequential use)
# =============================================================================

def build_fact_checker():
    """Level 3: Fact checking subgraph."""
    graph = StateGraph(ReviewState)
    graph.add_node("check", check_facts)
    graph.add_edge(START, "check")
    graph.add_edge("check", END)
    return graph.compile()


def build_code_validator():
    """Level 3: Code validation subgraph."""
    graph = StateGraph(ReviewState)
    graph.add_node("validate", validate_code)
    graph.add_edge(START, "validate")
    graph.add_edge("validate", END)
    return graph.compile()


def build_grammar_reviewer():
    """Level 3: Grammar review subgraph."""
    graph = StateGraph(ReviewState)
    graph.add_node("grammar", review_grammar)
    graph.add_edge(START, "grammar")
    graph.add_edge("grammar", END)
    return graph.compile()


def build_style_reviewer():
    """Level 3: Style review subgraph."""
    graph = StateGraph(ReviewState)
    graph.add_node("style", review_style)
    graph.add_edge(START, "style")
    graph.add_edge("style", END)
    return graph.compile()


# =============================================================================
# LEVEL 2 CORE FUNCTIONS (for parallel execution at Level 1)
# =============================================================================

def run_technical_review(state: ReviewState) -> dict:
    """Run technical review (fact check + code validation) sequentially.
    
    Note: We run these sequentially within this function because parallel
    subgraphs cause state conflicts. The parallelism happens at Level 1
    where technical and editorial reviews run simultaneously.
    """
    # Run fact check
    fact_result = check_facts(state)
    
    # Run code validation
    code_result = validate_code(state)
    
    # Summarize
    summary = (
        f"📊 TECHNICAL REVIEW SUMMARY\n"
        f"{'=' * 40}\n\n"
        f"🔍 Fact Check:\n{fact_result['fact_check_results']}\n\n"
        f"💻 Code Review:\n{code_result['code_validation_results']}"
    )
    
    return {
        "fact_check_results": fact_result["fact_check_results"],
        "code_validation_results": code_result["code_validation_results"],
        "technical_review_summary": summary,
        "all_feedback": [summary]
    }


def run_editorial_review(state: ReviewState) -> dict:
    """Run editorial review (grammar + style) sequentially.
    
    Note: We run these sequentially within this function because parallel
    subgraphs cause state conflicts. The parallelism happens at Level 1
    where technical and editorial reviews run simultaneously.
    """
    # Run grammar review
    grammar_result = review_grammar(state)
    
    # Run style review
    style_result = review_style(state)
    
    # Summarize
    summary = (
        f"📝 EDITORIAL REVIEW SUMMARY\n"
        f"{'=' * 40}\n\n"
        f"✏️ Grammar:\n{grammar_result['grammar_review']}\n\n"
        f"🎨 Style:\n{style_result['style_review']}"
    )
    
    return {
        "grammar_review": grammar_result["grammar_review"],
        "style_review": style_result["style_review"],
        "editorial_review_summary": summary,
        "all_feedback": [summary]
    }


# =============================================================================
# LEVEL 2 SUBGRAPH WRAPPERS (for standalone use)
# =============================================================================

def build_technical_review():
    """Level 2: Technical review subgraph."""
    graph = StateGraph(ReviewState)
    graph.add_node("review", run_technical_review)
    graph.add_edge(START, "review")
    graph.add_edge("review", END)
    return graph.compile()


def build_editorial_review():
    """Level 2: Editorial review subgraph."""
    graph = StateGraph(ReviewState)
    graph.add_node("review", run_editorial_review)
    graph.add_edge(START, "review")
    graph.add_edge("review", END)
    return graph.compile()


# =============================================================================
# LEVEL 1: Top-level Document Reviewer
# =============================================================================

def build_document_reviewer():
    """Level 1: Top-level orchestrator.
    
    Runs technical and editorial reviews in parallel using functions
    directly (not compiled subgraphs) to avoid state conflicts.
    """
    
    def compile_final_review(state: ReviewState) -> dict:
        final = (
            f"📋 COMPLETE DOCUMENT REVIEW\n"
            f"{'=' * 60}\n\n"
            f"Document Type: {state['document_type']}\n"
            f"Document Preview: {state['document'][:100]}...\n\n"
            f"{'=' * 60}\n\n"
        )
        
        for feedback in state["all_feedback"]:
            final += feedback + "\n\n"
        
        final += (
            f"{'=' * 60}\n"
            f"✅ Review Complete - All feedback compiled above\n"
            f"{'=' * 60}"
        )
        
        return {"final_review": final}
    
    graph = StateGraph(ReviewState)
    
    # Use functions directly for parallel execution
    graph.add_node("technical", run_technical_review)
    graph.add_node("editorial", run_editorial_review)
    graph.add_node("compile", compile_final_review)
    
    # Parallel execution of technical and editorial reviews
    graph.add_edge(START, "technical")
    graph.add_edge(START, "editorial")
    
    # Both converge to final compilation
    graph.add_edge("technical", "compile")
    graph.add_edge("editorial", "compile")
    
    graph.add_edge("compile", END)
    
    return graph.compile()


# =============================================================================
# DEMO
# =============================================================================

def run_document_review():
    reviewer = build_document_reviewer()
    
    # Sample technical document
    document = """
    Introduction to Python Decorators
    
    Decorators in Python are a powerfull design pattern that allows you to 
    modify the behavior of functions or classes. Their commonly used for 
    logging, authentication, and caching.
    
    Here's a basic example:
    
    def my_decorator(func):
        def wrapper():
            print("Before function call")
            func()
            print("After function call")
        return wrapper
    
    @my_decorator
    def say_hello():
        print("Hello!")
    
    The decorator syntax @my_decorator is equivelent to:
    say_hello = my_decorator(say_hello)
    
    Best practices include using functools.wraps to preserve function metadata
    and keeping decorators focused on a single responsibilty.
    """
    
    print("🔍 Starting Hierarchical Document Review")
    print("=" * 60)
    print("Structure:")
    print("  Level 1: DocumentReviewer")
    print("  ├── Level 2: TechnicalReview (parallel)")
    print("  │   ├── Level 3: FactChecker")
    print("  │   └── Level 3: CodeValidator")
    print("  └── Level 2: EditorialReview (parallel)")
    print("      ├── Level 3: GrammarReviewer")
    print("      └── Level 3: StyleReviewer")
    print("=" * 60 + "\n")
    
    result = reviewer.invoke({
        "document": document,
        "document_type": "technical tutorial",
        "fact_check_results": "",
        "code_validation_results": "",
        "technical_review_summary": "",
        "grammar_review": "",
        "style_review": "",
        "editorial_review_summary": "",
        "all_feedback": [],
        "final_review": ""
    })
    
    print(result["final_review"])


if __name__ == "__main__":
    run_document_review()