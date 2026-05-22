"""Audio playback to speaker using asyncio."""


class AudioPlayback:
    """Plays audio chunks to the speaker."""

    async def play(self, chunk: bytes) -> None:
        """Play a single audio chunk."""
