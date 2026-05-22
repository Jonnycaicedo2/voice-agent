"""Tests for Text-to-Speech module."""

import pytest
from backend.tts.synthesizer import MockSynthesizer, OpenAITTSSynthesizer


class TestMockSynthesizer:
    """Tests for the mock TTS synthesizer."""

    async def test_returns_bytes(self):
        """Mock should return audio bytes."""
        tts = MockSynthesizer()
        result = await tts.synthesize("Hello world")
        assert isinstance(result, bytes)
        assert len(result) > 0

    async def test_custom_audio(self):
        """Mock should return configured bytes."""
        custom = b"\xff" * 256
        tts = MockSynthesizer(fixed_audio=custom)
        result = await tts.synthesize("test")
        assert result == custom


class TestOpenAITTSSynthesizer:
    """Tests for the OpenAI TTS synthesizer."""

    async def test_requires_api_key(self):
        """Should require an API key."""
        tts = OpenAITTSSynthesizer(api_key="sk-test")
        assert tts.api_key == "sk-test"
        assert tts.model == "tts-1"

    async def test_custom_model_and_voice(self):
        """Should accept custom model and voice."""
        tts = OpenAITTSSynthesizer(api_key="sk-test", model="tts-1-hd",
                                   voice="nova")
        assert tts.model == "tts-1-hd"
        assert tts.voice == "nova"