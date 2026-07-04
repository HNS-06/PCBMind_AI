from abc import ABC, abstractmethod
from app.services.ai.ai_service import AIService


class BaseAgent(ABC):
    def __init__(self, model: str = "gemini"):
        self.ai = AIService()
        self.model = model

    @abstractmethod
    async def execute(self, input_data: dict) -> dict:
        pass

    async def generate(self, prompt: str, system_prompt: str, **kwargs) -> tuple[str, dict]:
        return await self.ai.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            model=kwargs.get("model", self.model),
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 8192),
        )

    async def generate_json(self, prompt: str, system_prompt: str, **kwargs) -> tuple[dict, dict]:
        return await self.ai.generate_json(
            prompt=prompt,
            system_prompt=system_prompt,
            model=kwargs.get("model", self.model),
            temperature=kwargs.get("temperature", 0.3),
        )
