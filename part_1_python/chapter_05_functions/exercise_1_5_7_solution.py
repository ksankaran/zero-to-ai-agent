# From: Zero to AI Agent, Chapter 5, Section 5.7
# File: exercise_1_5_7_solution.py

# string_utils.py module
"""String manipulation utilities module"""

def capitalize_words(text):
    """Capitalize first letter of each word"""
    return ' '.join(word.capitalize() for word in text.split())

def remove_punctuation(text):
    """Remove all punctuation from text"""
    import string
    return ''.join(char for char in text if char not in string.punctuation)

def count_vowels(text):
    """Count vowels in text"""
    vowels = 'aeiouAEIOU'
    return sum(1 for char in text if char in vowels)

def is_palindrome(text):
    """Check if text is palindrome (ignoring spaces and case)"""
    cleaned = ''.join(text.split()).lower()
    return cleaned == cleaned[::-1]

def reverse_words(text):
    """Reverse the order of words in text"""
    return ' '.join(text.split()[::-1])

def get_word_frequency(text):
    """Return dictionary of word frequencies"""
    words = text.lower().split()
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    return frequency

# Test file that uses the module
if __name__ == "__main__":
    # Test all functions
    test_text = "Hello World! Python Programming is Fun"
    
    print("Original text:", test_text)
    print("Capitalized:", capitalize_words(test_text.lower()))
    print("No punctuation:", remove_punctuation(test_text))
    print("Vowel count:", count_vowels(test_text))
    print("Words reversed:", reverse_words(test_text))
    
    # Test palindrome
    palindrome_test = "A man a plan a canal Panama"
    print(f"\nIs '{palindrome_test}' a palindrome?", is_palindrome(palindrome_test))
    
    # Test word frequency
    frequency_text = "the quick brown fox jumps over the lazy brown dog"
    print(f"\nWord frequency for: '{frequency_text}'")
    print(get_word_frequency(frequency_text))
