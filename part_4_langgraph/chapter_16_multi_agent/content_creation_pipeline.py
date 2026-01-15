# From: Zero to AI Agent, Chapter 16 Challenge Project
# File: content_creation_pipeline.py

"""
Chapter 16 Challenge Project: Content Creation Pipeline

Multi-agent system that produces blog posts with:
- Topic Researcher: Gathers facts and background
- Outline Creator: Structures content into sections
- Draft Writer: Writes initial draft
- Editor: Reviews and improves draft
- SEO Optimizer: Adds keywords and improves searchability

Features:
- Pipeline flow: Research → Outline → Draft → Edit → SEO
- Quality loop: Editor can send back to Writer (max 2 revisions)
- Error handling with fallbacks
- Metrics reporting
"""

from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from datetime import datetime
import operator
import logging

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("content_pipeline")

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)


# =============================================================================
# STATE
# =============================================================================

class ContentState(TypedDict):
    topic: str
    research: str
    outline: str
    draft: str
    edited_draft: str
    final_content: str
    feedback: str
    revision_count: int
    max_revisions: int
    approved: bool
    stage_times: Annotated[list[str], operator.add]  # Track time per stage


# =============================================================================
# HELPER: Time tracker
# =============================================================================

def track_time(agent_name: str, start: datetime) -> str:
    """Create a time tracking entry."""
    duration = (datetime.now() - start).total_seconds()
    return f"{agent_name}: {duration:.2f}s"


# =============================================================================
# AGENTS
# =============================================================================

def topic_researcher(state: ContentState) -> dict:
    """Gathers facts and background on the topic."""
    start = datetime.now()
    logger.info(f"[Researcher] Starting research on: {state['topic']}")
    
    try:
        prompt = f"""Research the topic: {state['topic']}

Provide:
1. Key facts (3-4 bullet points)
2. Background context
3. Current relevance/trends
4. Target audience interests

Keep it concise but informative."""

        response = llm.invoke(prompt)
        
        logger.info("[Researcher] Research complete")
        return {
            "research": response.content,
            "stage_times": [track_time("Researcher", start)]
        }
    except Exception as e:
        logger.error(f"[Researcher] Error: {e}")
        return {
            "research": f"Basic research on {state['topic']}: A popular and relevant topic.",
            "stage_times": [track_time("Researcher (fallback)", start)]
        }


def outline_creator(state: ContentState) -> dict:
    """Creates a structured outline for the content."""
    start = datetime.now()
    logger.info("[Outline] Creating content structure")
    
    try:
        prompt = f"""Based on this research, create a blog post outline:

TOPIC: {state['topic']}

RESEARCH:
{state['research']}

Create an outline with:
- Catchy title
- Introduction hook
- 3-4 main sections with subpoints
- Conclusion with call-to-action

Format as a clear outline structure."""

        response = llm.invoke(prompt)
        
        logger.info("[Outline] Structure created")
        return {
            "outline": response.content,
            "stage_times": [track_time("Outline Creator", start)]
        }
    except Exception as e:
        logger.error(f"[Outline] Error: {e}")
        return {
            "outline": f"I. Introduction\nII. Main Points about {state['topic']}\nIII. Conclusion",
            "stage_times": [track_time("Outline Creator (fallback)", start)]
        }


def draft_writer(state: ContentState) -> dict:
    """Writes the initial draft based on outline."""
    start = datetime.now()
    revision_note = f" (revision {state['revision_count']})" if state['revision_count'] > 0 else ""
    logger.info(f"[Writer] Writing draft{revision_note}")
    
    try:
        if state['revision_count'] > 0 and state['feedback']:
            # Revision mode - incorporate feedback
            prompt = f"""Revise this blog post based on the feedback:

CURRENT DRAFT:
{state['edited_draft'] or state['draft']}

EDITOR FEEDBACK:
{state['feedback']}

Write an improved version that addresses all feedback points.
Maintain the overall structure but improve quality."""
        else:
            # Initial draft
            prompt = f"""Write a blog post based on this outline:

TOPIC: {state['topic']}

OUTLINE:
{state['outline']}

RESEARCH:
{state['research']}

Write engaging, informative content:
- Use conversational tone
- Include specific facts from research
- Make it 300-400 words
- Use subheadings for sections"""

        response = llm.invoke(prompt)
        
        logger.info("[Writer] Draft complete")
        return {
            "draft": response.content,
            "stage_times": [track_time(f"Writer{revision_note}", start)]
        }
    except Exception as e:
        logger.error(f"[Writer] Error: {e}")
        return {
            "draft": f"# {state['topic']}\n\nContent about {state['topic']}...",
            "stage_times": [track_time("Writer (fallback)", start)]
        }


def editor(state: ContentState) -> dict:
    """Reviews and provides feedback on the draft."""
    start = datetime.now()
    logger.info(f"[Editor] Reviewing draft (revision {state['revision_count']})")
    
    try:
        prompt = f"""Review this blog post draft:

{state['draft']}

Evaluate:
1. Content quality (facts, depth)
2. Writing clarity
3. Engagement level
4. Structure and flow
5. Length (should be 300+ words)

If the draft is good (score 7+/10), respond with:
APPROVED: Yes
FEEDBACK: Brief praise

If it needs work, respond with:
APPROVED: No
FEEDBACK: Specific improvements needed (bullet points)"""

        response = llm.invoke(prompt)
        result = response.content
        
        # Parse response
        approved = "APPROVED: Yes" in result or "approved: yes" in result.lower()
        
        # Extract feedback
        if "FEEDBACK:" in result:
            feedback = result.split("FEEDBACK:")[-1].strip()
        else:
            feedback = result
        
        logger.info(f"[Editor] Review complete - Approved: {approved}")
        return {
            "edited_draft": state['draft'],
            "feedback": feedback,
            "approved": approved,
            "revision_count": state['revision_count'] + 1,
            "stage_times": [track_time("Editor", start)]
        }
    except Exception as e:
        logger.error(f"[Editor] Error: {e}")
        return {
            "edited_draft": state['draft'],
            "approved": True,  # Approve on error to continue
            "feedback": "Auto-approved due to processing issue",
            "revision_count": state['revision_count'] + 1,
            "stage_times": [track_time("Editor (fallback)", start)]
        }


def seo_optimizer(state: ContentState) -> dict:
    """Adds SEO keywords and improves searchability."""
    start = datetime.now()
    logger.info("[SEO] Optimizing for search")
    
    try:
        prompt = f"""Optimize this blog post for SEO:

{state['edited_draft'] or state['draft']}

Add:
1. SEO-friendly title (with main keyword)
2. Meta description (150 chars)
3. 3-5 relevant keywords naturally in text
4. Internal/external link suggestions
5. Alt text suggestions for potential images

Return the optimized full article with SEO elements clearly marked."""

        response = llm.invoke(prompt)
        
        logger.info("[SEO] Optimization complete")
        return {
            "final_content": response.content,
            "stage_times": [track_time("SEO Optimizer", start)]
        }
    except Exception as e:
        logger.error(f"[SEO] Error: {e}")
        return {
            "final_content": state['edited_draft'] or state['draft'],
            "stage_times": [track_time("SEO Optimizer (fallback)", start)]
        }


# =============================================================================
# ROUTING
# =============================================================================

def should_revise(state: ContentState) -> Literal["revise", "optimize"]:
    """Decide if draft needs revision or can proceed to SEO."""
    if state['approved']:
        logger.info("[Router] Draft approved -> SEO")
        return "optimize"
    
    if state['revision_count'] >= state['max_revisions']:
        logger.info(f"[Router] Max revisions ({state['max_revisions']}) reached -> SEO")
        return "optimize"
    
    logger.info(f"[Router] Revision {state['revision_count']} requested -> Writer")
    return "revise"


# =============================================================================
# BUILD WORKFLOW
# =============================================================================

workflow = StateGraph(ContentState)

# Add nodes
workflow.add_node("researcher", topic_researcher)
workflow.add_node("outline", outline_creator)
workflow.add_node("writer", draft_writer)
workflow.add_node("editor", editor)
workflow.add_node("seo", seo_optimizer)

# Add edges
workflow.add_edge(START, "researcher")
workflow.add_edge("researcher", "outline")
workflow.add_edge("outline", "writer")
workflow.add_edge("writer", "editor")

# Conditional edge for revision loop
workflow.add_conditional_edges(
    "editor",
    should_revise,
    {
        "revise": "writer",
        "optimize": "seo"
    }
)

workflow.add_edge("seo", END)

content_pipeline = workflow.compile()


# =============================================================================
# METRICS REPORT
# =============================================================================

def print_metrics(state: ContentState):
    """Print stage timing metrics."""
    print("\n" + "=" * 50)
    print("PIPELINE METRICS")
    print("=" * 50)
    
    total_time = 0
    for entry in state['stage_times']:
        print(f"  {entry}")
        # Extract time from entry like "Writer: 1.23s"
        try:
            time_str = entry.split(":")[-1].strip().replace("s", "")
            total_time += float(time_str)
        except:
            pass
    
    print("-" * 50)
    print(f"  Total: {total_time:.2f}s")
    print(f"  Revisions: {state['revision_count']}")
    print(f"  Approved: {state['approved']}")
    print("=" * 50)


# =============================================================================
# RUN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("CONTENT CREATION PIPELINE")
    print("=" * 60)
    
    topic = "The Benefits of Learning Python in 2024"
    print(f"\nTopic: {topic}\n")
    
    result = content_pipeline.invoke({
        "topic": topic,
        "research": "",
        "outline": "",
        "draft": "",
        "edited_draft": "",
        "final_content": "",
        "feedback": "",
        "revision_count": 0,
        "max_revisions": 2,
        "approved": False,
        "stage_times": []
    })
    
    # Print metrics
    print_metrics(result)
    
    # Print final content
    print("\n" + "=" * 60)
    print("FINAL OPTIMIZED CONTENT")
    print("=" * 60)
    print(result['final_content'])
