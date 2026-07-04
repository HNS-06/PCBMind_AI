from app.agents.project_planner import ProjectPlannerAgent
from app.agents.circuit_designer import CircuitDesignerAgent
from app.agents.pcb_expert import PCBExpertAgent
from app.agents.firmware_engineer import FirmwareEngineerAgent
from app.agents.documentation_writer import DocumentationWriterAgent
from app.agents.design_reviewer import DesignReviewerAgent


class AgentOrchestrator:
    def __init__(self, model: str = "gemini"):
        self.planner = ProjectPlannerAgent(model=model)
        self.circuit_designer = CircuitDesignerAgent(model=model)
        self.pcb_expert = PCBExpertAgent(model=model)
        self.firmware_engineer = FirmwareEngineerAgent(model=model)
        self.doc_writer = DocumentationWriterAgent(model=model)
        self.reviewer = DesignReviewerAgent(model=model)

    async def run_full_pipeline(self, prompt: str) -> dict:
        results = {}
        all_tokens = {}

        print("[1/5] Analyzing requirements...")
        planner_result = await self.planner.execute({"prompt": prompt})
        results["spec"] = planner_result["spec"]
        all_tokens["planner"] = planner_result["tokens"]

        print("[2/5] Selecting components and designing circuit...")
        circuit_result = await self.circuit_designer.execute({
            "spec": results["spec"],
            "components": results["spec"].get("selected_components", []),
        })
        results["circuit"] = circuit_result["circuit"]
        all_tokens["circuit_designer"] = circuit_result["tokens"]

        print("[3/5] Designing PCB layout...")
        pcb_result = await self.pcb_expert.execute({
            "spec": results["spec"],
            "components": results["spec"].get("selected_components", []),
            "connections": results["circuit"].get("connections", []),
        })
        results["pcb"] = pcb_result["pcb_design"]
        all_tokens["pcb_expert"] = pcb_result["tokens"]

        print("[4/5] Generating firmware...")
        firmware_result = await self.firmware_engineer.execute({
            "spec": results["spec"],
            "components": results["spec"].get("selected_components", []),
            "connections": results["circuit"].get("connections", []),
        })
        results["firmware"] = firmware_result["firmware"]
        all_tokens["firmware_engineer"] = firmware_result["tokens"]

        print("[5/5] Writing documentation...")
        doc_result = await self.doc_writer.execute({
            "spec": results["spec"],
            "components": results["spec"].get("selected_components", []),
            "connections": results["circuit"].get("connections", []),
            "bom": results["circuit"].get("bom", []),
        })
        results["documentation"] = doc_result["documentation"]
        all_tokens["doc_writer"] = doc_result["tokens"]

        results["tokens"] = all_tokens
        return results
