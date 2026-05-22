"""LLM processor for generating conversational responses."""

from abc import ABC, abstractmethod


class LLMProcessor(ABC):
    """Abstract interface for LLM-based response generation."""

    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """Generate a response from the LLM."""
        ...


class OpenAIProcessor(LLMProcessor):
    """LLM implementation using OpenAI Chat Completions API."""

    def __init__(self, api_key: str, model: str = "gpt-4o-mini",
                 system_prompt: str = "You are a helpful voice assistant."):
        self.api_key = api_key
        self.model = model
        self.system_prompt = system_prompt
        self.history: list[dict] = []

    async def generate(self, prompt: str) -> str:
        """Send prompt to OpenAI and return response."""
        import aiohttp

        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.history)
        messages.append({"role": "user", "content": prompt})

        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            body = {
                "model": self.model,
                "messages": messages,
            }

            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                json=body,
                headers=headers,
            ) as resp:
                if resp.status != 200:
                    raise RuntimeError(f"OpenAI API error: {await resp.text()}")
                result = await resp.json()
                response = result["choices"][0]["message"]["content"]

        self.history.append({"role": "user", "content": prompt})
        self.history.append({"role": "assistant", "content": response})
        return response


class MockProcessor(LLMProcessor):
    """Mock LLM for testing without API calls."""

    def __init__(self, fixed_response: str = "I'm doing great, thanks!"):
        self.fixed_response = fixed_response
        self.history: list[dict] = []

    async def generate(self, prompt: str) -> str:
        """Return a fixed response and log the prompt."""
        self.history.append({"role": "user", "content": prompt})
        self.history.append({"role": "assistant", "content": self.fixed_response})
        return self.fixed_response