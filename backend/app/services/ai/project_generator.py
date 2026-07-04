import json
import logging
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import async_session
from app.models.project import Project, ProjectStatus
from app.services.ai.ai_service import AIService
from app.services.ai.prompts import PROMPTS

logger = logging.getLogger(__name__)


class ProjectGeneratorService:
    def __init__(self):
        self.ai = AIService()

    async def generate(self, project_id: str, prompt: str, model: str = "gemini"):
        async with async_session() as db:
            try:
                result = await db.execute(
                    __import__("sqlalchemy").select(Project).where(Project.id == UUID(project_id))
                )
                project = result.scalar_one_or_none()
                if not project:
                    logger.error(f"Project {project_id} not found")
                    return

                spec = await self._analyze_requirements(prompt, model)
                components = await self._select_components(spec, model)
                connections = await self._design_circuit(spec, components, model)
                netlist = self._generate_netlist(components, connections)
                schematic = self._generate_schematic_data(components, connections)
                pcb = self._generate_pcb_data(components, schematic)
                bom = self._generate_bom(components)
                firmware = await self._generate_firmware(spec, components, model)
                documentation = await self._generate_docs(spec, components, connections, model)

                project.components = components
                project.connections = connections
                project.netlist = netlist
                project.schematic_data = schematic
                project.pcb_data = pcb
                project.bom = bom
                project.firmware_code = firmware
                project.documentation = documentation
                project.status = ProjectStatus.COMPLETED
                project.project_metadata = {"spec": spec, "model_used": model}

                await db.commit()
                logger.info(f"Project {project_id} generation completed")

            except Exception as e:
                logger.error(f"Project generation failed: {e}")
                result = await db.execute(
                    __import__("sqlalchemy").select(Project).where(Project.id == UUID(project_id))
                )
                project = result.scalar_one_or_none()
                if project:
                    project.status = ProjectStatus.ERROR
                    project.project_metadata = {"error": str(e)}
                    await db.commit()

    async def _analyze_requirements(self, prompt: str, model: str) -> dict:
        system_prompt = PROMPTS["project_analyst"]
        spec, _ = await self.ai.generate_json(prompt, system_prompt, model)
        return spec

    async def _select_components(self, spec: dict, model: str) -> list[dict]:
        prompt = f"Select components for this hardware specification:\n{json.dumps(spec, indent=2)}"
        system_prompt = PROMPTS["component_selector"]
        result, _ = await self.ai.generate_json(prompt, system_prompt, model)
        return result.get("components", [])

    async def _design_circuit(self, spec: dict, components: list[dict], model: str) -> list[dict]:
        prompt = f"""Design circuit connections for:
Specification: {json.dumps(spec, indent=2)}
Components: {json.dumps(components, indent=2)}"""
        system_prompt = PROMPTS["circuit_designer"]
        result, _ = await self.ai.generate_json(prompt, system_prompt, model)
        return result.get("connections", [])

    def _generate_netlist(self, components: list[dict], connections: list[dict]) -> list[dict]:
        netlist = []
        for conn in connections:
            netlist.append({
                "net_name": conn.get("net_name", ""),
                "components": conn.get("pins", []),
            })
        return netlist

    def _generate_schematic_data(self, components: list[dict], connections: list[dict]) -> dict:
        placed = []
        x_offset = 50
        y_offset = 50
        for i, comp in enumerate(components):
            placed.append({
                "id": comp.get("ref", f"U{i}"),
                "type": comp.get("type", ""),
                "value": comp.get("value", ""),
                "package": comp.get("package", ""),
                "x": x_offset + (i % 5) * 200,
                "y": y_offset + (i // 5) * 150,
                "rotation": 0,
                "pins": comp.get("pins", []),
            })
        return {"components": placed, "connections": connections}

    def _generate_pcb_data(self, components: list[dict], schematic: dict) -> dict:
        board_width = 80
        board_height = 60
        placed = []
        x_pos = 10
        y_pos = 10
        for i, comp in enumerate(components):
            placed.append({
                "id": comp.get("ref", f"U{i}"),
                "footprint": comp.get("package", "SMD"),
                "x": x_pos,
                "y": y_pos,
                "rotation": 0,
                "layer": "F.Cu" if i % 2 == 0 else "B.Cu",
            })
            x_pos += 20
            if x_pos > board_width - 10:
                x_pos = 10
                y_pos += 15

        return {
            "board": {"width": board_width, "height": board_height, "layers": 2},
            "components": placed,
            "tracks": [],
            "vias": [],
            "copper_pours": [{"net": "GND", "layer": "F.Cu", "clearance": 0.2}],
        }

    def _generate_bom(self, components: list[dict]) -> list[dict]:
        bom = []
        for comp in components:
            bom.append({
                "ref": comp.get("ref", ""),
                "name": comp.get("type", ""),
                "value": comp.get("value", ""),
                "package": comp.get("package", ""),
                "quantity": comp.get("quantity", 1),
                "manufacturer": comp.get("manufacturer", ""),
                "part_number": comp.get("part_number", ""),
                "price": comp.get("price", 0.0),
                "supplier": comp.get("supplier", ""),
                "datasheet": comp.get("datasheet", ""),
                "alternatives": comp.get("alternatives", []),
            })
        return bom

    async def _generate_firmware(self, spec: dict, components: list[dict], model: str) -> str:
        prompt = f"""Generate complete firmware for this project:
Platform: {spec.get('platform', 'ESP32')}
Specification: {json.dumps(spec, indent=2)}
Components: {json.dumps(components, indent=2)}"""
        system_prompt = PROMPTS["firmware_engineer"]
        text, _ = await self.ai.generate(prompt, system_prompt, model, max_tokens=16384)
        return text

    async def _generate_docs(self, spec: dict, components: list[dict], connections: list[dict], model: str) -> str:
        prompt = f"""Generate complete documentation for this hardware project:
Specification: {json.dumps(spec, indent=2)}
Components: {json.dumps(components, indent=2)}
Connections: {json.dumps(connections, indent=2)}"""
        system_prompt = PROMPTS["documentation_writer"]
        text, _ = await self.ai.generate(prompt, system_prompt, model)
        return text
