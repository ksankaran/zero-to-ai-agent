# From: Zero to AI Agent, Chapter 5, Section 5.4
# File: mutable_defaults_gotcha.py

# DON'T DO THIS - Mutable default argument
def add_item_bad(item, shopping_list=[]):  # Bad! Empty list as default
    shopping_list.append(item)
    return shopping_list

# Watch what happens:
list1 = add_item_bad("apples")
print(list1)  # ['apples'] - looks fine

list2 = add_item_bad("bananas")
print(list2)  # ['apples', 'bananas'] - WHAT?! 

# The default list is shared between calls!

# DO THIS INSTEAD:
def add_item_good(item, shopping_list=None):
    if shopping_list is None:
        shopping_list = []  # Create new list each time
    shopping_list.append(item)
    return shopping_list

# Now it works correctly:
list3 = add_item_good("apples")
print(list3)  # ['apples']

list4 = add_item_good("bananas")
print(list4)  # ['bananas'] - Correct!