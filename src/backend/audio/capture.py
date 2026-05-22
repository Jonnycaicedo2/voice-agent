"""Microphone audio capture using asyncio."""


class AudioCapture:
    """Captures audio from the microphone in an async generator."""

    async def stream(self):
        """Yield raw audio chunks from the microphone."""
        yield b""
