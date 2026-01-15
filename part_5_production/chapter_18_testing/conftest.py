# From: AI Agents Book, Chapter 18, Section 18.2
# File: conftest.py
# Description: Shared pytest fixtures for integration tests

import os
import pytest
from unittest.mock import MagicMock
from dotenv import load_dotenv

# Load .env file for tests that need API keys
load_dotenv()


@pytest.fixture
def mock_llm():
    """Standard mock LLM for integration tests."""
    llm = MagicMock()
    llm.invoke.return_value = MagicMock(content="Mock response")
    return llm


@pytest.fixture
def configured_mock_llm():
    """Mock LLM that can be configured with specific responses."""
    def _create_mock(responses: list[str]):
        llm = MagicMock()
        llm.invoke.side_effect = [
            MagicMock(content=r) for r in responses
        ]
        return llm
    return _create_mock
