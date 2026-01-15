# From: Zero to AI Agent, Chapter 11, Section 11.3
# File: exercise_2_11_3_solution.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(temperature=0.7)

# Step 1: Generate questions
question_generator_prompt = ChatPromptTemplate.from_template(
    """Generate exactly 3 interesting questions about {topic}.
    Number them 1, 2, and 3.
    
    Questions:"""
)

question_chain = question_generator_prompt | llm

# Step 2: Pick the most interesting question
question_selector_prompt = ChatPromptTemplate.from_template(
    """From these questions, pick the MOST interesting and thought-provoking one.
    Return ONLY that question, nothing else.
    
    Questions:
    {questions}
    
    Most interesting question:"""
)

selector_chain = question_selector_prompt | llm

# Step 3: Answer the selected question
answer_prompt = ChatPromptTemplate.from_template(
    """Provide a thoughtful, detailed answer to this question:
    {question}
    
    Answer:"""
)

answer_chain = answer_prompt | llm

# Run the complete process
def explore_topic(topic):
    """Generate questions, select the best, and answer it"""
    
    print(f"📚 Exploring Topic: {topic}")
    print("=" * 60)
    
    # Generate questions
    print("\n1️⃣ Generating questions...")
    questions_response = question_chain.invoke({"topic": topic})
    questions = questions_response.content
    print(questions)
    
    # Select most interesting
    print("\n2️⃣ Selecting most interesting question...")
    selected_response = selector_chain.invoke({"questions": questions})
    selected_question = selected_response.content
    print(f"Selected: {selected_question}")
    
    # Answer it
    print("\n3️⃣ Answering the question...")
    answer_response = answer_chain.invoke({"question": selected_question})
    print(answer_response.content)
    
    return {
        "topic": topic,
        "all_questions": questions,
        "selected": selected_question,
        "answer": answer_response.content
    }

# Test with different topics
topics = ["quantum computing", "happiness", "climate change"]

for topic in topics:
    result = explore_topic(topic)
    print("\n" + "="*60 + "\n")
