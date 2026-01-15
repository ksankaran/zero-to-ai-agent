# From: Zero to AI Agent, Chapter 3, Section 3.4
# Exercise 2: Character Frequency Counter
# Count vowels and consonants in a string using loops

print("=" * 40)
print("CHARACTER FREQUENCY COUNTER")
print("=" * 40)

text = input("Enter some text: ")

# Initialize counters for each vowel
count_a = 0
count_e = 0
count_i = 0
count_o = 0
count_u = 0
total_consonants = 0
total_digits = 0
total_spaces = 0
total_other = 0

# Process each character using a for loop
for char in text.lower():
    if char == 'a':
        count_a = count_a + 1
    elif char == 'e':
        count_e = count_e + 1
    elif char == 'i':
        count_i = count_i + 1
    elif char == 'o':
        count_o = count_o + 1
    elif char == 'u':
        count_u = count_u + 1
    elif char.isalpha():
        # It's a letter but not a vowel, so it's a consonant
        total_consonants = total_consonants + 1
    elif char.isdigit():
        total_digits = total_digits + 1
    elif char == ' ':
        total_spaces = total_spaces + 1
    else:
        total_other = total_other + 1

# Calculate totals
total_vowels = count_a + count_e + count_i + count_o + count_u
total_letters = total_vowels + total_consonants

# Display results
print("")
print("CHARACTER ANALYSIS:")
print("-" * 40)

print("Vowel breakdown:")
if count_a > 0:
    print(f"  A: {'*' * count_a} ({count_a})")
if count_e > 0:
    print(f"  E: {'*' * count_e} ({count_e})")
if count_i > 0:
    print(f"  I: {'*' * count_i} ({count_i})")
if count_o > 0:
    print(f"  O: {'*' * count_o} ({count_o})")
if count_u > 0:
    print(f"  U: {'*' * count_u} ({count_u})")

print("")
print("Total Statistics:")
print(f"  Vowels: {total_vowels}")
print(f"  Consonants: {total_consonants}")
print(f"  Digits: {total_digits}")
print(f"  Spaces: {total_spaces}")
print(f"  Other: {total_other}")

if total_letters > 0:
    vowel_percentage = (total_vowels / total_letters) * 100
    print("")
    print(f"Vowels make up {vowel_percentage:.1f}% of all letters")
    print(f"Consonants make up {100 - vowel_percentage:.1f}% of all letters")

print("=" * 40)
