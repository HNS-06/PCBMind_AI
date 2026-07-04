from app.agents.base import BaseAgent
from app.services.ai.prompts import PROMPTS


class PCBExpertAgent(BaseAgent):
    """Agent 3: Handles PCB placement, routing, and layout optimization."""

    async def execute(self, input_data: dict) -> dict:
        import json
        components = input_data.get("components", [])
        connections = input_data.get("connections", [])
        spec = input_data.get("spec", {})

        prompt = f"""Design the PCB layout for this project:

Board Requirements:
{json.dumps(spec.get('physical', {}), indent=2)}

Components ({len(components)}):
{json.dumps(components, indent=2)}

Connections ({len(connections)}):
{json.dumps(connections, indent=2)}

Provide component placement strategy, routing guidelines, copper pour design,
and manufacturing specifications."""

        result, tokens = await self.generate_json(
            prompt=prompt,
            system_prompt=PROMPTS["pcb_designer"],
        )
        return {"pcb_design": result, "tokens": tokens}
