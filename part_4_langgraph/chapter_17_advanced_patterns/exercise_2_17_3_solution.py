# From: Zero to AI Agent, Chapter 17, Section 17.3
# Save as: exercise_2_17_3_solution.py
# Exercise 2: Parallel Document Analyzer

import operator
from typing import TypedDict, Annotated
from collections import Counter
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

class MainState(TypedDict):
    documents: list[dict]  # {id, title, content}
    analyses: Annotated[list[dict], operator.add]
    final_report: str

class DocumentAnalysisState(TypedDict):
    doc_id: str
    title: str
    content: str

def distribute_documents(state: MainState) -> list[Send]:
    """Send each document for parallel analysis."""
    return [
        Send("analyze", {
            "doc_id": doc.get("id", f"doc_{i}"),
            "title": doc.get("title", f"Document {i+1}"),
            "content": doc["content"]
        })
        for i, doc in enumerate(state["documents"])
    ]

def analyze_document(state: DocumentAnalysisState) -> dict:
    """Analyze a single document: themes, sentiment, action items."""
    
    response = llm.invoke(
        f"Analyze this document and provide structured analysis:\n\n"
        f"Title: {state['title']}\n"
        f"Content: {state['content']}\n\n"
        f"Provide:\n"
        f"1. KEY THEMES (list 3-5 themes, comma-separated)\n"
        f"2. SENTIMENT (Positive/Neutral/Negative with confidence %)\n"
        f"3. ACTION ITEMS (list any action items or recommendations)\n\n"
        f"Format strictly as:\n"
        f"THEMES: theme1, theme2, theme3\n"
        f"SENTIMENT: [Sentiment] ([confidence]%)\n"
        f"ACTIONS: action1; action2; action3"
    )
    
    content = response.content
    
    # Parse the structured response
    themes = []
    sentiment = "Neutral"
    sentiment_confidence = 50
    actions = []
    
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('THEMES:'):
            themes = [t.strip() for t in line[7:].split(',') if t.strip()]
        elif line.startswith('SENTIMENT:'):
            sent_part = line[10:].strip()
            if 'Positive' in sent_part:
                sentiment = 'Positive'
            elif 'Negative' in sent_part:
                sentiment = 'Negative'
            else:
                sentiment = 'Neutral'
            # Extract confidence if present
            import re
            conf_match = re.search(r'(\d+)%', sent_part)
            if conf_match:
                sentiment_confidence = int(conf_match.group(1))
        elif line.startswith('ACTIONS:'):
            actions = [a.strip() for a in line[8:].split(';') if a.strip()]
    
    print(f"📄 Analyzed: {state['title']}")
    
    return {"analyses": [{
        "doc_id": state["doc_id"],
        "title": state["title"],
        "themes": themes,
        "sentiment": sentiment,
        "sentiment_confidence": sentiment_confidence,
        "actions": actions,
        "raw_analysis": content
    }]}

def compile_report(state: MainState) -> dict:
    """Compile all analyses into a comprehensive report."""
    
    analyses = state["analyses"]
    
    # Aggregate themes across all documents
    all_themes = []
    for analysis in analyses:
        all_themes.extend(analysis.get("themes", []))
    
    theme_counts = Counter(all_themes)
    ranked_themes = theme_counts.most_common(10)
    
    # Aggregate sentiments
    sentiments = [a["sentiment"] for a in analyses]
    sentiment_summary = Counter(sentiments)
    
    # Collect all action items
    all_actions = []
    for analysis in analyses:
        for action in analysis.get("actions", []):
            all_actions.append({
                "action": action,
                "source": analysis["title"]
            })
    
    # Build report
    report_parts = []
    
    report_parts.append("=" * 60)
    report_parts.append("DOCUMENT ANALYSIS REPORT")
    report_parts.append("=" * 60)
    
    report_parts.append(f"\n📚 Documents Analyzed: {len(analyses)}")
    
    # Theme section
    report_parts.append("\n📌 RANKED THEMES (by frequency):")
    for i, (theme, count) in enumerate(ranked_themes, 1):
        report_parts.append(f"   {i}. {theme} (mentioned in {count} documents)")
    
    # Sentiment section
    report_parts.append("\n😊 SENTIMENT DISTRIBUTION:")
    for sent, count in sentiment_summary.items():
        pct = count / len(analyses) * 100
        report_parts.append(f"   • {sent}: {count} documents ({pct:.0f}%)")
    
    # Action items section
    report_parts.append(f"\n✅ ACTION ITEMS ({len(all_actions)} total):")
    for item in all_actions[:10]:  # Top 10
        report_parts.append(f"   • {item['action']}")
        report_parts.append(f"     (from: {item['source']})")
    
    # Individual document summaries
    report_parts.append("\n📄 INDIVIDUAL DOCUMENT ANALYSES:")
    for analysis in analyses:
        report_parts.append(f"\n   [{analysis['doc_id']}] {analysis['title']}")
        report_parts.append(f"   Sentiment: {analysis['sentiment']} ({analysis['sentiment_confidence']}% confidence)")
        report_parts.append(f"   Themes: {', '.join(analysis['themes'][:3])}")
    
    report_parts.append("\n" + "=" * 60)
    
    return {"final_report": "\n".join(report_parts)}

def build_document_analyzer_graph():
    workflow = StateGraph(MainState)
    
    workflow.add_node("distribute", lambda state: {})
    workflow.add_node("analyze", analyze_document)
    workflow.add_node("compile", compile_report)
    
    workflow.add_edge(START, "distribute")
    
    workflow.add_conditional_edges(
        "distribute",
        distribute_documents,
        ["analyze"]
    )
    
    workflow.add_edge("analyze", "compile")
    workflow.add_edge("compile", END)
    
    return workflow.compile()

def run_document_analyzer():
    graph = build_document_analyzer_graph()
    
    # Sample documents
    documents = [
        {
            "id": "doc_001",
            "title": "Q3 Sales Report",
            "content": "Sales increased 15% this quarter. The new marketing campaign "
                      "drove significant traffic. Customer satisfaction remains high. "
                      "We need to expand the sales team and improve CRM integration. "
                      "Action required: Hire 3 new sales representatives by Q4."
        },
        {
            "id": "doc_002",
            "title": "Engineering Update",
            "content": "The new feature release was delayed due to testing issues. "
                      "Technical debt is becoming a concern. Team morale is affected. "
                      "We need to prioritize refactoring and improve CI/CD pipeline. "
                      "Consider hiring a DevOps engineer."
        },
        {
            "id": "doc_003",
            "title": "Customer Feedback Summary",
            "content": "Users love the new interface design. Mobile app performance "
                      "has improved significantly. Some concerns about pricing tiers. "
                      "Feature requests include dark mode and offline support. "
                      "Overall satisfaction: 4.2/5 stars."
        },
        {
            "id": "doc_004",
            "title": "Market Analysis",
            "content": "Competitor X launched a similar product at lower price point. "
                      "Market share slightly decreased. Innovation is key to differentiation. "
                      "Recommend investing in R&D and exploring partnership opportunities. "
                      "Consider strategic acquisition of startup Y."
        }
    ]
    
    print(f"📚 Analyzing {len(documents)} documents in parallel...")
    print("=" * 60 + "\n")
    
    result = graph.invoke({
        "documents": documents,
        "analyses": [],
        "final_report": ""
    })
    
    print("\n" + result["final_report"])

if __name__ == "__main__":
    run_document_analyzer()
