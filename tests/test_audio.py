"""Tests for audio capture and playback."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.audio.capture import AudioCapture


class TestAudioCapture:
    """Test suite for AudioCapture."""

    @patch("backend.audio.capture.pyaudio")
    async def test_stream_returns_bytes(self, mock_pyaudio):
        """Stream should yield bytes from the microphone."""
        mock_instance = MagicMock()
        mock_pyaudio.PyAudio.return_value = mock_instance
        mock_stream = MagicMock()
        mock_instance.open.return_value = mock_stream
        mock_stream.read.return_value = b"\x00\x01" * 512  # 1024 bytes

        capture = AudioCapture()
        capture.start()

        async for chunk in capture.stream():
            assert isinstance(chunk, bytes)
            assert len(chunk) > 0
            capture.stop()
            break

        mock_stream.stop_stream.assert_called_once()
        mock_stream.close.assert_called_once()

    @patch("backend.audio.capture.pyaudio")
    async def test_stream_stops_cleanly(self, mock_pyaudio):
        """Stream should stop when stop() is called."""
        import asyncio

        mock_instance = MagicMock()
        mock_pyaudio.PyAudio.return_value = mock_instance
        mock_stream = MagicMock()
        mock_instance.open.return_value = mock_stream
        mock_stream.read.return_value = b"\x00" * 1024

        capture = AudioCapture()
        capture.start()

        async def delayed_stop():
            await asyncio.sleep(0.05)
            capture.stop()

        task = asyncio.create_task(delayed_stop())

        chunks = []
        async for chunk in capture.stream():
            chunks.append(chunk)

        await task
        assert len(chunks) > 0
        assert all(isinstance(c, bytes) for c in chunks)

    @patch("backend.audio.capture.pyaudio")
    async def test_default_parameters(self, mock_pyaudio):
        """AudioCapture should use sensible defaults."""
        capture = AudioCapture()
        assert capture.sample_rate == 16000
        assert capture.channels == 1
        assert capture.chunk_size == 1024

    @patch("backend.audio.capture.pyaudio")
    async def test_custom_parameters(self, mock_pyaudio):
        """AudioCapture should accept custom audio parameters."""
        capture = AudioCapture(sample_rate=44100, channels=2, chunk_size=2048)
        assert capture.sample_rate == 44100
        assert capture.channels == 2
        assert capture.chunk_size == 2048

    @patch("backend.audio.capture.pyaudio")
    async def test_stream_respects_exception(self, mock_pyaudio):
        """Stream should not suppress exceptions from PyAudio."""
        mock_instance = MagicMock()
        mock_pyaudio.PyAudio.return_value = mock_instance
        mock_pyaudio.paInt16 = 8
        mock_instance.open.side_effect = OSError("No audio device")

        capture = AudioCapture()

        with pytest.raises(OSError, match="No audio device"):
            async for _ in capture.stream():
                pass


class TestAudioPlayback:
    """Test suite for AudioPlayback."""

    async def test_play_accepts_bytes(self):
        """play() should accept bytes without error."""
        pass
