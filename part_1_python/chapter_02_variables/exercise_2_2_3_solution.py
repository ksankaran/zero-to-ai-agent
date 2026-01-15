# Exercise 2: Mad Libs Story Generator
# Create a silly story by filling in the blanks!

# Solution:

print("=" * 40)
print("MAD LIBS STORY GENERATOR")
print("=" * 40)

# The words to fill in (simulating user input)
adjective1 = "fluffy"
animal = "penguin"
verb = "dancing"
food = "pizza"
place = "the moon"
adjective2 = "sparkly"
number = 42

# Build the silly story using f-strings
story_line1 = f"Once upon a time, a {adjective1} {animal} was {verb} in {place}."
story_line2 = f"Suddenly, it found {number} pieces of {adjective2} {food}!"
story_line3 = f"The {animal} shouted: 'This is the best day ever!'"
story_line4 = f"And from that day on, everyone called it the {adjective1} {animal} of {place}."

# Display the story
print("\nYOUR SILLY STORY:")
print("-" * 40)
print(story_line1)
print(story_line2)
print(story_line3)
print(story_line4)
print("-" * 40)

# Show statistics about the story
full_story = story_line1 + " " + story_line2 + " " + story_line3 + " " + story_line4
print(f"\nStory length: {len(full_story)} characters")
print(f"Your animal '{animal}' appears in the story!")
print("=" * 40)
