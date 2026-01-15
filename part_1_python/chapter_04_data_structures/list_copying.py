# From: Zero to AI Agent, Chapter 4, Section 4.2
# list_copying.py - The critical importance of proper list copying

# The WRONG way (creates a reference, not a copy)
original_list = [1, 2, 3, 4, 5]
not_a_copy = original_list  # This is NOT a copy!

not_a_copy.append(6)
print("Original list:", original_list)  # [1, 2, 3, 4, 5, 6] - CHANGED!
print("Not a copy:", not_a_copy)        # [1, 2, 3, 4, 5, 6]
# They're the same list!

# The RIGHT ways to copy a list

# Method 1: Using copy()
list1 = [1, 2, 3, 4, 5]
list2 = list1.copy()  # Creates an actual copy
list2.append(6)
print("\nUsing copy():")
print("list1:", list1)  # [1, 2, 3, 4, 5] - unchanged!
print("list2:", list2)  # [1, 2, 3, 4, 5, 6]

# Method 2: Using slicing
list3 = [7, 8, 9]
list4 = list3[:]  # The [:] creates a copy
list4.append(10)
print("\nUsing slicing [:]:")
print("list3:", list3)  # [7, 8, 9] - unchanged!
print("list4:", list4)  # [7, 8, 9, 10]

# Method 3: Using list()
list5 = [11, 12, 13]
list6 = list(list5)  # Creates a new list
list6.append(14)
print("\nUsing list():")
print("list5:", list5)  # [11, 12, 13] - unchanged!
print("list6:", list6)  # [11, 12, 13, 14]
