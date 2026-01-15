# special_characters.py
# From: Zero to AI Agent, Chapter 2, Section 2.3
# Using escape sequences in strings

# Common escape sequences
print("Line 1\nLine 2\nLine 3")  # \n creates new lines
print("\tIndented text")          # \t creates tabs
print("She said, \"Hello!\"")     # \" for quotes inside quotes
print('It\'s a beautiful day')    # \' for apostrophes in single quotes
print("Path: C:\\Users\\Documents")  # \\ for actual backslashes

# Raw strings (ignore escape sequences)
path = r"C:\Users\Documents\new_folder"  # r prefix makes it raw
print("\nRaw string:", path)

# Unicode characters (emojis!)
print("\nFun with Unicode:")
print("Python \u2764 You")  # Heart symbol
print("Happy coding! 😊")    # Direct emoji (if your terminal supports it)
