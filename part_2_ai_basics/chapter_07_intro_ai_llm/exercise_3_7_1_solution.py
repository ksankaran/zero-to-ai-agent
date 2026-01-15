# From: Zero to AI Agent, Chapter 7, Section 7.1
# File: exercise_3_7_1_solution.py

"""
Exercise 3 Solution: Design Your Own AI Application
Example AI application design to inspire your thinking.
"""

def create_example_application():
    """
    Creates a detailed example of an AI application design.
    This shows one possible solution to inspire creative thinking.
    """
    
    ai_application = {
        "name": "Smart Fridge Chef",
        
        "problem": """I never know what to cook with the random ingredients in my fridge, 
and food often goes to waste. I also struggle to maintain a balanced diet and 
often resort to ordering takeout when I can't think of what to make.""",
        
        "ai_type": "Supervised Learning",
        
        "ai_type_reason": """The system would learn from thousands of labeled recipes 
(ingredients → dish name + instructions). Each recipe is labeled with ingredients, 
cooking time, difficulty level, nutritional info, and user ratings. This is 
classic supervised learning - learning from examples with known outputs.""",
        
        "data_needed": [
            "Thousands of recipes with complete ingredient lists",
            "User ratings and reviews for each recipe",
            "Ingredient substitution database (e.g., buttermilk → milk + lemon)",
            "Nutritional information for all ingredients",
            "Typical shelf life and storage info for ingredients",
            "Cooking technique videos/instructions",
            "Dietary restriction mappings (vegan, gluten-free, etc.)",
            "Seasonal ingredient availability data",
            "Price data for missing ingredients"
        ],
        
        "inputs": [
            "Photo of fridge contents (computer vision to identify ingredients)",
            "Manual ingredient list entry option",
            "Dietary restrictions and allergies",
            "Available cooking time",
            "Number of servings needed",
            "Cooking skill level (beginner/intermediate/expert)",
            "Kitchen equipment available",
            "Preferred cuisine types",
            "Nutritional goals (high protein, low carb, etc.)"
        ],
        
        "outputs": [
            "Top 5 recipe recommendations ranked by match percentage",
            "Shopping list for missing minor ingredients (with cost estimate)",
            "Step-by-step cooking instructions with timers",
            "Nutritional breakdown of each recipe",
            "Estimated prep and cooking time",
            "Difficulty rating for each recipe",
            "Video tutorials for complex techniques",
            "Meal prep suggestions for leftovers",
            "Wine/beverage pairing suggestions"
        ],
        
        "why_ai": """Traditional programming would require impossibly complex rules 
for every ingredient combination. You'd need millions of if-then statements like 
'if has_tomatoes and has_basil and has_mozzarella then suggest_caprese'. 

AI excels here because it can:
1. Learn subtle patterns (ingredients that pair well together)
2. Handle partial matches (missing one ingredient? Find alternatives)
3. Personalize over time (learn YOUR preferences)
4. Discover non-obvious combinations (fusion cuisine)
5. Consider multiple factors simultaneously (nutrition + taste + time + skill)
6. Improve with user feedback (ratings make it better)"""
    }
    
    return ai_application


def display_application_design():
    """Displays the AI application design in a structured format."""
    
    print("="*70)
    print("EXERCISE 3 SOLUTION: AI Application Design Example")
    print("="*70)
    
    app = create_example_application()
    
    print(f"\n🍳 APPLICATION NAME: {app['name']}")
    print("-" * 50)
    
    print(f"\n📌 PROBLEM IT SOLVES:")
    print(app['problem'])
    
    print(f"\n📊 TYPE OF AI: {app['ai_type']}")
    print(f"\nWhy this type?")
    print(app['ai_type_reason'])
    
    print("\n📁 DATA IT WOULD NEED TO LEARN FROM:")
    for i, data in enumerate(app['data_needed'], 1):
        print(f"  {i}. {data}")
    
    print("\n➡️ INPUTS (What users provide):")
    for i, input_item in enumerate(app['inputs'], 1):
        print(f"  {i}. {input_item}")
    
    print("\n⬅️ OUTPUTS (What the AI produces):")
    for i, output in enumerate(app['outputs'], 1):
        print(f"  {i}. {output}")
    
    print("\n💡 WHY AI INSTEAD OF TRADITIONAL PROGRAMMING?")
    print(app['why_ai'])


def provide_additional_ideas():
    """Provides more AI application ideas to inspire creativity."""
    
    print("\n" + "="*70)
    print("MORE AI APPLICATION IDEAS TO INSPIRE YOU")
    print("="*70)
    
    ideas = [
        {
            "name": "Personal Energy Coach",
            "problem": "Feeling tired at random times, poor sleep quality",
            "ai_approach": "Track activities, sleep, food → predict energy levels",
            "type": "Supervised Learning (energy levels from lifestyle data)"
        },
        {
            "name": "Plant Health Monitor",
            "problem": "House plants dying despite best efforts",
            "ai_approach": "Image analysis + environment data → care instructions",
            "type": "Supervised Learning (plant images → health diagnosis)"
        },
        {
            "name": "Wardrobe Optimizer",
            "problem": "Never know what to wear, clothes go unworn",
            "ai_approach": "Weather + calendar + style preferences → outfit suggestions",
            "type": "Supervised + Reinforcement (learns your actual choices)"
        },
        {
            "name": "Study Buddy AI",
            "problem": "Inefficient studying, forgetting material",
            "ai_approach": "Track study patterns → optimize review schedule",
            "type": "Reinforcement Learning (rewards for retention)"
        },
        {
            "name": "Mood Predictor",
            "problem": "Unexpected mood swings affecting productivity",
            "ai_approach": "Daily patterns + activities → mood forecast",
            "type": "Unsupervised (finding patterns) + Supervised (prediction)"
        }
    ]
    
    for idea in ideas:
        print(f"\n💡 {idea['name']}")
        print(f"   Problem: {idea['problem']}")
        print(f"   Approach: {idea['ai_approach']}")
        print(f"   AI Type: {idea['type']}")


def evaluation_criteria():
    """Shows what makes a good AI application idea."""
    
    print("\n" + "="*70)
    print("WHAT MAKES A GOOD AI APPLICATION?")
    print("="*70)
    
    print("\n✅ Good candidates for AI have:")
    print("  • Patterns to learn (not just rules to follow)")
    print("  • Lots of available training data")
    print("  • Clear success metrics (you can measure if it's working)")
    print("  • Complexity that makes rules impractical")
    print("  • Opportunity for personalization")
    print("  • Room for improvement over time")
    
    print("\n❌ Poor candidates for AI:")
    print("  • Simple calculations (use traditional programming)")
    print("  • Tasks requiring 100% accuracy (AI can make mistakes)")
    print("  • Problems with clear, simple rules")
    print("  • Situations with no historical data")
    print("  • Tasks requiring human judgment/ethics")
    
    print("\n🎯 Remember: AI is best for pattern recognition, prediction, and personalization!")


if __name__ == "__main__":
    display_application_design()
    provide_additional_ideas()
    evaluation_criteria()
    
    print("\n" + "="*70)
    print("YOUR TURN!")
    print("="*70)
    print("\nNow design YOUR OWN AI application using this template:")
    print("1. What problem does it solve?")
    print("2. What type of AI would it use?")
    print("3. What data would it need?")
    print("4. What inputs/outputs would it have?")
    print("5. Why is AI better than traditional programming for this?")
    print("\nBe creative! The best AI ideas solve real problems you face daily.")
