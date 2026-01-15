# From: Zero to AI Agent, Chapter 7, Section 7.4
# File: exercise_4_7_4_solution.py

"""
Exercise 4 Solution: Completion Control Experiment
Experiment with different parameters to control LLM output.
"""

import json
from typing import Dict, List, Any
from dataclasses import dataclass, asdict


@dataclass
class ExperimentResult:
    """Results from a parameter experiment."""
    temperature: float
    max_tokens: int
    stop_sequences: List[str]
    prompt: str
    output: str
    observations: List[str]
    metrics: Dict[str, Any]


def run_completion_experiments():
    """
    Run experiments with different completion control parameters.
    """
    
    print("=" * 70)
    print("EXERCISE 4: COMPLETION CONTROL EXPERIMENTS")
    print("=" * 70)
    
    # Base prompt for all experiments
    base_prompt = "Write a description of a mysterious forest. The forest"
    
    # Experiment 1: Temperature variations
    temperature_experiment(base_prompt)
    
    # Experiment 2: Max tokens variations
    max_tokens_experiment(base_prompt)
    
    # Experiment 3: Stop sequences
    stop_sequence_experiment(base_prompt)
    
    # Experiment 4: Combined parameters
    combined_parameters_experiment(base_prompt)
    
    # Analysis and insights
    show_parameter_insights()
    
    # Practical applications
    show_practical_applications()


def temperature_experiment(base_prompt: str):
    """Experiment with different temperature settings."""
    
    print(f"\n🌡️ EXPERIMENT 1: TEMPERATURE VARIATIONS")
    print("-" * 50)
    print(f"Base prompt: \"{base_prompt}\"")
    print("-" * 50)
    
    temperatures = [0.0, 0.5, 1.0, 1.5]
    
    results = []
    for temp in temperatures:
        result = ExperimentResult(
            temperature=temp,
            max_tokens=50,
            stop_sequences=[],
            prompt=base_prompt,
            output=simulate_completion(base_prompt, temp, 50, []),
            observations=analyze_temperature_output(temp),
            metrics=calculate_metrics(temp)
        )
        results.append(result)
    
    # Display results
    for result in results:
        print(f"\n📊 Temperature: {result.temperature}")
        print(f"Output: {result.output}")
        print("Observations:")
        for obs in result.observations:
            print(f"  • {obs}")
        print(f"Metrics: Creativity={result.metrics['creativity']}, "
              f"Coherence={result.metrics['coherence']}")
    
    print("\n🔍 TEMPERATURE INSIGHTS:")
    print("• T=0.0: Deterministic, same output every time, very predictable")
    print("• T=0.5: Slightly varied, maintains coherence, good for factual content")
    print("• T=1.0: Balanced creativity and coherence, good for general use")
    print("• T=1.5: Highly creative, may lose coherence, good for brainstorming")


def simulate_completion(prompt: str, temperature: float, 
                        max_tokens: int, stop_sequences: List[str]) -> str:
    """Simulate LLM completion with different parameters."""
    
    # Simulated outputs based on temperature
    outputs = {
        0.0: "is dark and dense with ancient trees. The tall pines block most sunlight, creating shadows everywhere. A narrow path winds through the undergrowth.",
        0.5: "holds ancient secrets within its shadowy depths. Twisted oaks and towering pines create a canopy so thick that daylight barely penetrates.",
        1.0: "whispers with voices of forgotten ages. Luminescent fungi paint ethereal patterns on bark while mist dances between gnarled roots that seem to breathe.",
        1.5: "dreams in colors that don't exist, where time flows backward and trees sing lullabies to sleeping dragons made of starlight and shadow."
    }
    
    output = outputs.get(temperature, outputs[1.0])
    
    # Apply max_tokens limit
    words = output.split()
    if max_tokens < 50:
        words = words[:max_tokens // 4]  # Rough token estimation
    output = " ".join(words)
    
    # Apply stop sequences
    for stop in stop_sequences:
        if stop in output:
            output = output.split(stop)[0] + stop
            break
    
    return output


def analyze_temperature_output(temperature: float) -> List[str]:
    """Analyze characteristics of output at different temperatures."""
    
    analyses = {
        0.0: [
            "Highly predictable word choices",
            "Conventional descriptions",
            "Consistent style",
            "Safe, expected imagery",
            "Suitable for technical documentation"
        ],
        0.5: [
            "Some variety in word choice",
            "Mostly conventional with occasional surprises",
            "Good balance of consistency",
            "Clear and coherent",
            "Suitable for professional content"
        ],
        1.0: [
            "Creative word combinations",
            "Mix of expected and unexpected",
            "Natural flow with variety",
            "Engaging imagery",
            "Suitable for creative writing"
        ],
        1.5: [
            "Highly unpredictable",
            "Unusual word combinations",
            "May include surreal elements",
            "Risk of incoherence",
            "Suitable for brainstorming only"
        ]
    }
    
    return analyses.get(temperature, analyses[1.0])


def calculate_metrics(temperature: float) -> Dict[str, Any]:
    """Calculate metrics for different parameter settings."""
    
    # Simulated metrics
    creativity = min(10, temperature * 6.67)  # 0-10 scale
    coherence = max(0, 10 - temperature * 5)  # 0-10 scale
    predictability = max(0, 10 - temperature * 6.67)  # 0-10 scale
    
    return {
        "creativity": round(creativity, 1),
        "coherence": round(coherence, 1),
        "predictability": round(predictability, 1)
    }


def max_tokens_experiment(base_prompt: str):
    """Experiment with different max_tokens settings."""
    
    print(f"\n📏 EXPERIMENT 2: MAX_TOKENS VARIATIONS")
    print("-" * 50)
    
    token_limits = [50, 200, 500]
    
    for limit in token_limits:
        print(f"\n🎯 Max Tokens: {limit}")
        
        # Estimate output characteristics
        if limit == 50:
            print("Output: Short, ~2-3 sentences")
            print("Use case: Quick summaries, brief responses")
            print("Cost: Minimal")
            print("Speed: Very fast")
        elif limit == 200:
            print("Output: Medium, ~1 paragraph")
            print("Use case: Standard responses, explanations")
            print("Cost: Moderate")
            print("Speed: Fast")
        else:  # 500
            print("Output: Long, ~2-3 paragraphs")
            print("Use case: Detailed explanations, stories")
            print("Cost: Higher")
            print("Speed: Slower")
        
        print("Considerations:")
        print(f"  • Response may end mid-sentence if limit reached")
        print(f"  • Actual tokens ≠ words (roughly 1 token = 0.75 words)")
        print(f"  • Include buffer for unexpected verbosity")


def stop_sequence_experiment(base_prompt: str):
    """Experiment with different stop sequences."""
    
    print(f"\n🛑 EXPERIMENT 3: STOP SEQUENCES")
    print("-" * 50)
    
    stop_configs = [
        {
            "sequences": [],
            "description": "No stop sequences",
            "output": "continues until max_tokens or natural end",
            "use_case": "Free-form generation"
        },
        {
            "sequences": ["\n"],
            "description": "Stop at newline",
            "output": "single line/paragraph only",
            "use_case": "Single-line responses, titles"
        },
        {
            "sequences": [".", "!", "?"],
            "description": "Stop at sentence end",
            "output": "exactly one sentence",
            "use_case": "Concise responses, definitions"
        },
        {
            "sequences": ["END", "---"],
            "description": "Custom markers",
            "output": "continues until marker",
            "use_case": "Structured templates, forms"
        },
        {
            "sequences": ["</answer>"],
            "description": "XML-style tags",
            "output": "structured response sections",
            "use_case": "Parsing specific content"
        }
    ]
    
    for config in stop_configs:
        print(f"\n📍 Stop Sequences: {config['sequences'] if config['sequences'] else 'None'}")
        print(f"   Description: {config['description']}")
        print(f"   Behavior: {config['output']}")
        print(f"   Use Case: {config['use_case']}")
    
    print("\n💡 STOP SEQUENCE TIPS:")
    print("• Order matters - first match wins")
    print("• Include the stop sequence in output")
    print("• Use unique markers to avoid premature stops")
    print("• Test with your specific content type")


def combined_parameters_experiment(base_prompt: str):
    """Experiment with combined parameter effects."""
    
    print(f"\n🎨 EXPERIMENT 4: COMBINED PARAMETERS")
    print("-" * 50)
    
    combinations = [
        {
            "name": "Factual Assistant",
            "temperature": 0.1,
            "max_tokens": 150,
            "stop_sequences": ["\n\n"],
            "use_case": "Technical documentation, facts",
            "characteristics": ["Precise", "Consistent", "Brief", "Structured"]
        },
        {
            "name": "Creative Writer",
            "temperature": 0.9,
            "max_tokens": 500,
            "stop_sequences": ["THE END"],
            "use_case": "Stories, creative content",
            "characteristics": ["Imaginative", "Varied", "Flowing", "Expansive"]
        },
        {
            "name": "Chatbot",
            "temperature": 0.7,
            "max_tokens": 200,
            "stop_sequences": [],
            "use_case": "Conversational AI",
            "characteristics": ["Natural", "Balanced", "Responsive", "Friendly"]
        },
        {
            "name": "Code Generator",
            "temperature": 0.2,
            "max_tokens": 300,
            "stop_sequences": ["```", "# End"],
            "use_case": "Programming assistance",
            "characteristics": ["Syntactically correct", "Functional", "Complete", "Commented"]
        },
        {
            "name": "Brainstorming Bot",
            "temperature": 1.2,
            "max_tokens": 100,
            "stop_sequences": [],
            "use_case": "Idea generation",
            "characteristics": ["Wild", "Unexpected", "Brief bursts", "Provocative"]
        }
    ]
    
    for combo in combinations:
        print(f"\n🎯 {combo['name']}")
        print(f"   Temperature: {combo['temperature']}")
        print(f"   Max Tokens: {combo['max_tokens']}")
        print(f"   Stop Sequences: {combo['stop_sequences']}")
        print(f"   Use Case: {combo['use_case']}")
        print(f"   Characteristics: {', '.join(combo['characteristics'])}")


def show_parameter_insights():
    """Show key insights about parameter interactions."""
    
    print("\n" + "="*70)
    print("PARAMETER INTERACTION INSIGHTS")
    print("="*70)
    
    insights = [
        {
            "observation": "Temperature vs Max Tokens",
            "insight": "High temperature needs more tokens to develop creative ideas fully",
            "recommendation": "If temp > 1.0, use max_tokens > 200"
        },
        {
            "observation": "Stop Sequences vs Temperature",
            "insight": "High temperature may generate stop sequences unexpectedly",
            "recommendation": "Use unique stop sequences with high temperature"
        },
        {
            "observation": "Task vs Parameters",
            "insight": "Match parameters to task requirements, not preferences",
            "recommendation": "Create parameter presets for common tasks"
        },
        {
            "observation": "Cost vs Quality",
            "insight": "Lower temperature often needs fewer tokens for good results",
            "recommendation": "Start with temp=0.3-0.5 for cost optimization"
        },
        {
            "observation": "Consistency vs Variety",
            "insight": "Production systems need predictability, creative tasks need variety",
            "recommendation": "Use temp<0.3 for production, temp>0.7 for creative"
        }
    ]
    
    for item in insights:
        print(f"\n🔍 {item['observation']}")
        print(f"   Insight: {item['insight']}")
        print(f"   📝 Recommendation: {item['recommendation']}")


def show_practical_applications():
    """Show practical applications of parameter control."""
    
    print("\n" + "="*70)
    print("PRACTICAL APPLICATIONS")
    print("="*70)
    
    applications = [
        {
            "scenario": "Customer Service Bot",
            "config": "temp=0.3, max_tokens=150, stop=['\nCustomer:', '\nAgent:']",
            "why": "Consistent, professional, controlled length"
        },
        {
            "scenario": "Blog Post Generator",
            "config": "temp=0.7, max_tokens=800, stop=['</article>']",
            "why": "Creative but coherent, full length allowed"
        },
        {
            "scenario": "Data Extraction",
            "config": "temp=0.0, max_tokens=100, stop=['\\n', ',']",
            "why": "Deterministic parsing, structured output"
        },
        {
            "scenario": "Code Documentation",
            "config": "temp=0.2, max_tokens=200, stop=['```', '\"\"\"']",
            "why": "Accurate, concise, properly formatted"
        },
        {
            "scenario": "Story Writing",
            "config": "temp=0.9, max_tokens=1000, stop=['THE END']",
            "why": "Creative freedom with defined ending"
        }
    ]
    
    for app in applications:
        print(f"\n📱 {app['scenario']}")
        print(f"   Config: {app['config']}")
        print(f"   Why: {app['why']}")


def create_parameter_testing_framework():
    """Create a framework for systematic parameter testing."""
    
    print("\n" + "="*70)
    print("PARAMETER TESTING FRAMEWORK")
    print("="*70)
    
    code = '''
class ParameterTester:
    """Framework for systematic LLM parameter testing."""
    
    def __init__(self, base_prompt: str):
        self.base_prompt = base_prompt
        self.results = []
    
    def test_temperature_range(self, temps: List[float], 
                               fixed_tokens: int = 100):
        """Test across temperature range."""
        for temp in temps:
            output = llm_call(
                prompt=self.base_prompt,
                temperature=temp,
                max_tokens=fixed_tokens
            )
            self.results.append({
                "temperature": temp,
                "output": output,
                "word_count": len(output.split()),
                "unique_words": len(set(output.split()))
            })
    
    def test_token_limits(self, limits: List[int], 
                         fixed_temp: float = 0.7):
        """Test different token limits."""
        for limit in limits:
            output = llm_call(
                prompt=self.base_prompt,
                temperature=fixed_temp,
                max_tokens=limit
            )
            self.results.append({
                "max_tokens": limit,
                "output": output,
                "actual_length": len(output),
                "truncated": not output.endswith(('.', '!', '?'))
            })
    
    def analyze_results(self) -> Dict:
        """Analyze test results."""
        return {
            "total_tests": len(self.results),
            "avg_length": sum(len(r["output"]) for r in self.results) / len(self.results),
            "variety_score": self.calculate_variety(),
            "optimal_settings": self.find_optimal()
        }
    
    def export_results(self, filename: str):
        """Export results for analysis."""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)

# Usage
tester = ParameterTester("Write about artificial intelligence")
tester.test_temperature_range([0, 0.3, 0.5, 0.7, 1.0, 1.3])
tester.test_token_limits([50, 100, 200, 500])
analysis = tester.analyze_results()
    '''
    
    print("IMPLEMENTATION:")
    print(code)


def main():
    """Run completion control experiments."""
    
    # Run experiments
    run_completion_experiments()
    
    # Testing framework
    create_parameter_testing_framework()
    
    print("\n" + "="*70)
    print("EXERCISE 4 COMPLETE")
    print("="*70)
    print("\n✅ You now understand how parameters control LLM output!")
    print("   Remember: Test systematically, document results, create presets!")


if __name__ == "__main__":
    main()
