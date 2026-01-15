# From: Zero to AI Agent, Chapter 5, Section 5.3
# File: exercise_1_5_3_solution.py

def calculate_letter_grade(score):
    """Convert numerical score to letter grade"""
    # Check for invalid scores
    if score < 0 or score > 100:
        return None
    
    # Return appropriate letter grade
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

def get_grade_statistics(scores):
    """Calculate statistics for a list of scores"""
    if not scores:  # Empty list check
        return None, None, None, None
    
    # Calculate basic stats
    average = sum(scores) / len(scores)
    highest = max(scores)
    lowest = min(scores)
    
    # Get all letter grades
    letter_grades = []
    for score in scores:
        grade = calculate_letter_grade(score)
        if grade:  # Only add valid grades
            letter_grades.append(grade)
    
    # Find most common grade
    if letter_grades:
        grade_counts = {}
        for grade in letter_grades:
            grade_counts[grade] = grade_counts.get(grade, 0) + 1
        most_common = max(grade_counts, key=grade_counts.get)
    else:
        most_common = None
    
    return average, highest, lowest, most_common

# Test the functions
print(calculate_letter_grade(95))   # A
print(calculate_letter_grade(75))   # C
print(calculate_letter_grade(150))  # None (invalid)

# Test with a list of scores
test_scores = [85, 92, 78, 95, 88, 73, 91]
avg, high, low, common = get_grade_statistics(test_scores)
print(f"\nClass Statistics:")
print(f"Average: {avg:.1f}")
print(f"Highest: {high}")
print(f"Lowest: {low}")
print(f"Most common grade: {common}")