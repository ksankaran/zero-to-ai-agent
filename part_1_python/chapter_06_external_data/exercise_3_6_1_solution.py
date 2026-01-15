# From: Zero to AI Agent, Chapter 6, Section 6.1
# Exercise 3 Solution: Word Counter

"""
Word Counter
Create a program that counts words in any text file.
"""

def count_words(filename):
    """Count words, lines, and find longest word in file"""
    try:
        with open(filename, "r") as file:
            content = file.read()
            lines = content.split("\n")
            words = content.split()
            
            # Count statistics
            total_words = len(words)
            total_lines = len(lines)
            
            # Find longest word
            longest_word = ""
            if words:
                longest_word = max(words, key=len)
            
            # Display results
            print(f"\n📊 File Statistics for '{filename}':")
            print(f"  Total words: {total_words}")
            print(f"  Total lines: {total_lines}")
            print(f"  Longest word: '{longest_word}' ({len(longest_word)} chars)")
            
    except FileNotFoundError:
        print(f"❌ File '{filename}' not found!")
    except Exception as e:
        print(f"Error reading file: {e}")

def main():
    print("=== Word Counter ===")
    filename = input("Enter filename to analyze: ")
    count_words(filename)
    
    # Ask if they want to analyze another
    while True:
        another = input("\nAnalyze another file? (yes/no): ")
        if another.lower() == "yes":
            filename = input("Enter filename: ")
            count_words(filename)
        else:
            break
    
    print("Thanks for using Word Counter! 📚")

if __name__ == "__main__":
    main()
