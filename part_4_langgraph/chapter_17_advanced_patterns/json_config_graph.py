# From: Zero to AI Agent, Chapter 17, Section 17.5
# Save as: json_config_graph.py

import json
from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)

class FlexibleState(TypedDict):
    input_data: str
    results: Annotated[list[dict], operator.add]
    final_output: str

def create_llm_node(prompt_template: str, output_key: str):
    """Factory to create LLM-powered nodes from config."""
    
    def node_function(state: FlexibleState) -> dict:
        # Fill in the template with input data
        prompt = prompt_template.format(input=state["input_data"])
        response = llm.invoke(prompt)
        
        return {
            "results": [{
                "step": output_key,
                "output": response.content
            }]
        }
    
    return node_function

def create_transform_node(transform_type: str):
    """Factory to create transform nodes from config."""
    
    def node_function(state: FlexibleState) -> dict:
        text = state["input_data"]
        
        if transform_type == "uppercase":
            result = text.upper()
        elif transform_type == "lowercase":
            result = text.lower()
        elif transform_type == "word_count":
            result = f"Word count: {len(text.split())}"
        else:
            result = text
        
        return {
            "results": [{
                "step": transform_type,
                "output": result
            }]
        }
    
    return node_function

def build_from_json(config_json: str):
    """
    Build a graph from JSON configuration.
    
    JSON format:
    {
        "nodes": [
            {"name": "step1", "type": "llm", "prompt": "...", "output_key": "..."},
            {"name": "step2", "type": "transform", "transform": "uppercase"}
        ],
        "edges": [
            {"from": "START", "to": "step1"},
            {"from": "step1", "to": "step2"},
            {"from": "step2", "to": "END"}
        ]
    }
    """
    config = json.loads(config_json)
    
    graph = StateGraph(FlexibleState)
    
    # Create and add nodes
    for node_config in config["nodes"]:
        name = node_config["name"]
        node_type = node_config["type"]
        
        if node_type == "llm":
            node_fn = create_llm_node(
                node_config["prompt"],
                node_config.get("output_key", name)
            )
        elif node_type == "transform":
            node_fn = create_transform_node(node_config["transform"])
        else:
            raise ValueError(f"Unknown node type: {node_type}")
        
        graph.add_node(name, node_fn)
    
    # Add edges
    for edge in config["edges"]:
        from_node = edge["from"]
        to_node = edge["to"]
        
        if from_node == "START":
            graph.add_edge(START, to_node)
        elif to_node == "END":
            graph.add_edge(from_node, END)
        else:
            graph.add_edge(from_node, to_node)
    
    return graph.compile()

def test_json_config():
    # Define workflow as JSON
    config = json.dumps({
        "nodes": [
            {
                "name": "analyze",
                "type": "llm",
                "prompt": "Analyze the sentiment of this text: {input}",
                "output_key": "sentiment"
            },
            {
                "name": "extract",
                "type": "llm", 
                "prompt": "Extract 3 key topics from: {input}",
                "output_key": "topics"
            },
            {
                "name": "count",
                "type": "transform",
                "transform": "word_count"
            }
        ],
        "edges": [
            {"from": "START", "to": "analyze"},
            {"from": "START", "to": "extract"},
            {"from": "START", "to": "count"},
            {"from": "analyze", "to": "END"},
            {"from": "extract", "to": "END"},
            {"from": "count", "to": "END"}
        ]
    })
    
    print("📊 Graph Built from JSON Config")
    print("=" * 50)
    print("Config creates 3 parallel nodes!")
    
    graph = build_from_json(config)
    
    result = graph.invoke({
        "input_data": "The new AI product launch exceeded expectations. "
                      "Customers loved the intuitive interface and powerful features. "
                      "Sales grew 150% in the first quarter.",
        "results": [],
        "final_output": ""
    })
    
    print("\nResults:")
    for r in result["results"]:
        print(f"\n{r['step'].upper()}:")
        print(f"  {r['output']}")

if __name__ == "__main__":
    test_json_config()
