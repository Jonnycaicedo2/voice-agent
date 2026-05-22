"""Tests for LLM processor module."""

import pytest
from backend.llm.processor import MockProcessor, OpenAIProcessor


class TestMockProcessor:
    """Tests for the mock LLM processor."""

    async def test_returns_fixed_response(self):
        """Mock should return the configured response."""
        llm = MockProcessor(fixed_response="test response")
        result = await llm.generate("Hello")
        assert result == "test response"

    async def test_default_response(self):
        """Mock should have a sensible default response."""
        llm = MockProcessor()
        result = await llm.generate("Hi there")
        assert isinstance(result, str)
        assert len(result) > 0

    async def test_maintains_history(self):
        """Should maintain conversation history."""
        llm = MockProcessor()
        await llm.generate("Question 1")
        await llm.generate("Question 2")
        assert len(llm.history) == 4


class TestOpenAIProcessor:
    """Tests for the OpenAI processor."""

    async def test_requires_api_key(self):
        """Should require an API key."""
        llm = OpenAIProcessor(api_key="sk-test")
        assert llm.api_key == "sk-test"
        assert llm.model == "gpt-4o-mini"

    async def test_custom_model(self):
        """Should accept custom model."""
        llm = OpenAIProcessor(api_key="sk-test", model="gpt-4")
        assert llm.model == "gpt-4"

    async def test_system_prompt(self):
        """Should accept custom system prompt."""
        llm = OpenAIProcessor(api_key="sk-test",
                              system_prompt="You are a pirate.")
        assert "pirate" in llm.system_prompt