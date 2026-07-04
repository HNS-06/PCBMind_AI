from app.agents.base import BaseAgent
from app.services.ai.prompts import PROMPTS


class DocumentationWriterAgent(BaseAgent):
    """Agent 5: Generates project documentation."""

    async def execute(self, input_data: dict) -> dict:
        import json
        spec = input_data.get("spec", {})
        components = input_data.get("components", [])
        connections = input_data.get("connections", [])
        bom = input_data.get("bom", [])

        prompt = f"""Generate comprehensive documentation for this hardware project:

Project: {spec.get('project_name', 'Hardware Project')}
Description: {spec.get('description', '')}

Specification:
{json.dumps(spec, indent=2)}

Components: {len(components)} total
BOM Cost: ${sum(item.get('price', 0) for item in bom):.2f}

Generate complete documentation with all sections."""

        doc, tokens = await self.generate(
            prompt=prompt,
            system_prompt=PROMPTS["documentation_writer"],
            max_tokens=16384,
        )
        return {"documentation": doc, "tokens": tokens}
