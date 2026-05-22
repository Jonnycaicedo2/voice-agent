"""Audio playback to speaker using asyncio."""

import asyncio

import pyaudio


class AudioPlayback:
    """Plays audio chunks to the system speaker with an internal buffer queue."""

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
        self._queue: asyncio.Queue[bytes] = asyncio.Queue()
        self._stop_event = asyncio.Event()
        self._worker_task: asyncio.Task | None = None

    async def play(self, chunk: bytes) -> None:
        """Enqueue a chunk for playback.

        Starts the background worker on first call if not already running.
        """
        self._queue.put_nowait(chunk)
        if self._worker_task is None or self._worker_task.done():
            self._worker_task = asyncio.create_task(self._run())

    async def _run(self) -> None:
        """Background worker: open PyAudio output and drain the queue."""
        audio = pyaudio.PyAudio()
        try:
            stream = audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                output=True,
                frames_per_buffer=self.chunk_size,
            )
        except OSError:
            audio.terminate()
            raise

        try:
            while not self._stop_event.is_set():
                try:
                    data = await asyncio.wait_for(self._queue.get(), timeout=0.1)
                    stream.write(data)
                except asyncio.TimeoutError:
                    continue
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()

    async def stop(self) -> None:
        """Signal the worker to stop and wait for it to finish."""
        self._stop_event.set()
        if self._worker_task is not None and not self._worker_task.done():
            await self._worker_task
