# From: Zero to AI Agent, Chapter 17, Section 17.4
# Save as: exercise_2_17_4_solution.py
# Exercise 2: Multi-Format Translator

import operator
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

# Parent state schema
class ParentState(TypedDict):
    source_text: str
    source_lang: str
    target_langs: list[str]
    translations: Annotated[list[dict], operator.add]
    final_output: str

# Subgraph state schema (different from parent!)
class TranslationState(TypedDict):
    text: str
    from_lang: str
    to_lang: str
    result: str

# === SUBGRAPH: Single Translation ===

def build_translation_subgraph():
    """Subgraph that translates text to a single language."""
    
    def translate(state: TranslationState) -> dict:
        response = llm.invoke(
            f"Translate the following text from {state['from_lang']} to {state['to_lang']}.\n"
            f"Return only the translated text, nothing else.\n\n"
            f"Text: {state['text']}"
        )
        return {"result": response.content}
    
    graph = StateGraph(TranslationState)
    graph.add_node("translate", translate)
    graph.add_edge(START, "translate")
    graph.add_edge("translate", END)
    
    return graph.compile()

# Compile once
translation_subgraph = build_translation_subgraph()

# === WRAPPER: State Transformation ===

def call_translation_subgraph(state: dict) -> dict:
    """Wrapper that transforms state between parent and subgraph schemas.
    
    This is called for each parallel translation task.
    The state here is the Send payload (TranslationState-like).
    """
    # This receives the Send payload directly
    # Transform to subgraph state
    subgraph_input = {
        "text": state["text"],
        "from_lang": state["from_lang"],
        "to_lang": state["to_lang"],
        "result": ""
    }
    
    # Call subgraph
    subgraph_output = translation_subgraph.invoke(subgraph_input)
    
    # Transform back - return to parent's translations list
    return {"translations": [{
        "language": state["to_lang"],
        "text": subgraph_output["result"]
    }]}

# === PARENT GRAPH ===

def distribute_translations(state: ParentState) -> list[Send]:
    """Create parallel translation tasks for each target language."""
    return [
        Send("translate", {
            "text": state["source_text"],
            "from_lang": state["source_lang"],
            "to_lang": lang
        })
        for lang in state["target_langs"]
    ]

def compile_translations(state: ParentState) -> dict:
    """Compile all translations into final output."""
    output_parts = [
        f"📝 Original ({state['source_lang']}):",
        state["source_text"],
        "",
        "=" * 50,
        "🌍 Translations:",
        "=" * 50
    ]
    
    for t in state["translations"]:
        output_parts.append(f"\n📌 {t['language']}:")
        output_parts.append(t["text"])
    
    return {"final_output": "\n".join(output_parts)}

def build_translator_graph():
    """Build the parent translator graph."""
    
    graph = StateGraph(ParentState)
    
    # Dummy node to trigger distribution
    graph.add_node("start", lambda state: {})
    # Translation wrapper (called in parallel via Send)
    graph.add_node("translate", call_translation_subgraph)
    # Compile results
    graph.add_node("compile", compile_translations)
    
    graph.add_edge(START, "start")
    graph.add_conditional_edges(
        "start",
        distribute_translations,
        ["translate"]
    )
    graph.add_edge("translate", "compile")
    graph.add_edge("compile", END)
    
    return graph.compile()

def run_translator():
    graph = build_translator_graph()
    
    # Test translation
    result = graph.invoke({
        "source_text": "Artificial intelligence is transforming how we live and work. "
                       "The future holds amazing possibilities for human-AI collaboration.",
        "source_lang": "English",
        "target_langs": ["Spanish", "French", "German", "Japanese", "Chinese"],
        "translations": [],
        "final_output": ""
    })
    
    print("🌍 Multi-Format Translator")
    print("=" * 60)
    print(result["final_output"])
    print("\n" + "=" * 60)
    print(f"✅ Translated to {len(result['translations'])} languages in parallel!")

if __name__ == "__main__":
    run_translator()
