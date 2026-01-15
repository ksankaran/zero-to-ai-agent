# From: Zero to AI Agent, Chapter 6, Section 6.4
# File: 06_robust_functions.py


def get_number(prompt, min_val=None, max_val=None):
    """Get valid number with retry"""
    while True:
        try:
            value = float(input(prompt))
            if min_val is not None and value < min_val:
                print(f"Must be at least {min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f"Must be at most {max_val}")
                continue
            return value
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            print("\nCancelled")
            return None

def safe_file_read(filename, default=""):
    """Read file with fallback"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return default
    except PermissionError:
        print(f"No permission to read {filename}")
        return default
    except UnicodeDecodeError:
        print(f"Encoding issue with {filename}")
        return default
