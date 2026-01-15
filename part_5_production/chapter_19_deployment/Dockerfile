# From: Zero to AI Agent, Chapter 19, Section 19.1
# File: Dockerfile

# Build stage - install dependencies
FROM python:3.13-slim as builder

WORKDIR /app

# Install dependencies into a virtual environment
COPY requirements.txt .
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage - just the essentials
FROM python:3.13-slim

WORKDIR /app

# Copy the virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY . .

# Create a non-root user for security
RUN useradd --create-home appuser
USER appuser

# Expose the port our app will use (for APIs)
EXPOSE 8000

# Default command
CMD ["python", "simple_agent.py"]
