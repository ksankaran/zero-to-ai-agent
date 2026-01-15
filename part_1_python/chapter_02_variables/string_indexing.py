# string_indexing.py
# From: Zero to AI Agent, Chapter 2, Section 2.3
# Accessing parts of strings

message = "Python Programming"
#          012345678901234567  (positive indices)
#         -18-17-16...-3-2-1   (negative indices)

# Accessing individual characters
print("First character:", message[0])     # 'P'
print("Fifth character:", message[4])     # 'o'
print("Last character:", message[-1])     # 'g'
print("Second to last:", message[-2])     # 'n'

# Slicing - getting chunks of the string
print("\n--- Slicing ---")
print("First 6 characters:", message[0:6])    # 'Python'
print("Characters 7 to end:", message[7:])    # 'Programming'
print("Characters 7 to 11:", message[7:11])   # 'Prog'
print("Everything except last 4:", message[:-4])  # 'Python Program'

# Slicing with steps
print("\n--- Slicing with steps ---")
print("Every other character:", message[::2])  # 'Pto rgamn'
print("Reverse the string:", message[::-1])    # 'gnimmargorP nohtyP'

# Practical example: extracting parts of data
email = "john.doe@example.com"
at_position = email.index('@')  # Find where @ is
username = email[:at_position]  # Everything before @
domain = email[at_position+1:]  # Everything after @
print(f"\nEmail: {email}")
print(f"Username: {username}")
print(f"Domain: {domain}")
