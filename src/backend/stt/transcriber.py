"""Speech-to-Text transcription using external APIs."""

from abc import ABC, abstractmethod


class STTTranscriber(ABC):
    """Abstract interface for speech-to-text engines."""

    @abstractmethod
    async def transcribe(self, audio_bytes: bytes) -> str:
        """Convert audio bytes to text."""
        ...


class WhisperTranscriber(STTTranscriber):
    """STT using OpenAI Whisper API."""

    def __init__(self, api_key: str, model: str = "whisper-1"):
        self.api_key = api_key
        self.model = model

    async def transcribe(self, audio_bytes: bytes) -> str:
        """Transcribe audio via Whisper API."""
        import aiohttp

        async with aiohttp.ClientSession() as session:
            form = aiohttp.FormData()
            form.add_field("model", self.model)
            form.add_field("file", audio_bytes, filename="audio.wav",
                           content_type="audio/wav")
            headers = {"Authorization": f"Bearer {self.api_key}"}

            async with session.post(
                "https://api.openai.com/v1/audio/transcriptions",
                data=form,
                headers=headers,
            ) as resp:
                if resp.status != 200:
                    raise RuntimeError(f"Whisper API error: {await resp.text()}")
                result = await resp.json()
                return result["text"]


class MockTranscriber(STTTranscriber):
    """Mock STT for testing without API calls."""

    def __init__(self, fixed_response: str = "Hello, how are you?"):
        self.fixed_response = fixed_response

    async def transcribe(self, audio_bytes: bytes) -> str:
        """Return a fixed response regardless of input."""
        return self.fixed_response