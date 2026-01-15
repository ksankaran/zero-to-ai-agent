# From: Zero to AI Agent, Chapter 3, Section 3.4
# text_analyzer.py

text = input("Enter some text: ")

vowel_count = 0
consonant_count = 0

for character in text.lower():
    if character in "aeiou":
        vowel_count += 1
    elif character.isalpha():  # Check if it's a letter
        consonant_count += 1
    # Skip spaces, numbers, punctuation

print(f"\nText Analysis Complete!")
print(f"Vowels: {vowel_count}")
print(f"Consonants: {consonant_count}")
print(f"Total letters: {vowel_count + consonant_count}")
