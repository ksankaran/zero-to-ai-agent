# string_immutability.py
# From: Zero to AI Agent, Chapter 2, Section 2.3
# Understanding that strings cannot be modified

word = "Python"
print("Original word:", word)

# This DOESN'T change the string, it creates a new one
new_word = word.replace('P', 'J')
print("After replace:")
print("  word:", word)          # Still "Python"
print("  new_word:", new_word)  # "Jython"

# You CAN'T do this:
# word[0] = 'J'  # This would cause an error!

# Instead, you must create a new string
word = 'J' + word[1:]  # Take 'J' plus everything after first character
print("Modified word:", word)

# Why does this matter?
# When you "modify" strings, Python creates new ones
text = "Hello"
text = text + " World"  # Creates a NEW string "Hello World"
text = text.upper()      # Creates ANOTHER new string "HELLO WORLD"
# The original strings are discarded
