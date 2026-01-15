# From: Zero to AI Agent, Chapter 17, Section 17.2
# Save as: exercise_1_17_2_solution.py
# Exercise 1: Research Assistant with Progress

import asyncio
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import StreamWriter
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class ResearchState(TypedDict):
    topic: str
    questions: list[str]
    research_results: list[str]
    final_report: str
    status: str

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, streaming=True)

async def generate_questions(state: ResearchState, writer: StreamWriter) -> dict:
    """Generate 3 research questions about the topic."""
    
    writer({
        "phase": "questions",
        "message": f"Generating research questions about: {state['topic']}"
    })
    
    response = await llm.ainvoke(
        f"Generate exactly 3 specific research questions about: {state['topic']}. "
        f"Format: One question per line, numbered 1-3."
    )
    
    # Parse questions from response
    questions = []
    for line in response.content.strip().split('\n'):
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith('-')):
            # Remove numbering/bullets
            question = line.lstrip('0123456789.-) ').strip()
            if question:
                questions.append(question)
    
    # Ensure we have exactly 3 questions
    questions = questions[:3] if len(questions) >= 3 else questions
    
    writer({
        "phase": "questions_complete",
        "message": f"Generated {len(questions)} questions"
    })
    
    return {"questions": questions, "status": "questions_generated"}

async def research_questions(state: ResearchState, writer: StreamWriter) -> dict:
    """Research each question with progress updates."""
    
    questions = state["questions"]
    results = []
    
    for i, question in enumerate(questions):
        progress = (i + 1) / len(questions) * 100
        
        writer({
            "phase": "researching",
            "progress": f"{progress:.0f}%",
            "message": f"Researching question {i + 1}/{len(questions)}: {question[:50]}..."
        })
        
        response = await llm.ainvoke(
            f"Provide a brief research finding (2-3 sentences) for: {question}"
        )
        
        results.append({
            "question": question,
            "finding": response.content
        })
        
        writer({
            "phase": "question_complete",
            "progress": f"{progress:.0f}%",
            "message": f"✓ Completed research for question {i + 1}"
        })
    
    return {"research_results": results, "status": "research_complete"}

async def compile_report(state: ResearchState, writer: StreamWriter) -> dict:
    """Compile findings into a final report."""
    
    writer({
        "phase": "compiling",
        "message": "Compiling final report..."
    })
    
    # Format research results
    findings_text = "\n".join([
        f"Q: {r['question']}\nA: {r['finding']}"
        for r in state["research_results"]
    ])
    
    response = await llm.ainvoke(
        f"Write a comprehensive research report summarizing these findings about "
        f"{state['topic']}:\n\n{findings_text}\n\n"
        f"Format as a professional report with introduction, key findings, and conclusion."
    )
    
    writer({
        "phase": "complete",
        "message": "Report compilation complete!"
    })
    
    return {"final_report": response.content, "status": "complete"}

def build_research_graph():
    workflow = StateGraph(ResearchState)
    
    workflow.add_node("generate_questions", generate_questions)
    workflow.add_node("research", research_questions)
    workflow.add_node("compile", compile_report)
    
    workflow.add_edge(START, "generate_questions")
    workflow.add_edge("generate_questions", "research")
    workflow.add_edge("research", "compile")
    workflow.add_edge("compile", END)
    
    return workflow.compile()

async def stream_final_report(graph, state: dict):
    """Stream the final report token-by-token."""
    
    print("\n📄 Final Report (streaming):\n")
    print("-" * 50)
    
    async for event in graph.astream_events(state, version="v2"):
        if event["event"] == "on_chat_model_stream":
            # Only stream from the compile node
            if "compile" in str(event.get("name", "")):
                chunk = event["data"]["chunk"]
                if hasattr(chunk, "content") and chunk.content:
                    print(chunk.content, end="", flush=True)
    
    print("\n" + "-" * 50)

async def run_research_assistant():
    """Run the research assistant with all streaming features."""
    
    graph = build_research_graph()
    
    topic = input("Enter a research topic: ").strip() or "The impact of AI on education"
    
    initial_state = {
        "topic": topic,
        "questions": [],
        "research_results": [],
        "final_report": "",
        "status": "starting"
    }
    
    print(f"\n🔬 Research Assistant - Investigating: {topic}")
    print("=" * 60)
    
    final_state = None
    
    # Stream progress updates
    async for mode, chunk in graph.astream(
        initial_state,
        stream_mode=["updates", "custom"]
    ):
        if mode == "custom":
            progress = chunk.get("progress", "")
            message = chunk.get("message", "")
            if progress:
                print(f"  [{progress}] {message}")
            else:
                print(f"  📡 {message}")
        elif mode == "updates":
            for node_name, updates in chunk.items():
                if updates.get("final_report"):
                    final_state = updates
    
    print("=" * 60)
    
    # Display the final report
    if final_state and final_state.get("final_report"):
        print("\n📄 FINAL REPORT:")
        print("-" * 60)
        print(final_state["final_report"])
        print("-" * 60)
    
    print("\n✅ Research complete!")

if __name__ == "__main__":
    asyncio.run(run_research_assistant())
