"""Text-to-Speech synthesis using external APIs."""

from abc import ABC, abstractmethod


class TTSSynthesizer(ABC):
    """Abstract interface for text-to-speech engines."""

    @abstractmethod
    async def synthesize(self, text: str) -> bytes:
        """Convert text to audio bytes."""
        ...


class OpenAITTSSynthesizer(TTSSynthesizer):
    """TTS using OpenAI TTS API."""

    def __init__(self, api_key: str, model: str = "tts-1",
                 voice: str = "alloy"):
        self.api_key = api_key
        self.model = model
        self.voice = voice

    async def synthesize(self, text: str) -> bytes:
        """Synthesize text to audio via OpenAI TTS API."""
        import aiohttp

        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            body = {
                "model": self.model,
                "input": text,
                "voice": self.voice,
            }

            async with session.post(
                "https://api.openai.com/v1/audio/speech",
                json=body,
                headers=headers,
            ) as resp:
                if resp.status != 200:
                    raise RuntimeError(f"OpenAI TTS error: {await resp.text()}")
                return await resp.read()


class MockSynthesizer(TTSSynthesizer):
    """Mock TTS for testing without API calls."""

    def __init__(self, fixed_audio: bytes = b"\x00\x01" * 512):
        self.fixed_audio = fixed_audio

    async def synthesize(self, text: str) -> bytes:
        """Return fixed audio bytes regardless of input."""
        return self.fixed_audio