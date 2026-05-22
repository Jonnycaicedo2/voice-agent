"""Tests for audio capture and playback."""

import asyncio
from unittest.mock import MagicMock, patch

import pytest

from backend.audio.capture import AudioCapture
from backend.audio.playback import AudioPlayback


class TestAudioCapture:
    """Test suite for AudioCapture."""

    @patch("backend.audio.capture.pyaudio")
    async def test_stream_returns_bytes(self, mock_pyaudio):
        """Stream should yield bytes from the microphone."""
        mock_pyaudio.paInt16 = 8
        mock_instance = MagicMock()
        mock_pyaudio.PyAudio.return_value = mock_instance
        mock_stream = MagicMock()
        mock_instance.open.return_value = mock_stream
        mock_stream.read.return_value = b"\x00\x01" * 512

        capture = AudioCapture()
        capture.start()

        # Get first chunk and stop immediately
        stream_gen = capture.stream()
        chunk = await stream_gen.__anext__()
        capture.stop()

        assert isinstance(chunk, bytes)
        assert len(chunk) > 0

    @patch("backend.audio.capture.pyaudio")
    async def test_stop_event_set(self, mock_pyaudio):
        """stop() should set the stop event."""
        capture = AudioCapture()
        assert not capture._stop_event.is_set()
        capture.stop()
        assert capture._stop_event.is_set()

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
        """Stream should raise OSError when no audio device."""
        mock_pyaudio.paInt16 = 8
        mock_instance = MagicMock()
        mock_pyaudio.PyAudio.return_value = mock_instance
        mock_instance.open.side_effect = OSError("No audio device")

        capture = AudioCapture()

        with pytest.raises(OSError, match="No audio device"):
            stream_gen = capture.stream()
            await stream_gen.__anext__()


class TestAudioPlayback:
    """Test suite for AudioPlayback."""

    @patch("backend.audio.playback.pyaudio")
    async def test_play_accepts_bytes(self, mock_pyaudio):
        """play() should accept bytes without error."""
        mock_pyaudio.paInt16 = 8
        mock_instance = MagicMock()
        mock_pyaudio.PyAudio.return_value = mock_instance
        mock_stream = MagicMock()
        mock_instance.open.return_value = mock_stream

        playback = AudioPlayback()
        await playback.play(b"\x00\x01" * 512)
        await asyncio.sleep(0.15)
        await playback.stop()

        mock_stream.write.assert_called_once()

    @patch("backend.audio.playback.pyaudio")
    async def test_play_multiple_chunks(self, mock_pyaudio):
        """Multiple chunks should play sequentially."""
        mock_pyaudio.paInt16 = 8
        mock_instance = MagicMock()
        mock_pyaudio.PyAudio.return_value = mock_instance
        mock_stream = MagicMock()
        mock_instance.open.return_value = mock_stream

        playback = AudioPlayback()
        await playback.play(b"\x00" * 512)
        await playback.play(b"\xff" * 512)
        await playback.play(b"\xaa" * 512)
        await asyncio.sleep(0.2)
        await playback.stop()

        assert mock_stream.write.call_count == 3

    @patch("backend.audio.playback.pyaudio")
    async def test_default_parameters(self, mock_pyaudio):
        """AudioPlayback should use sensible defaults."""
        mock_pyaudio.paInt16 = 8
        playback = AudioPlayback()
        assert playback.sample_rate == 16000
        assert playback.channels == 1
        assert playback.chunk_size == 1024

    @patch("backend.audio.playback.pyaudio")
    async def test_stop_without_play(self, mock_pyaudio):
        """stop() should be safe to call even if play() was never called."""
        mock_pyaudio.paInt16 = 8
        playback = AudioPlayback()
        await playback.stop()  # should not raise