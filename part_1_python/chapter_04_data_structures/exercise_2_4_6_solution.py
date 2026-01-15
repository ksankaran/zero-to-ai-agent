# From: Zero to AI Agent, Chapter 4, Section 4.6
# Exercise 2: Quiz Application

# Questions with order - LIST OF DICTIONARIES
questions = [
    {
        "id": 1,
        "question": "What is Python?",
        "choices": ["A snake", "A language", "A framework", "A database"],
        "correct": 1  # Index of correct answer
    },
    {
        "id": 2,
        "question": "What is a list?",
        "choices": ["A tuple", "An ordered collection", "A dictionary", "A set"],
        "correct": 1
    }
]

# Track answered questions - SET (fast membership testing)
answered = set()

# Store correct answers securely - DICTIONARY (hidden from main list)
answer_key = {q["id"]: q["correct"] for q in questions}

# User responses - DICTIONARY
user_answers = {}

# Simulate quiz
for q in questions:
    print(f"Q{q['id']}: {q['question']}")
    # Simulate answer
    user_answers[q['id']] = 1
    answered.add(q['id'])

# Calculate score
score = sum(1 for qid, ans in user_answers.items() 
           if ans == answer_key[qid])
print(f"Score: {score}/{len(questions)}")
print(f"Questions answered: {answered}")
