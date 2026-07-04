from app.agents.base import BaseAgent
from app.services.ai.prompts import PROMPTS


class ProjectPlannerAgent(BaseAgent):
    """Agent 1: Analyzes natural language and creates hardware specifications."""

    async def execute(self, input_data: dict) -> dict:
        prompt = input_data.get("prompt", "")
        spec, tokens = await self.generate_json(
            prompt=prompt,
            system_prompt=PROMPTS["project_analyst"],
        )
        return {"spec": spec, "tokens": tokens}
