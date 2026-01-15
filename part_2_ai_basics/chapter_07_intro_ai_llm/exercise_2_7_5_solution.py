# From: Zero to AI Agent, Chapter 7, Section 7.5
# File: exercise_2_7_5_solution.py

"""
Exercise 2 Solution: Provider Comparison Matrix
Build a comparison matrix for your specific use case.
"""

import pandas as pd
from typing import Dict, List
from dataclasses import dataclass
import json


@dataclass
class ProviderEvaluation:
    """Evaluation of a provider for specific use case."""
    provider: str
    cost_score: float  # 1-10, 10 being cheapest
    performance_score: float  # 1-10, 10 being best
    features_score: float  # 1-10, 10 being most features
    limitations_score: float  # 1-10, 10 being least limitations
    overall_score: float  # Weighted average


def create_provider_comparison_matrix():
    """Create comprehensive provider comparison matrix."""
    
    print("=" * 70)
    print("EXERCISE 2: PROVIDER COMPARISON MATRIX")
    print("=" * 70)
    
    # Define use cases
    use_cases = [
        "Customer Service Chatbot",
        "Code Generation Assistant",
        "Content Writing Platform",
        "Data Analysis Tool",
        "Educational Tutor"
    ]
    
    for use_case in use_cases:
        print(f"\n📊 USE CASE: {use_case}")
        print("-" * 50)
        
        # Create comparison for this use case
        comparison = create_use_case_comparison(use_case)
        display_comparison_matrix(comparison)
        
        # Provide recommendations
        provide_recommendations(use_case, comparison)


def create_use_case_comparison(use_case: str) -> Dict:
    """Create detailed comparison for specific use case."""
    
    providers_data = {
        "OpenAI": {
            "models": ["GPT-3.5-Turbo", "GPT-4", "GPT-4-Turbo"],
            "cost": get_cost_rating(use_case, "OpenAI"),
            "performance": get_performance_rating(use_case, "OpenAI"),
            "features": {
                "function_calling": True,
                "json_mode": True,
                "vision": True,
                "streaming": True,
                "fine_tuning": True,
                "embeddings": True
            },
            "limitations": {
                "rate_limits": "Medium",
                "context_window": "16K-128K",
                "data_privacy": "Standard",
                "geographic_restrictions": "Some countries blocked"
            }
        },
        "Anthropic": {
            "models": ["Claude-3-Haiku", "Claude-3-Sonnet", "Claude-3-Opus"],
            "cost": get_cost_rating(use_case, "Anthropic"),
            "performance": get_performance_rating(use_case, "Anthropic"),
            "features": {
                "function_calling": False,
                "json_mode": False,
                "vision": True,
                "streaming": True,
                "fine_tuning": False,
                "embeddings": False
            },
            "limitations": {
                "rate_limits": "Low",
                "context_window": "200K",
                "data_privacy": "Enhanced",
                "geographic_restrictions": "Limited availability"
            }
        },
        "Google": {
            "models": ["Gemini-Pro", "Gemini-Ultra", "Gemini-Nano"],
            "cost": get_cost_rating(use_case, "Google"),
            "performance": get_performance_rating(use_case, "Google"),
            "features": {
                "function_calling": True,
                "json_mode": True,
                "vision": True,
                "streaming": True,
                "fine_tuning": False,
                "embeddings": True
            },
            "limitations": {
                "rate_limits": "High (free tier)",
                "context_window": "32K-1M",
                "data_privacy": "Google standard",
                "geographic_restrictions": "Wide availability"
            }
        },
        "Open Source": {
            "models": ["Llama-2", "Mistral", "Mixtral"],
            "cost": get_cost_rating(use_case, "Open Source"),
            "performance": get_performance_rating(use_case, "Open Source"),
            "features": {
                "function_calling": "Depends",
                "json_mode": "Depends",
                "vision": "Limited",
                "streaming": True,
                "fine_tuning": True,
                "embeddings": True
            },
            "limitations": {
                "rate_limits": "None (self-hosted)",
                "context_window": "4K-32K",
                "data_privacy": "Full control",
                "geographic_restrictions": "None"
            }
        }
    }
    
    return providers_data


def get_cost_rating(use_case: str, provider: str) -> Dict:
    """Get cost ratings for specific use case and provider."""
    
    # Cost ratings matrix (simplified)
    cost_matrix = {
        "Customer Service Chatbot": {
            "OpenAI": 7,  # GPT-3.5 is cost-effective
            "Anthropic": 8,  # Haiku is very cheap
            "Google": 9,  # Gemini Pro has good free tier
            "Open Source": 10  # Self-hosting after initial setup
        },
        "Code Generation Assistant": {
            "OpenAI": 6,  # GPT-4 needed, expensive
            "Anthropic": 5,  # Opus needed, expensive
            "Google": 7,  # Gemini Pro decent
            "Open Source": 8  # Good open models available
        },
        "Content Writing Platform": {
            "OpenAI": 7,
            "Anthropic": 7,
            "Google": 8,
            "Open Source": 6
        },
        "Data Analysis Tool": {
            "OpenAI": 6,
            "Anthropic": 6,
            "Google": 7,
            "Open Source": 5
        },
        "Educational Tutor": {
            "OpenAI": 7,
            "Anthropic": 8,
            "Google": 8,
            "Open Source": 7
        }
    }
    
    return cost_matrix.get(use_case, {}).get(provider, 5)


def get_performance_rating(use_case: str, provider: str) -> Dict:
    """Get performance ratings for specific use case and provider."""
    
    performance_matrix = {
        "Customer Service Chatbot": {
            "OpenAI": 9,
            "Anthropic": 9,
            "Google": 8,
            "Open Source": 7
        },
        "Code Generation Assistant": {
            "OpenAI": 10,  # GPT-4 excels
            "Anthropic": 9,  # Claude very good
            "Google": 8,
            "Open Source": 7
        },
        "Content Writing Platform": {
            "OpenAI": 9,
            "Anthropic": 10,  # Claude excels at writing
            "Google": 8,
            "Open Source": 7
        },
        "Data Analysis Tool": {
            "OpenAI": 9,
            "Anthropic": 8,
            "Google": 8,
            "Open Source": 6
        },
        "Educational Tutor": {
            "OpenAI": 9,
            "Anthropic": 10,  # Claude great at explanations
            "Google": 8,
            "Open Source": 7
        }
    }
    
    return performance_matrix.get(use_case, {}).get(provider, 5)


def display_comparison_matrix(providers_data: Dict):
    """Display comparison matrix in readable format."""
    
    # Create summary scores
    summary = []
    
    for provider, data in providers_data.items():
        # Count features
        features_count = sum(1 for v in data["features"].values() 
                           if v is True or v == "Depends")
        
        # Calculate limitation score (inverse)
        limitation_factors = {
            "rate_limits": {"Low": 3, "Medium": 5, "High": 8, "None": 10},
            "context_window": {"4K-32K": 5, "16K-128K": 7, "32K-1M": 9, "200K": 10},
            "data_privacy": {"Standard": 5, "Enhanced": 8, "Google standard": 6, "Full control": 10}
        }
        
        limitation_score = 7  # Default
        
        summary.append({
            "Provider": provider,
            "Cost (1-10)": data["cost"],
            "Performance (1-10)": data["performance"],
            "Features": f"{features_count}/6",
            "Best Model": data["models"][0] if data["models"] else "N/A",
            "Key Advantage": get_key_advantage(provider)
        })
    
    # Display as table
    for row in summary:
        print(f"\n{row['Provider']}:")
        for key, value in row.items():
            if key != "Provider":
                print(f"  {key}: {value}")


def get_key_advantage(provider: str) -> str:
    """Get key advantage for each provider."""
    
    advantages = {
        "OpenAI": "Most mature ecosystem, best tooling",
        "Anthropic": "Longest context, best safety",
        "Google": "Great free tier, multimodal",
        "Open Source": "Full control, no restrictions"
    }
    
    return advantages.get(provider, "N/A")


def provide_recommendations(use_case: str, providers_data: Dict):
    """Provide specific recommendations for use case."""
    
    print(f"\n💡 RECOMMENDATIONS FOR {use_case}:")
    print("-" * 40)
    
    recommendations = {
        "Customer Service Chatbot": [
            "Start with: Google Gemini Pro (free tier)",
            "Scale to: OpenAI GPT-3.5-Turbo",
            "Enterprise: Anthropic Claude-3-Haiku",
            "Self-hosted: Llama-2-13B-Chat"
        ],
        "Code Generation Assistant": [
            "Best quality: OpenAI GPT-4",
            "Cost-effective: Anthropic Claude-3-Sonnet",
            "Free option: Google Gemini Pro",
            "Open source: Mixtral-8x7B-Instruct"
        ],
        "Content Writing Platform": [
            "Best quality: Anthropic Claude-3-Opus",
            "Balanced: OpenAI GPT-4-Turbo",
            "Budget: Google Gemini Pro",
            "Open source: Mistral-7B-Instruct"
        ],
        "Data Analysis Tool": [
            "Best: OpenAI GPT-4 (function calling)",
            "Alternative: Google Gemini Pro",
            "Budget: OpenAI GPT-3.5-Turbo",
            "Open source: CodeLlama-13B"
        ],
        "Educational Tutor": [
            "Best: Anthropic Claude (safe, detailed)",
            "Alternative: OpenAI GPT-4",
            "Budget: Google Gemini Pro",
            "Open source: Llama-2-70B-Chat"
        ]
    }
    
    for rec in recommendations.get(use_case, []):
        print(f"  • {rec}")


def create_detailed_comparison_framework():
    """Create detailed comparison framework code."""
    
    print("\n" + "=" * 70)
    print("DETAILED COMPARISON FRAMEWORK")
    print("=" * 70)
    
    code = '''
class ProviderComparator:
    """Comprehensive provider comparison framework."""
    
    def __init__(self, use_case: Dict):
        self.use_case = use_case
        self.weights = use_case.get("weights", {
            "cost": 0.3,
            "performance": 0.3,
            "features": 0.2,
            "limitations": 0.2
        })
        self.providers = {}
    
    def add_provider(self, name: str, config: Dict):
        """Add provider to comparison."""
        self.providers[name] = {
            "config": config,
            "scores": self.calculate_scores(config)
        }
    
    def calculate_scores(self, config: Dict) -> Dict:
        """Calculate scores for provider."""
        scores = {}
        
        # Cost score (based on per-token pricing)
        avg_cost = (config["input_cost"] + config["output_cost"]) / 2
        scores["cost"] = 10 * (1 / (1 + avg_cost * 100))  # Inverse cost
        
        # Performance score (based on benchmarks)
        scores["performance"] = config.get("benchmark_score", 5)
        
        # Features score
        feature_count = len([f for f in config.get("features", []) if f])
        scores["features"] = min(10, feature_count * 2)
        
        # Limitations score
        limitation_count = len(config.get("limitations", []))
        scores["limitations"] = max(0, 10 - limitation_count * 2)
        
        # Overall weighted score
        scores["overall"] = sum(
            scores[key] * self.weights.get(key, 0.25)
            for key in ["cost", "performance", "features", "limitations"]
        )
        
        return scores
    
    def compare(self) -> pd.DataFrame:
        """Generate comparison dataframe."""
        data = []
        
        for name, provider in self.providers.items():
            row = {"Provider": name}
            row.update(provider["scores"])
            data.append(row)
        
        df = pd.DataFrame(data)
        return df.sort_values("overall", ascending=False)
    
    def recommend(self, constraints: Dict = None) -> str:
        """Recommend best provider given constraints."""
        filtered = self.providers.copy()
        
        if constraints:
            if "max_cost" in constraints:
                filtered = {k: v for k, v in filtered.items()
                           if v["config"]["avg_cost"] <= constraints["max_cost"]}
            
            if "min_performance" in constraints:
                filtered = {k: v for k, v in filtered.items()
                           if v["scores"]["performance"] >= constraints["min_performance"]}
            
            if "required_features" in constraints:
                for feature in constraints["required_features"]:
                    filtered = {k: v for k, v in filtered.items()
                               if feature in v["config"].get("features", [])}
        
        if not filtered:
            return "No providers match your constraints"
        
        # Return provider with highest overall score
        best = max(filtered.items(), key=lambda x: x[1]["scores"]["overall"])
        return best[0]

# Usage Example
comparator = ProviderComparator({
    "name": "Customer Service Bot",
    "weights": {
        "cost": 0.4,  # Cost is most important
        "performance": 0.3,
        "features": 0.2,
        "limitations": 0.1
    }
})

comparator.add_provider("OpenAI", {
    "input_cost": 0.0005,
    "output_cost": 0.0015,
    "benchmark_score": 9,
    "features": ["streaming", "function_calling", "json_mode"],
    "limitations": ["rate_limits"]
})

comparator.add_provider("Anthropic", {
    "input_cost": 0.00025,
    "output_cost": 0.00125,
    "benchmark_score": 9,
    "features": ["streaming", "long_context"],
    "limitations": ["no_function_calling", "limited_availability"]
})

df = comparator.compare()
print(df)

best = comparator.recommend(constraints={"max_cost": 0.001})
print(f"Recommended: {best}")
    '''
    
    print(code)


def main():
    """Run provider comparison exercise."""
    
    # Create comparison matrices
    create_provider_comparison_matrix()
    
    # Detailed framework
    create_detailed_comparison_framework()
    
    print("\n" + "=" * 70)
    print("EXERCISE 2 COMPLETE")
    print("=" * 70)
    print("\n✅ You can now compare providers systematically for any use case!")


if __name__ == "__main__":
    main()
