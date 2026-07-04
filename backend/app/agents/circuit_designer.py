from app.agents.base import BaseAgent
from app.services.ai.prompts import PROMPTS


class CircuitDesignerAgent(BaseAgent):
    """Agent 2: Designs circuit connections and electrical architecture."""

    async def execute(self, input_data: dict) -> dict:
        import json
        spec = input_data.get("spec", {})
        components = input_data.get("components", [])

        prompt = f"""Design the complete circuit for this hardware project:

Specification:
{json.dumps(spec, indent=2)}

Selected Components:
{json.dumps(components, indent=2)}

Design voltage rails, signal connections, I2C/SPI buses, GPIO mapping,
power stages, and protection circuits."""

        result, tokens = await self.generate_json(
            prompt=prompt,
            system_prompt=PROMPTS["circuit_designer"],
            max_tokens=16384,
        )
        return {"circuit": result, "tokens": tokens}
