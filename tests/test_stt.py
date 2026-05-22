"""Tests for Speech-to-Text module."""

import pytest
from backend.stt.transcriber import MockTranscriber, WhisperTranscriber


class TestMockTranscriber:
    """Tests for the mock STT transcriber."""

    async def test_returns_fixed_response(self):
        """Mock should return the configured response."""
        transcriber = MockTranscriber(fixed_response="test output")
        result = await transcriber.transcribe(b"\x00" * 1024)
        assert result == "test output"

    async def test_default_response(self):
        """Mock should have a sensible default response."""
        transcriber = MockTranscriber()
        result = await transcriber.transcribe(b"\x00" * 1024)
        assert isinstance(result, str)
        assert len(result) > 0

    async def test_accepts_bytes(self):
        """transcribe() should accept bytes input."""
        transcriber = MockTranscriber()
        result = await transcriber.transcribe(b"\x00\x01\x02\x03")
        assert isinstance(result, str)


class TestWhisperTranscriber:
    """Tests for the Whisper API transcriber."""

    async def test_requires_api_key(self):
        """WhisperTranscriber should require an API key."""
        transcriber = WhisperTranscriber(api_key="sk-test")
        assert transcriber.api_key == "sk-test"
        assert transcriber.model == "whisper-1"

    async def test_custom_model(self):
        """Should accept custom model parameter."""
        transcriber = WhisperTranscriber(api_key="sk-test", model="whisper-2")
        assert transcriber.model == "whisper-2"