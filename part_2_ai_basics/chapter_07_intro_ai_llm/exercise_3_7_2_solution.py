# From: Zero to AI Agent, Chapter 7, Section 7.2
# File: exercise_3_7_2_solution.py

"""
Exercise 3 Solution: Identifying Good vs Bad LLM Tasks
Understanding what LLMs excel at versus what they struggle with.
"""

from enum import Enum
from typing import Dict, List, Tuple
from dataclasses import dataclass


class TaskSuitability(Enum):
    """Categories for LLM task suitability."""
    GREAT = "✅ Great for LLMs"
    OKAY = "⚠️ Okay with Caveats"
    BAD = "❌ Bad Idea"


@dataclass
class TaskAnalysis:
    """Analysis of a task's suitability for LLMs."""
    task: str
    suitability: TaskSuitability
    reasoning: str
    alternatives: str = ""
    best_practices: str = ""


def analyze_llm_tasks() -> Dict[str, TaskAnalysis]:
    """
    Analyze various tasks for LLM suitability.
    
    Returns:
        Dictionary of task -> TaskAnalysis
    """
    
    tasks = {
        "blog_draft": TaskAnalysis(
            task="Writing a first draft of a blog post",
            suitability=TaskSuitability.GREAT,
            reasoning=(
                "LLMs excel at generating coherent, structured text. "
                "They can create outlines, expand ideas, and maintain consistent tone."
            ),
            best_practices=(
                "• Provide clear topic and target audience\n"
                "• Review and fact-check output\n"
                "• Add personal insights and experiences\n"
                "• Verify any statistics or claims"
            )
        ),
        
        "compound_interest": TaskAnalysis(
            task="Calculating compound interest over 30 years",
            suitability=TaskSuitability.BAD,
            reasoning=(
                "LLMs can't perform precise mathematical calculations reliably. "
                "They approximate based on training patterns, leading to errors."
            ),
            alternatives=(
                "• Use a calculator or spreadsheet\n"
                "• Write or use a simple Python function\n"
                "• Use financial calculator tools\n"
                "• Ask LLM to write the formula, then calculate yourself"
            )
        ),
        
        "email_professional": TaskAnalysis(
            task="Checking if an email sounds professional",
            suitability=TaskSuitability.GREAT,
            reasoning=(
                "LLMs understand tone, formality, and professional communication. "
                "They can identify casual language, suggest improvements, and ensure clarity."
            ),
            best_practices=(
                "• Provide context about recipient and purpose\n"
                "• Ask for specific feedback (tone, clarity, structure)\n"
                "• Consider industry-specific conventions\n"
                "• Review suggestions critically"
            )
        ),
        
        "stock_prices": TaskAnalysis(
            task="Getting today's stock prices",
            suitability=TaskSuitability.BAD,
            reasoning=(
                "LLMs don't have real-time data access. "
                "Training data has a cutoff date, so current information is unavailable."
            ),
            alternatives=(
                "• Use financial APIs (Yahoo Finance, Alpha Vantage)\n"
                "• Check financial websites directly\n"
                "• Use specialized trading platforms\n"
                "• Some LLMs with web access can search for current data"
            )
        ),
        
        "explain_concept": TaskAnalysis(
            task="Explaining a complex concept simply",
            suitability=TaskSuitability.GREAT,
            reasoning=(
                "LLMs excel at adapting explanations for different audiences. "
                "They can use analogies, break down components, and adjust complexity."
            ),
            best_practices=(
                "• Specify the audience level (child, beginner, expert)\n"
                "• Ask for analogies or examples\n"
                "• Request step-by-step breakdowns\n"
                "• Verify technical accuracy for specialized topics"
            )
        ),
        
        "test_data": TaskAnalysis(
            task="Generating test data for your application",
            suitability=TaskSuitability.GREAT,
            reasoning=(
                "LLMs can generate realistic, varied test data quickly. "
                "They understand data patterns and can create edge cases."
            ),
            best_practices=(
                "• Provide clear schema/format requirements\n"
                "• Specify constraints and validation rules\n"
                "• Request both typical and edge cases\n"
                "• Generate in batches to ensure variety"
            )
        ),
        
        "medical_diagnosis": TaskAnalysis(
            task="Making medical diagnoses",
            suitability=TaskSuitability.BAD,
            reasoning=(
                "Medical diagnosis requires professional expertise and liability. "
                "LLMs can hallucinate symptoms or conditions. Lives are at stake."
            ),
            alternatives=(
                "• Consult qualified medical professionals\n"
                "• Use for educational understanding only\n"
                "• Can help prepare questions for doctors\n"
                "• Never replace professional medical advice"
            )
        ),
        
        "document_summary": TaskAnalysis(
            task="Summarizing a long document",
            suitability=TaskSuitability.GREAT,
            reasoning=(
                "LLMs excel at identifying key points and condensing information. "
                "They maintain context and can adjust summary length/detail."
            ),
            best_practices=(
                "• Specify desired summary length\n"
                "• Indicate key aspects to focus on\n"
                "• Check that critical points aren't omitted\n"
                "• Consider chunking very long documents"
            )
        ),
        
        "password_security": TaskAnalysis(
            task="Checking if a password is secure",
            suitability=TaskSuitability.BAD,
            reasoning=(
                "Never send passwords to LLMs - security risk! "
                "Also, password strength requires algorithmic checking, not language analysis."
            ),
            alternatives=(
                "• Use dedicated password strength libraries\n"
                "• Implement client-side validation\n"
                "• Use services like Have I Been Pwned API\n"
                "• Never transmit actual passwords to third parties"
            )
        ),
        
        "shakespeare_poetry": TaskAnalysis(
            task="Writing poetry in Shakespeare's style",
            suitability=TaskSuitability.GREAT,
            reasoning=(
                "LLMs are excellent at mimicking writing styles. "
                "They understand meter, rhyme schemes, and archaic language patterns."
            ),
            best_practices=(
                "• Specify form (sonnet, soliloquy, etc.)\n"
                "• Request specific themes or subjects\n"
                "• Can combine with modern topics for humor\n"
                "• Review for authentic feel and rhythm"
            )
        )
    }
    
    return tasks


def categorize_exercise_tasks():
    """Solve Exercise 3: Categorize the specific tasks."""
    
    print("=" * 70)
    print("EXERCISE 3 SOLUTION: IDENTIFYING GOOD VS BAD LLM TASKS")
    print("=" * 70)
    
    # Map exercise numbers to task keys
    exercise_mapping = [
        (1, "blog_draft"),
        (2, "compound_interest"),
        (3, "email_professional"),
        (4, "stock_prices"),
        (5, "explain_concept"),
        (6, "test_data"),
        (7, "medical_diagnosis"),
        (8, "document_summary"),
        (9, "password_security"),
        (10, "shakespeare_poetry")
    ]
    
    tasks = analyze_llm_tasks()
    
    # Group by suitability
    great_tasks = []
    okay_tasks = []
    bad_tasks = []
    
    for num, task_key in exercise_mapping:
        task = tasks[task_key]
        if task.suitability == TaskSuitability.GREAT:
            great_tasks.append((num, task))
        elif task.suitability == TaskSuitability.OKAY:
            okay_tasks.append((num, task))
        else:
            bad_tasks.append((num, task))
    
    # Display categorized results
    print("\n✅ GREAT FOR LLMs:")
    print("-" * 50)
    for num, task in great_tasks:
        print(f"{num}. {task.task}")
        print(f"   Why: {task.reasoning[:100]}...")
    
    print("\n⚠️ OKAY WITH CAVEATS:")
    print("-" * 50)
    if okay_tasks:
        for num, task in okay_tasks:
            print(f"{num}. {task.task}")
            print(f"   Caveat: {task.reasoning[:100]}...")
    else:
        print("(None in this exercise)")
    
    print("\n❌ BAD IDEA:")
    print("-" * 50)
    for num, task in bad_tasks:
        print(f"{num}. {task.task}")
        print(f"   Why: {task.reasoning[:100]}...")


def detailed_task_analysis():
    """Provide detailed analysis for each task."""
    
    print("\n" + "=" * 70)
    print("DETAILED TASK ANALYSIS")
    print("=" * 70)
    
    tasks = analyze_llm_tasks()
    
    # Sort tasks by suitability
    sorted_tasks = sorted(tasks.values(), 
                         key=lambda x: (x.suitability.value, x.task))
    
    current_suitability = None
    
    for task in sorted_tasks:
        if task.suitability != current_suitability:
            print(f"\n{task.suitability.value}")
            print("=" * 50)
            current_suitability = task.suitability
        
        print(f"\n📋 Task: {task.task}")
        print(f"💭 Reasoning: {task.reasoning}")
        
        if task.best_practices:
            print(f"✨ Best Practices:\n{task.best_practices}")
        
        if task.alternatives:
            print(f"🔄 Alternatives:\n{task.alternatives}")


def task_selection_framework():
    """Framework for deciding if a task is suitable for LLMs."""
    
    print("\n" + "=" * 70)
    print("LLM TASK SUITABILITY FRAMEWORK")
    print("=" * 70)
    
    print("\n🎯 GREAT FOR LLMs - All these conditions:")
    print("• Involves natural language processing")
    print("• Doesn't require real-time data")
    print("• Benefits from pattern recognition")
    print("• Allows for some variation in output")
    print("• Not life-critical or high-stakes")
    
    print("\n⚠️ USE WITH CAUTION - Any of these:")
    print("• Requires some factual accuracy")
    print("• Involves subjective judgment")
    print("• Needs cultural/contextual awareness")
    print("• Has legal/ethical implications")
    print("• Output needs human review")
    
    print("\n❌ AVOID FOR LLMs - Any of these:")
    print("• Requires precise calculations")
    print("• Needs real-time/current data")
    print("• Involves personal/sensitive data")
    print("• Has safety/health implications")
    print("• Requires guaranteed accuracy")
    print("• Needs deterministic output")


def practical_examples():
    """Show practical examples of good task design."""
    
    print("\n" + "=" * 70)
    print("PRACTICAL EXAMPLES: TURNING BAD TASKS INTO GOOD ONES")
    print("=" * 70)
    
    transformations = [
        {
            "bad": "Calculate my tax return",
            "good": "Explain tax deductions I might be eligible for",
            "why": "Shifted from calculation to explanation"
        },
        {
            "bad": "Diagnose my symptoms",
            "good": "Help me describe symptoms clearly for my doctor",
            "why": "Shifted from diagnosis to communication aid"
        },
        {
            "bad": "Tell me tomorrow's weather",
            "good": "Explain how weather patterns work",
            "why": "Shifted from real-time data to general knowledge"
        },
        {
            "bad": "Is this contract legally binding?",
            "good": "What are common elements in contracts I should review?",
            "why": "Shifted from legal advice to educational information"
        },
        {
            "bad": "Debug my production code",
            "good": "Suggest debugging strategies for this type of error",
            "why": "Shifted from specific fix to general approach"
        }
    ]
    
    for i, transform in enumerate(transformations, 1):
        print(f"\nExample {i}:")
        print(f"❌ Bad: {transform['bad']}")
        print(f"✅ Good: {transform['good']}")
        print(f"💡 Why: {transform['why']}")


def key_insights():
    """Summarize key insights about LLM task suitability."""
    
    print("\n" + "=" * 70)
    print("KEY INSIGHTS")
    print("=" * 70)
    
    insights = [
        ("Language Tasks", "LLMs excel at anything involving natural language"),
        ("Pattern Recognition", "Great at finding and applying patterns from training"),
        ("Creative Generation", "Excellent for creative and varied content"),
        ("Style Mimicry", "Can adopt any writing style or tone"),
        ("Knowledge Synthesis", "Good at combining information in new ways"),
        
        ("No Real-Time Data", "Cannot access current information"),
        ("No True Calculation", "Approximate math, not compute"),
        ("No Critical Decisions", "Never use for life-impacting choices"),
        ("No Personal Data", "Don't send sensitive information"),
        ("No Guaranteed Facts", "Always verify important information")
    ]
    
    print("\n✅ LLMs ARE GREAT AT:")
    for title, desc in insights[:5]:
        print(f"• {title}: {desc}")
    
    print("\n❌ LLMs CANNOT/SHOULD NOT:")
    for title, desc in insights[5:]:
        print(f"• {title}: {desc}")
    
    print("\n" + "=" * 70)
    print("🎯 REMEMBER: LLMs are powerful tools for language tasks,")
    print("   not magic oracles for all problems!")
    print("=" * 70)


def main():
    """Run all task suitability demonstrations."""
    
    # Exercise solution
    categorize_exercise_tasks()
    
    # Detailed analysis
    detailed_task_analysis()
    
    # Framework
    task_selection_framework()
    
    # Practical examples
    practical_examples()
    
    # Key insights
    key_insights()


if __name__ == "__main__":
    main()
