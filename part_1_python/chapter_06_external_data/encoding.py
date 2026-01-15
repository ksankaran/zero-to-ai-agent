# From: Zero to AI Agent, Chapter 6, Section 6.1
# File: encoding.py

# UTF-8 is the standard (handles emojis and all languages!)
with open("encoded.txt", "w", encoding="utf-8") as f:
    f.write("Hello World! 👋\n")
    f.write("Hola Mundo! 🌎\n")
    f.write("你好世界! 🇨🇳\n")
    f.write("مرحبا بالعالم! 🌍\n")

print("Created file with various languages and emojis")

# Reading with correct encoding
with open("encoded.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print("\nWith UTF-8 encoding:")
    print(content)

# What happens with wrong encoding?
try:
    with open("encoded.txt", "r", encoding="ascii") as f:
        content = f.read()
        print("\nWith ASCII encoding:")
        print(content)
except UnicodeDecodeError as e:
    print(f"\n❌ ASCII can't handle this: {e}")

# Handling encoding errors gracefully
with open("encoded.txt", "r", encoding="ascii", errors="ignore") as f:
    content = f.read()
    print("\nASCII with errors ignored (data loss!):")
    print(content)

with open("encoded.txt", "r", encoding="ascii", errors="replace") as f:
    content = f.read()
    print("\nASCII with errors replaced (see the � symbols):")
    print(content)
