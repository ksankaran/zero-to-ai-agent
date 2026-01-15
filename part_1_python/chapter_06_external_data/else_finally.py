# From: Zero to AI Agent, Chapter 6, Section 6.4
# File: 02_else_finally.py


def read_config(filename):
    file = None
    try:
        file = open(filename)
        config = file.read()
    except FileNotFoundError:
        print("Config file not found")
        config = "default_config"
    else:
        # Runs only if no exception
        print(f"Successfully loaded {len(config)} bytes")
    finally:
        # ALWAYS runs, even if there's an error
        if file:
            file.close()
            print("File closed")
    
    return config

# The modern way with context managers
def read_config_modern(filename):
    try:
        with open(filename) as f:  # Automatically closes file
            config = f.read()
    except FileNotFoundError:
        config = "default_config"
    else:
        print("Config loaded successfully")
    
    return config
