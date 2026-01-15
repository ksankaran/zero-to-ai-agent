# Save as: secure_logging.py
"""
Secure logging utilities that automatically redact sensitive data.
Prevents API keys, passwords, and other secrets from ending up in logs.
"""

import logging
import re
from typing import List, Tuple


class SanitizedFormatter(logging.Formatter):
    """
    Formatter that automatically redacts sensitive data from log messages.
    
    Use this instead of default formatters to prevent secrets in logs.
    """
    
    SENSITIVE_PATTERNS: List[Tuple[str, str]] = [
        # API keys
        (r'sk-[a-zA-Z0-9]+', 'sk-***REDACTED***'),
        (r'pk-[a-zA-Z0-9]+', 'pk-***REDACTED***'),
        
        # Generic secrets
        (r'password["\']?\s*[:=]\s*["\']?[^"\'\s,}]+', 'password=***REDACTED***'),
        (r'api[_-]?key["\']?\s*[:=]\s*["\']?[^"\'\s,}]+', 'api_key=***REDACTED***'),
        (r'secret["\']?\s*[:=]\s*["\']?[^"\'\s,}]+', 'secret=***REDACTED***'),
        (r'token["\']?\s*[:=]\s*["\']?[^"\'\s,}]+', 'token=***REDACTED***'),
        
        # Bearer tokens
        (r'Bearer\s+[a-zA-Z0-9\-_]+\.?[a-zA-Z0-9\-_]*\.?[a-zA-Z0-9\-_]*', 'Bearer ***REDACTED***'),
        
        # Credit card numbers (basic pattern)
        (r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', '****-****-****-****'),
    ]
    
    def __init__(self, *args, additional_patterns: List[Tuple[str, str]] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.patterns = self.SENSITIVE_PATTERNS.copy()
        if additional_patterns:
            self.patterns.extend(additional_patterns)
    
    def format(self, record: logging.LogRecord) -> str:
        """Format the log record, redacting sensitive data."""
        message = super().format(record)
        
        for pattern, replacement in self.patterns:
            message = re.sub(pattern, replacement, message, flags=re.IGNORECASE)
        
        return message


def setup_secure_logging(
    name: str = None,
    level: int = logging.INFO,
    log_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
) -> logging.Logger:
    """
    Set up a logger with sanitized output.
    
    Args:
        name: Logger name (None for root logger)
        level: Logging level
        log_format: Log message format
    
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Console handler with sanitized formatter
    handler = logging.StreamHandler()
    handler.setFormatter(SanitizedFormatter(log_format))
    logger.addHandler(handler)
    
    return logger


# Safe logging functions that always redact
def log_request(logger: logging.Logger, method: str, path: str, headers: dict = None):
    """Log an API request safely, redacting sensitive headers."""
    safe_headers = {}
    if headers:
        sensitive_headers = ['authorization', 'x-api-key', 'cookie']
        for key, value in headers.items():
            if key.lower() in sensitive_headers:
                safe_headers[key] = '***REDACTED***'
            else:
                safe_headers[key] = value
    
    logger.info(f"Request: {method} {path} headers={safe_headers}")


def log_response(logger: logging.Logger, status: int, duration_ms: float):
    """Log an API response safely."""
    logger.info(f"Response: status={status} duration={duration_ms:.2f}ms")


def log_error(logger: logging.Logger, error: Exception, context: str = ""):
    """
    Log an error safely.
    
    Logs the error type and context but NOT the full message,
    which might contain sensitive data.
    """
    error_type = type(error).__name__
    logger.error(f"Error ({error_type}) in {context}: {str(error)[:100]}")


# Example usage
if __name__ == "__main__":
    # Set up secure logger
    logger = setup_secure_logging("test_app")
    
    print("Testing secure logging - sensitive data should be redacted:\n")
    
    # These should all be redacted
    test_messages = [
        "Using API key: sk-abc123def456ghi789jkl012mno345pqr678",
        "Config: api_key='sk-secret123' password='hunter2'",
        "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test",
        "User entered credit card: 4111-1111-1111-1111",
        "Database secret = 'supersecret123'",
        "Normal message without secrets",
    ]
    
    for msg in test_messages:
        print(f"Original: {msg}")
        logger.info(msg)
        print()
    
    # Test safe request logging
    print("\nTesting safe request logging:")
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer secret-token-123",
        "X-API-Key": "sk-mysecretkey"
    }
    log_request(logger, "POST", "/api/chat", headers)
