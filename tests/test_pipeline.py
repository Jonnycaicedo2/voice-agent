"""Tests for pipeline orchestrator."""

import asyncio
import pytest

from backend.audio.capture import AudioCapture
from backend.audio.playback import AudioPlayback
from backend.stt.transcriber import MockTranscriber
from backend.llm.processor import MockProcessor
from backend.tts.synthesizer import MockSynthesizer
from backend.pipeline.orchestrator import PipelineOrchestrator


class TestPipelineOrchestrator:
    """Tests for the pipeline orchestrator."""

    async def test_pipeline_components_injected(self):
        """All components should be injectable."""
        capture = AudioCapture()
        transcriber = MockTranscriber()
        llm = MockProcessor()
        synthesizer = MockSynthesizer()
        playback = AudioPlayback()

        orchestrator = PipelineOrchestrator(
            capture=capture,
            transcriber=transcriber,
            llm=llm,
            synthesizer=synthesizer,
            playback=playback,
        )

        assert orchestrator.capture is capture
        assert orchestrator.transcriber is transcriber
        assert orchestrator.llm is llm
        assert orchestrator.synthesizer is synthesizer
        assert orchestrator.playback is playback

    async def test_stop_when_not_running_is_safe(self):
        """stop() should be safe to call even if pipeline never started."""
        orchestrator = PipelineOrchestrator(
            capture=AudioCapture(),
            transcriber=MockTranscriber(),
            llm=MockProcessor(),
            synthesizer=MockSynthesizer(),
            playback=AudioPlayback(),
        )

        await orchestrator.stop()  # should not raise