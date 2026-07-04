from app.agents.base import BaseAgent
from app.services.ai.prompts import PROMPTS


class FirmwareEngineerAgent(BaseAgent):
    """Agent 4: Generates complete firmware code."""

    async def execute(self, input_data: dict) -> dict:
        import json
        spec = input_data.get("spec", {})
        components = input_data.get("components", [])
        connections = input_data.get("connections", [])

        prompt = f"""Generate complete, compilable firmware for this project:

Platform: {spec.get('platform', 'ESP32')}
MCU: {spec.get('mcu', 'ESP32')}

Specification:
{json.dumps(spec, indent=2)}

Components:
{json.dumps(components, indent=2)}

Connections:
{json.dumps(connections, indent=2)}

Generate complete Arduino/PlatformIO code with:
- Pin definitions
- Sensor initialization and reading
- Display output (if applicable)
- WiFi connectivity and web server (if applicable)
- Power management
- Error handling
- Serial debug output
- OTA update support (if WiFi)"""

        code, tokens = await self.generate(
            prompt=prompt,
            system_prompt=PROMPTS["firmware_engineer"],
            max_tokens=16384,
        )
        return {"firmware": code, "tokens": tokens}
