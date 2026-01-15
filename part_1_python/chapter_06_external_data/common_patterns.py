# From: Zero to AI Agent, Chapter 6, Section 6.4
# File: 08_common_patterns.py


import json
import os

# Pattern 1: Default values
def get_config(key, default=None):
    try:
        with open('config.json') as f:
            config = json.load(f)
            return config.get(key, default)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

# Pattern 2: Validation loops
def get_choice(options):
    while True:
        try:
            choice = int(input(f"Choose (1-{len(options)}): "))
            if 1 <= choice <= len(options):
                return choice
            print(f"Please choose between 1 and {len(options)}")
        except ValueError:
            print("Please enter a number")

# Pattern 3: Resource cleanup
class DatabaseConnection:
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        # Return False to propagate any exception

# Pattern 4: Graceful degradation
def get_user_location():
    try:
        return get_gps_location()
    except GPSError:
        try:
            return get_ip_location()
        except NetworkError:
            return get_default_location()
