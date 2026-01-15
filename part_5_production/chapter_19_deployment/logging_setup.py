# From: Zero to AI Agent, Chapter 19, Section 19.4
# File: logging_setup.py

import logging
import json
from datetime import datetime, timezone


class JSONFormatter(logging.Formatter):
    """Format log records as JSON for easy parsing by cloud platforms."""
    
    def format(self, record):
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        # Add extra fields if present
        if hasattr(record, "conversation_id"):
            log_data["conversation_id"] = record.conversation_id
        if hasattr(record, "processing_time_ms"):
            log_data["processing_time_ms"] = record.processing_time_ms
            
        return json.dumps(log_data)


def setup_logging(name: str = "agent_api", level: int = logging.INFO):
    """Set up JSON logging for production use."""
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    
    logger = logging.getLogger(name)
    logger.handlers = []  # Remove existing handlers
    logger.addHandler(handler)
    logger.setLevel(level)
    
    return logger


# Example usage
if __name__ == "__main__":
    logger = setup_logging()
    
    # Basic logging
    logger.info("Application started")
    logger.warning("This is a warning")
    logger.error("This is an error")
    
    # Output will be JSON:
    # {"timestamp": "2024-01-15T10:30:45.123456+00:00", "level": "INFO", ...}
