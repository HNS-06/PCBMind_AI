import pytest
from app.agents.orchestrator import AgentOrchestrator
from app.agents.project_planner import ProjectPlannerAgent
from app.agents.circuit_designer import CircuitDesignerAgent
from app.agents.pcb_expert import PCBExpertAgent
from app.agents.firmware_engineer import FirmwareEngineerAgent
from app.agents.documentation_writer import DocumentationWriterAgent
from app.agents.design_reviewer import DesignReviewerAgent


def test_orchestrator_init():
    orch = AgentOrchestrator(model="gemini")
    assert orch.planner is not None
    assert orch.circuit_designer is not None
    assert orch.pcb_expert is not None
    assert orch.firmware_engineer is not None
    assert orch.doc_writer is not None
    assert orch.reviewer is not None


def test_agent_init():
    planner = ProjectPlannerAgent(model="openai")
    assert planner.model == "openai"
    assert planner.ai is not None

    designer = CircuitDesignerAgent(model="claude")
    assert designer.model == "claude"

    pcb = PCBExpertAgent()
    assert pcb.model == "gemini"


def test_all_agents_have_execute():
    agents = [
        ProjectPlannerAgent(),
        CircuitDesignerAgent(),
        PCBExpertAgent(),
        FirmwareEngineerAgent(),
        DocumentationWriterAgent(),
        DesignReviewerAgent(),
    ]
    for agent in agents:
        assert hasattr(agent, "execute")
        assert callable(agent.execute)
