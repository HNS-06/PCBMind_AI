from app.agents.base import BaseAgent
from app.services.ai.prompts import PROMPTS


class DesignReviewerAgent(BaseAgent):
    """Reviews circuit design for issues and improvements."""

    async def execute(self, input_data: dict) -> dict:
        import json
        components = input_data.get("components", [])
        connections = input_data.get("connections", [])
        schematic = input_data.get("schematic_data", {})
        pcb_data = input_data.get("pcb_data", {})

        prompt = f"""Review this complete hardware design:

Components:
{json.dumps(components, indent=2)}

Connections:
{json.dumps(connections, indent=2)}

Schematic Data:
{json.dumps(schematic, indent=2)}

PCB Data:
{json.dumps(pcb_data, indent=2)}

Perform a thorough design review. Check for electrical issues,
manufacturing problems, and optimization opportunities."""

        review, tokens = await self.generate_json(
            prompt=prompt,
            system_prompt=PROMPTS["design_reviewer"],
        )
        return {"review": review, "tokens": tokens}
