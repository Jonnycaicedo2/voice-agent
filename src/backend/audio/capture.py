"""Microphone audio capture using asyncio."""

import asyncio

import pyaudio


class AudioCapture:
    """Captures audio from the microphone in an async generator.

    Uses PyAudio to read raw audio chunks from the default input device.
    The async generator ``stream()`` yields ``bytes`` until ``stop()`` is called.
    """

    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        chunk_size: int = 1024,
        format: int = pyaudio.paInt16,
    ):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.format = format
        self._stop_event = asyncio.Event()

    def start(self) -> None:
        """Clear the stop flag so that ``stream()`` can run."""
        self._stop_event.clear()

    def stop(self) -> None:
        """Signal ``stream()`` to stop and exit cleanly."""
        self._stop_event.set()

    async def stream(self):
        """Async generator that yields raw audio chunks from the microphone.

        Opens a PyAudio input stream and reads ``chunk_size``-sized blocks
        in a loop.  Each block is yielded as ``bytes``.  The generator
        terminates when ``stop()`` is called or if PyAudio raises an error.

        Yields:
            bytes: Raw PCM audio data (little-endian 16-bit signed ints).
        """
        audio = pyaudio.PyAudio()
        try:
            stream = audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size,
            )
        except OSError:
            audio.terminate()
            raise

        try:
            while not self._stop_event.is_set():
                data = stream.read(self.chunk_size)
                yield data
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()
