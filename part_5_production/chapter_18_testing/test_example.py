# From: AI Agents Book, Chapter 18, Section 18.1
# File: test_example.py
# Description: Basic pytest examples to get started with testing

def test_addition():
    """Our very first test!"""
    result = 2 + 2
    assert result == 4


def test_string_contains():
    """Test that a string contains expected text."""
    message = "Hello, World!"
    assert "World" in message


def test_list_length():
    """Test the length of a list."""
    items = [1, 2, 3, 4, 5]
    assert len(items) == 5


def test_that_fails():
    """This test will fail - on purpose! 
    Uncomment to see what failure output looks like."""
    # result = 2 + 2
    # assert result == 5, "Math is broken!"
    pass
