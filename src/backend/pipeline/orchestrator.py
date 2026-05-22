"""Pipeline orchestrator connecting all voice agent components."""

import asyncio

from backend.audio.capture import AudioCapture
from backend.audio.playback import AudioPlayback
from backend.stt.transcriber import STTTranscriber
from backend.llm.processor import LLMProcessor
from backend.tts.synthesizer import TTSSynthesizer


class PipelineOrchestrator:
    """Orchestrates the voice pipeline: Mic -> STT -> LLM -> TTS -> Speaker."""

    def __init__(
        self,
        capture: AudioCapture,
        transcriber: STTTranscriber,
        llm: LLMProcessor,
        synthesizer: TTSSynthesizer,
        playback: AudioPlayback,
    ):
        self.capture = capture
        self.transcriber = transcriber
        self.llm = llm
        self.synthesizer = synthesizer
        self.playback = playback
        self._running = False
        self._task: asyncio.Task | None = None

    async def start(self) -> None:
        """Start the voice pipeline."""
        self._running = True
        self.capture.start()
        self._task = asyncio.create_task(self._run_pipeline())

    async def stop(self) -> None:
        """Stop the voice pipeline gracefully."""
        self._running = False
        self.capture.stop()
        await self.playback.stop()
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    async def _run_pipeline(self) -> None:
        """Main pipeline loop: capture -> transcribe -> generate -> synthesize -> play."""
        async for audio_chunk in self.capture.stream():
            if not self._running:
                break

            text = await self.transcriber.transcribe(audio_chunk)
            response = await self.llm.generate(text)
            audio = await self.synthesizer.synthesize(response)
            await self.playback.play(audio)