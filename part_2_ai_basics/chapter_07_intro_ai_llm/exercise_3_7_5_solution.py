# From: Zero to AI Agent, Chapter 7, Section 7.5
# File: exercise_3_7_5_solution.py

"""
Exercise 3 Solution: Migration Planning
Design a migration plan from OpenAI to an open-source model.
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class MigrationPhase:
    """A phase in the migration plan."""
    name: str
    duration: int  # days
    tasks: List[str]
    risks: List[str]
    success_criteria: List[str]
    rollback_plan: str


def create_migration_plan():
    """Create comprehensive migration plan from OpenAI to open-source."""
    
    print("=" * 70)
    print("EXERCISE 3: MIGRATION PLANNING")
    print("=" * 70)
    print("Migration: OpenAI GPT → Open Source LLM (Llama-2/Mistral)")
    print("=" * 70)
    
    # Define migration phases
    phases = create_migration_phases()
    
    # Display migration timeline
    display_migration_timeline(phases)
    
    # Identify challenges
    identify_migration_challenges()
    
    # Create mitigation strategies
    create_mitigation_strategies()
    
    # Provide migration checklist
    provide_migration_checklist()
    
    # Show code migration examples
    show_code_migration_examples()


def create_migration_phases() -> List[MigrationPhase]:
    """Define migration phases."""
    
    phases = [
        MigrationPhase(
            name="Phase 1: Assessment & Planning",
            duration=14,
            tasks=[
                "Audit current OpenAI usage patterns",
                "Document all API endpoints and features used",
                "Measure baseline performance metrics",
                "Evaluate open-source alternatives",
                "Select target model (Llama-2, Mistral, etc.)",
                "Estimate infrastructure requirements",
                "Calculate ROI and cost savings"
            ],
            risks=[
                "Underestimating complexity",
                "Missing critical features",
                "Incomplete usage audit"
            ],
            success_criteria=[
                "Complete API usage documentation",
                "Model selection justified with benchmarks",
                "Infrastructure requirements defined",
                "Budget approved"
            ],
            rollback_plan="Continue with OpenAI while re-evaluating"
        ),
        
        MigrationPhase(
            name="Phase 2: Infrastructure Setup",
            duration=21,
            tasks=[
                "Provision GPU servers or cloud instances",
                "Install model serving framework (vLLM, TGI, etc.)",
                "Deploy selected open-source model",
                "Setup monitoring and logging",
                "Configure load balancing",
                "Implement security measures",
                "Setup backup and recovery"
            ],
            risks=[
                "Hardware compatibility issues",
                "Insufficient compute resources",
                "Security vulnerabilities",
                "Complex deployment"
            ],
            success_criteria=[
                "Model successfully deployed",
                "Response times < 2 seconds",
                "99.9% uptime achieved in testing",
                "Security audit passed"
            ],
            rollback_plan="Maintain OpenAI as primary, use open-source as backup"
        ),
        
        MigrationPhase(
            name="Phase 3: Feature Parity Development",
            duration=30,
            tasks=[
                "Implement prompt translation layer",
                "Recreate function calling if needed",
                "Build response formatting modules",
                "Develop quality assurance tests",
                "Create performance benchmarks",
                "Build fallback mechanisms",
                "Implement caching layer"
            ],
            risks=[
                "Feature gaps discovered",
                "Quality degradation",
                "Performance issues",
                "Increased complexity"
            ],
            success_criteria=[
                "All critical features replicated",
                "Quality metrics within 10% of OpenAI",
                "Automated testing suite complete",
                "Fallback system operational"
            ],
            rollback_plan="Keep OpenAI for features that can't be replicated"
        ),
        
        MigrationPhase(
            name="Phase 4: Parallel Testing",
            duration=30,
            tasks=[
                "Run A/B tests with real traffic",
                "Compare outputs systematically",
                "Measure user satisfaction",
                "Monitor system performance",
                "Collect edge cases",
                "Tune model parameters",
                "Optimize infrastructure"
            ],
            risks=[
                "User experience degradation",
                "Unexpected edge cases",
                "Performance bottlenecks",
                "Higher error rates"
            ],
            success_criteria=[
                "95% output quality parity",
                "Response time within 150% of OpenAI",
                "Error rate < 2%",
                "Positive user feedback"
            ],
            rollback_plan="Route traffic back to OpenAI if issues arise"
        ),
        
        MigrationPhase(
            name="Phase 5: Gradual Migration",
            duration=21,
            tasks=[
                "Start with 10% traffic migration",
                "Monitor all metrics closely",
                "Gradually increase to 50%",
                "Address issues as they arise",
                "Train team on new system",
                "Update documentation",
                "Prepare full cutover"
            ],
            risks=[
                "Scaling issues",
                "Team resistance",
                "Documentation gaps",
                "Customer complaints"
            ],
            success_criteria=[
                "50% traffic on open-source",
                "SLA requirements met",
                "Team fully trained",
                "Documentation complete"
            ],
            rollback_plan="Reduce traffic percentage, fix issues, retry"
        ),
        
        MigrationPhase(
            name="Phase 6: Full Migration & Optimization",
            duration=14,
            tasks=[
                "Complete traffic migration",
                "Decommission OpenAI integration",
                "Optimize resource usage",
                "Implement cost tracking",
                "Setup continuous improvement",
                "Celebrate success! 🎉"
            ],
            risks=[
                "Premature decommissioning",
                "Optimization breaking functionality",
                "Team burnout"
            ],
            success_criteria=[
                "100% traffic on open-source",
                "Cost savings realized",
                "Team satisfaction high",
                "System stable for 2 weeks"
            ],
            rollback_plan="Emergency OpenAI API keys ready if critical issues"
        )
    ]
    
    return phases


def display_migration_timeline(phases: List[MigrationPhase]):
    """Display migration timeline."""
    
    print("\n📅 MIGRATION TIMELINE")
    print("-" * 50)
    
    total_days = sum(phase.duration for phase in phases)
    print(f"Total Duration: {total_days} days (~{total_days // 30} months)")
    print()
    
    start_date = datetime.now()
    
    for i, phase in enumerate(phases, 1):
        end_date = start_date + timedelta(days=phase.duration)
        print(f"📍 {phase.name}")
        print(f"   Duration: {phase.duration} days")
        print(f"   Start: {start_date.strftime('%Y-%m-%d')}")
        print(f"   End: {end_date.strftime('%Y-%m-%d')}")
        print(f"   Key Tasks: {len(phase.tasks)} tasks")
        print()
        start_date = end_date


def identify_migration_challenges():
    """Identify key migration challenges."""
    
    print("\n⚠️ KEY MIGRATION CHALLENGES")
    print("-" * 50)
    
    challenges = {
        "Technical Challenges": [
            "Prompt compatibility - OpenAI prompts may not work",
            "Feature gaps - No native function calling",
            "Performance differences - May be slower",
            "Context window limitations - Often smaller",
            "Output quality variance - Less consistent"
        ],
        "Infrastructure Challenges": [
            "GPU requirements - Expensive hardware needed",
            "Scaling complexity - Manual scaling required",
            "Monitoring gaps - Less mature tooling",
            "Security responsibility - You own security now",
            "Deployment complexity - More moving parts"
        ],
        "Organizational Challenges": [
            "Team training required - New skills needed",
            "Support burden - No vendor support",
            "Documentation needs - Must create your own",
            "Change resistance - Team may prefer OpenAI",
            "Risk tolerance - Management concerns"
        ],
        "Cost Challenges": [
            "Upfront investment - Hardware/cloud costs",
            "Hidden costs - DevOps, monitoring, maintenance",
            "Opportunity cost - Engineering time",
            "Training costs - Team education",
            "Dual running costs - During migration"
        ]
    }
    
    for category, items in challenges.items():
        print(f"\n{category}:")
        for item in items:
            print(f"  • {item}")


def create_mitigation_strategies():
    """Create strategies to handle migration challenges."""
    
    print("\n💡 MITIGATION STRATEGIES")
    print("-" * 50)
    
    strategies = [
        {
            "challenge": "Prompt Compatibility",
            "strategy": "Build prompt translation layer",
            "implementation": """
# Prompt translator example
def translate_prompt(openai_prompt: str) -> str:
    # OpenAI system prompts → Llama format
    if "You are" in openai_prompt:
        return f"<s>[INST] <<SYS>>\\n{openai_prompt}\\n<</SYS>>\\n[/INST]"
    return openai_prompt
            """
        },
        {
            "challenge": "Feature Gaps",
            "strategy": "Implement missing features externally",
            "implementation": """
# Function calling wrapper
def function_calling_wrapper(prompt: str, functions: List):
    # Add function descriptions to prompt
    enhanced_prompt = f"{prompt}\\n\\nAvailable functions: {functions}"
    response = llm_call(enhanced_prompt)
    # Parse response for function calls
    return parse_function_calls(response)
            """
        },
        {
            "challenge": "Performance Issues",
            "strategy": "Implement caching and optimization",
            "implementation": """
# Performance optimization
class OptimizedLLM:
    def __init__(self):
        self.cache = {}
        self.batch_queue = []
    
    def cached_inference(self, prompt: str):
        if prompt in self.cache:
            return self.cache[prompt]
        response = self.llm_call(prompt)
        self.cache[prompt] = response
        return response
            """
        },
        {
            "challenge": "Quality Variance",
            "strategy": "Implement quality assurance layer",
            "implementation": """
# Quality assurance
def quality_check(response: str, expected_quality: float = 0.8):
    score = calculate_quality_score(response)
    if score < expected_quality:
        # Retry with different parameters or fallback
        return retry_with_adjustments(response)
    return response
            """
        }
    ]
    
    for s in strategies:
        print(f"\n🎯 Challenge: {s['challenge']}")
        print(f"   Strategy: {s['strategy']}")
        print(f"   Implementation:")
        print(s['implementation'])


def provide_migration_checklist():
    """Provide comprehensive migration checklist."""
    
    print("\n✅ MIGRATION CHECKLIST")
    print("-" * 50)
    
    checklist = {
        "Pre-Migration": [
            "□ Complete API usage audit",
            "□ Document all prompts and patterns",
            "□ Benchmark current performance",
            "□ Calculate expected cost savings",
            "□ Get stakeholder buy-in",
            "□ Select target model",
            "□ Plan infrastructure",
            "□ Create rollback plan"
        ],
        "During Migration": [
            "□ Setup monitoring dashboards",
            "□ Implement A/B testing",
            "□ Create prompt translation",
            "□ Build quality checks",
            "□ Train the team",
            "□ Document everything",
            "□ Maintain OpenAI backup",
            "□ Collect user feedback"
        ],
        "Post-Migration": [
            "□ Monitor performance metrics",
            "□ Track cost savings",
            "□ Optimize resource usage",
            "□ Update documentation",
            "□ Plan improvements",
            "□ Share learnings",
            "□ Celebrate success!",
            "□ Plan next optimizations"
        ]
    }
    
    for phase, items in checklist.items():
        print(f"\n{phase}:")
        for item in items:
            print(f"  {item}")


def show_code_migration_examples():
    """Show actual code migration examples."""
    
    print("\n💻 CODE MIGRATION EXAMPLES")
    print("-" * 50)
    
    print("\n1️⃣ OPENAI → OPEN SOURCE API WRAPPER:")
    
    code_example = '''
class LLMProvider:
    """Unified interface for different LLM providers."""
    
    def __init__(self, provider: str = "openai"):
        self.provider = provider
        
        if provider == "openai":
            import openai
            self.client = openai.OpenAI()
        elif provider == "llama":
            from llama_cpp import Llama
            self.client = Llama(model_path="./models/llama-2-7b.gguf")
        elif provider == "vllm":
            from vllm import LLM
            self.client = LLM(model="meta-llama/Llama-2-7b-hf")
    
    def complete(self, prompt: str, **kwargs) -> str:
        """Unified completion interface."""
        
        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return response.choices[0].message.content
            
        elif self.provider == "llama":
            response = self.client(
                prompt,
                max_tokens=kwargs.get("max_tokens", 512),
                temperature=kwargs.get("temperature", 0.7)
            )
            return response["choices"][0]["text"]
            
        elif self.provider == "vllm":
            outputs = self.client.generate([prompt], **kwargs)
            return outputs[0].outputs[0].text

# Usage - same interface regardless of provider!
llm = LLMProvider(provider="llama")  # Easy switch!
response = llm.complete("Explain quantum computing")
    '''
    
    print(code_example)
    
    print("\n2️⃣ GRADUAL MIGRATION WITH FALLBACK:")
    
    fallback_code = '''
class MigrationLLM:
    """LLM with automatic fallback during migration."""
    
    def __init__(self, primary="llama", fallback="openai"):
        self.primary_llm = LLMProvider(primary)
        self.fallback_llm = LLMProvider(fallback)
        self.use_fallback_probability = 0.1  # Start with 10% on new
    
    def complete(self, prompt: str, **kwargs) -> str:
        """Complete with automatic fallback."""
        
        import random
        
        # Gradually increase usage of new system
        use_primary = random.random() > self.use_fallback_probability
        
        if use_primary:
            try:
                response = self.primary_llm.complete(prompt, **kwargs)
                # Log success
                self.log_success("primary")
                return response
            except Exception as e:
                # Log failure and fallback
                self.log_failure("primary", e)
                return self.fallback_llm.complete(prompt, **kwargs)
        else:
            # Still testing with fallback
            return self.fallback_llm.complete(prompt, **kwargs)
    
    def increase_primary_usage(self, increment: float = 0.1):
        """Gradually increase primary usage."""
        self.use_fallback_probability = max(0, 
            self.use_fallback_probability - increment)
    '''
    
    print(fallback_code)


def main():
    """Run migration planning exercise."""
    
    # Create comprehensive migration plan
    create_migration_plan()
    
    print("\n" + "=" * 70)
    print("EXERCISE 3 COMPLETE")
    print("=" * 70)
    print("\n✅ You now have a complete migration plan from OpenAI to open-source!")
    print("   Remember: Migration is a marathon, not a sprint. Plan carefully!")


if __name__ == "__main__":
    main()
