# From: Zero to AI Agent, Chapter 6, Section 6.4
# File: 01_try_except_basics.py


# Basic error handling
try:
    result = 10 / 0  # This would crash without try/except
except ZeroDivisionError:
    print("Can't divide by zero!")
    result = None

print(f"Program continues with result: {result}")

# Multiple error types
def process_data(value):
    try:
        num = int(value)
        result = 100 / num
        items = [1, 2, 3]
        return items[num]
    except ValueError:
        return "Not a number"
    except ZeroDivisionError:
        return "Can't divide by zero"
    except IndexError:
        return "Index out of range"

print(process_data("2"))    # Returns 3
print(process_data("0"))    # Can't divide by zero
print(process_data("abc"))  # Not a number
print(process_data("10"))   # Index out of range

# Catching multiple exceptions together
try:
    # Some risky operation
    pass
except (ValueError, TypeError, KeyError) as e:
    print(f"Error occurred: {type(e).__name__}: {e}")
