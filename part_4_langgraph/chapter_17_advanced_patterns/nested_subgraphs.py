# From: Zero to AI Agent, Chapter 17, Section 17.4
# Save as: nested_subgraphs.py

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

class DocumentState(TypedDict):
    document: str
    spell_checked: str
    grammar_fixed: str
    style_improved: str
    final_document: str

# Level 3 (deepest): Individual editing operations

def build_spell_checker():
    """Deepest level: spell checking."""
    
    def check_spelling(state: DocumentState) -> dict:
        response = llm.invoke(
            f"Fix any spelling errors in this text. Return only the corrected text:\n{state['document']}"
        )
        return {"spell_checked": response.content}
    
    graph = StateGraph(DocumentState)
    graph.add_node("spell", check_spelling)
    graph.add_edge(START, "spell")
    graph.add_edge("spell", END)
    return graph.compile()

def build_grammar_fixer():
    """Deepest level: grammar fixing."""
    
    def fix_grammar(state: DocumentState) -> dict:
        text = state.get("spell_checked") or state["document"]
        response = llm.invoke(
            f"Fix any grammar errors. Return only the corrected text:\n{text}"
        )
        return {"grammar_fixed": response.content}
    
    graph = StateGraph(DocumentState)
    graph.add_node("grammar", fix_grammar)
    graph.add_edge(START, "grammar")
    graph.add_edge("grammar", END)
    return graph.compile()

# Level 2: Editing subgraph that contains spell and grammar

def build_editing_subgraph():
    """Middle level: combines spell check and grammar fix."""
    
    spell_checker = build_spell_checker()
    grammar_fixer = build_grammar_fixer()
    
    editing = StateGraph(DocumentState)
    editing.add_node("spell", spell_checker)
    editing.add_node("grammar", grammar_fixer)
    
    editing.add_edge(START, "spell")
    editing.add_edge("spell", "grammar")
    editing.add_edge("grammar", END)
    
    return editing.compile()

# Level 1 (top): Full document processor

def build_document_processor():
    """Top level: full document processing pipeline."""
    
    editing_subgraph = build_editing_subgraph()
    
    def improve_style(state: DocumentState) -> dict:
        text = state.get("grammar_fixed") or state["document"]
        response = llm.invoke(
            f"Improve the writing style of this text. Make it clearer and more engaging:\n{text}"
        )
        return {"style_improved": response.content}
    
    def finalize(state: DocumentState) -> dict:
        return {"final_document": state["style_improved"]}
    
    processor = StateGraph(DocumentState)
    
    # Editing subgraph (which contains spell + grammar)
    processor.add_node("edit", editing_subgraph)
    processor.add_node("style", improve_style)
    processor.add_node("finalize", finalize)
    
    processor.add_edge(START, "edit")
    processor.add_edge("edit", "style")
    processor.add_edge("style", "finalize")
    processor.add_edge("finalize", END)
    
    return processor.compile()

def run_nested_example():
    graph = build_document_processor()
    
    messy_text = """
    Their going to the store becuase they need supplys.
    The weather is real nice today and me and him wants to go outside.
    """
    
    result = graph.invoke({
        "document": messy_text,
        "spell_checked": "",
        "grammar_fixed": "",
        "style_improved": "",
        "final_document": ""
    })
    
    print("📄 Nested Subgraph Document Processor")
    print("=" * 50)
    print(f"\n❌ Original:\n{messy_text}")
    print(f"\n✅ Final:\n{result['final_document']}")

if __name__ == "__main__":
    run_nested_example()
