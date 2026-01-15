# From: Zero to AI Agent, Chapter 6, Section 6.3
# Exercise 2 Solution: Dad Joke Fetcher

"""
Dad Joke Fetcher
Build a program that fetches random jokes from an API.
"""

import requests

def get_joke():
    """Fetch a random dad joke"""
    try:
        url = "https://icanhazdadjoke.com/"
        headers = {'Accept': 'application/json'}
        
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            return data['joke']
        else:
            return "Couldn't fetch a joke right now!"
            
    except requests.exceptions.RequestException:
        return "No internet connection for jokes!"

def main():
    print("=== Dad Joke Fetcher ===")
    jokes_viewed = 0
    
    while True:
        print("\nPress Enter for a joke (or type 'quit')")
        choice = input()
        
        if choice.lower() == 'quit':
            break
        
        joke = get_joke()
        print(f"\n😄 {joke}")
        jokes_viewed += 1
        
    print(f"\nYou viewed {jokes_viewed} jokes! Thanks for laughing! 😂")

if __name__ == "__main__":
    main()
