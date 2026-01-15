# From: Zero to AI Agent, Chapter 5, Section 5.1  
# File: return_preview.py
# Topic: Preview of return values (covered in detail in Section 5.3)

def calculate_dog_years():
    human_years = 5
    dog_years = human_years * 7
    print(f"{human_years} human years = {dog_years} dog years")

calculate_dog_years()  # This prints but doesn't give us the value back

# Preview of what's coming in section 5.3:
def calculate_dog_years_better():
    human_years = 5
    dog_years = human_years * 7
    return dog_years  # 'return' sends the value back

result = calculate_dog_years_better()
print(f"The result is {result}")  # Now we can use the value!
