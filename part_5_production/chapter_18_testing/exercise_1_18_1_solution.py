# From: AI Agents Book, Chapter 18, Section 18.1
# File: exercise_1_18_1_solution.py
# Description: Exercise 1 Solution - Email validation tool with comprehensive tests

import pytest
import re


# The tool function
def validate_email(email: str) -> dict:
    """Validate an email address and return detailed results."""
    if not email or not isinstance(email, str):
        return {
            "valid": False,
            "error": "Email must be a non-empty string",
            "normalized": None
        }
    
    # Normalize the email
    normalized = email.strip().lower()
    
    # Basic regex pattern for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email.strip()):
        return {
            "valid": False,
            "error": "Invalid email format",
            "normalized": normalized
        }
    
    # Check for common issues
    if ".." in normalized:
        return {
            "valid": False,
            "error": "Email cannot contain consecutive dots",
            "normalized": normalized
        }
    
    return {
        "valid": True,
        "error": None,
        "normalized": normalized
    }


# The tests
class TestValidateEmail:
    """Tests for the validate_email function."""
    
    def test_valid_simple_email(self):
        """Test a standard valid email."""
        result = validate_email("user@example.com")
        
        assert result["valid"] is True
        assert result["error"] is None
        assert result["normalized"] == "user@example.com"
    
    def test_valid_email_with_plus(self):
        """Test email with plus addressing."""
        result = validate_email("user+tag@example.com")
        
        assert result["valid"] is True
        assert result["normalized"] == "user+tag@example.com"
    
    def test_valid_email_with_dots(self):
        """Test email with dots in local part."""
        result = validate_email("first.last@example.com")
        
        assert result["valid"] is True
    
    def test_valid_email_normalized_to_lowercase(self):
        """Test that emails are normalized to lowercase."""
        result = validate_email("User@EXAMPLE.COM")
        
        assert result["valid"] is True
        assert result["normalized"] == "user@example.com"
    
    def test_valid_email_with_subdomain(self):
        """Test email with subdomain."""
        result = validate_email("user@mail.example.com")
        
        assert result["valid"] is True
    
    def test_invalid_no_at_symbol(self):
        """Test email without @ symbol."""
        result = validate_email("userexample.com")
        
        assert result["valid"] is False
        assert result["error"] == "Invalid email format"
    
    def test_invalid_no_domain(self):
        """Test email without domain."""
        result = validate_email("user@")
        
        assert result["valid"] is False
    
    def test_invalid_no_tld(self):
        """Test email without TLD."""
        result = validate_email("user@example")
        
        assert result["valid"] is False
    
    def test_invalid_consecutive_dots(self):
        """Test email with consecutive dots."""
        result = validate_email("user..name@example.com")
        
        assert result["valid"] is False
        assert "consecutive dots" in result["error"]
    
    def test_empty_string(self):
        """Test empty string input."""
        result = validate_email("")
        
        assert result["valid"] is False
        assert "non-empty string" in result["error"]
        assert result["normalized"] is None
    
    def test_none_input(self):
        """Test None input."""
        result = validate_email(None)
        
        assert result["valid"] is False
        assert result["normalized"] is None
    
    def test_whitespace_trimmed(self):
        """Test that whitespace is trimmed."""
        result = validate_email("  user@example.com  ")
        
        assert result["valid"] is True
        assert result["normalized"] == "user@example.com"
