# From: Zero to AI Agent, Chapter 5, Section 5.8
# class_anatomy.py - Understanding class structure

class Dog:                          # 'class' keyword + name (CamelCase!)
    """A class representing a dog"""  # Docstring (optional but recommended)

    def __init__(self, name, breed):  # Special method: runs when creating object
        self.name = name              # 'self.name' creates an attribute
        self.breed = breed            # Store data that belongs to THIS dog

    def bark(self):                   # Regular method (note 'self' parameter)
        print(f"{self.name} says: Woof!")

    def describe(self):
        return f"{self.name} is a {self.breed}"


# Creating an INSTANCE (an actual dog from the blueprint)
my_dog = Dog("Buddy", "Golden Retriever")

# Accessing attributes
print(my_dog.name)        # Buddy
print(my_dog.breed)       # Golden Retriever

# Calling methods
my_dog.bark()             # Buddy says: Woof!
print(my_dog.describe())  # Buddy is a Golden Retriever
