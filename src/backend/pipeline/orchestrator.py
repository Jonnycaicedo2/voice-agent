"""Main pipeline orchestrator connecting all stages."""


class PipelineOrchestrator:
    """Coordinates the voice pipeline: mic → STT → LLM → TTS → speaker."""

    async def run(self) -> None:
        """Run the conversation loop."""
