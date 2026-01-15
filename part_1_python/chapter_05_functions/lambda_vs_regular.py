# From: Zero to AI Agent, Chapter 5, Section 5.5
# File: lambda_vs_regular.py

# USE LAMBDA when:
# - Function is simple (one expression)
# - You need it just once
# - It's an argument to another function

# Simple operation used once
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))

# USE REGULAR FUNCTION when:
# - Logic is complex
# - You'll reuse it
# - You need multiple lines
# - It needs documentation

def calculate_ai_score(response, user_rating, time_taken):
    """
    Calculate quality score for AI response.
    Considers response length, user rating, and response time.
    """
    base_score = user_rating * 20  # Rating 1-5 becomes 20-100
    
    # Bonus for quick responses
    if time_taken < 1.0:
        base_score += 10
    
    # Penalty for very short responses
    if len(response) < 10:
        base_score -= 15
    
    # Keep score in valid range
    return max(0, min(100, base_score))

# This would be terrible as a lambda!