# From: Zero to AI Agent, Chapter 6, Section 6.3
# Exercise 3 Solution: Number Facts

"""
Number Facts
Create a program that gets interesting facts about numbers.
"""

import requests

def get_math_fact(number):
    """Get math fact about a number"""
    try:
        url = f"http://numbersapi.com/{number}/math"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            return response.text
        return None
    except:
        return None

def get_trivia_fact(number):
    """Get trivia fact about a number"""
    try:
        url = f"http://numbersapi.com/{number}/trivia"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            return response.text
        return None
    except:
        return None

def save_fact(fact):
    """Save interesting fact to file"""
    with open("number_facts.txt", "a") as file:
        file.write(fact + "\n\n")
    print("✅ Fact saved to number_facts.txt")

def main():
    print("=== Number Facts ===")
    
    while True:
        number = input("\nEnter a number (or 'quit'): ")
        
        if number.lower() == 'quit':
            break
        
        try:
            num = int(number)
            
            # Get facts
            math_fact = get_math_fact(num)
            trivia_fact = get_trivia_fact(num)
            
            if math_fact:
                print(f"\n🔢 Math fact: {math_fact}")
            
            if trivia_fact:
                print(f"\n🎲 Trivia: {trivia_fact}")
            
            if math_fact or trivia_fact:
                save_choice = input("\nSave these facts? (yes/no): ")
                if save_choice.lower() == 'yes':
                    if math_fact:
                        save_fact(f"Math: {math_fact}")
                    if trivia_fact:
                        save_fact(f"Trivia: {trivia_fact}")
            else:
                print("❌ Couldn't get facts for that number")
                
        except ValueError:
            print("Please enter a valid number!")
    
    print("Thanks for learning! 🎓")

if __name__ == "__main__":
    main()
