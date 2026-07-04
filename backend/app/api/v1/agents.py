import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field
from app.core.database import get_db
from app.models.user import User
from app.models.project import Project
from app.api.deps import get_current_user
from app.agents.specialized_agents import ALL_AGENTS, AGENT_MAP, find_best_agent, find_relevant_agents

router = APIRouter(prefix="/agents", tags=["AI Agents"])


class AgentInfo(BaseModel):
    id: str
    name: str
    title: str
    domain: str
    avatar: str
    color: str
    description: str
    capabilities: list[dict]
    keywords: list[str]


class AnalyzeRequest(BaseModel):
    query: str


class AnalyzeResponse(BaseModel):
    primary_agent: str
    relevant_agents: list[str]
    query_type: str


class AgentChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    project_id: uuid.UUID | None = None
    agent_id: str | None = None
    model: str = "groq"
    multi_agent: bool = False


@router.get("", response_model=list[AgentInfo])
async def list_agents():
    return [
        AgentInfo(
            id=a.id,
            name=a.name,
            title=a.title,
            domain=a.domain.value,
            avatar=a.avatar,
            color=a.color,
            description=a.description,
            capabilities=[{"name": c.name, "description": c.description} for c in a.capabilities],
            keywords=a.keywords[:10],
        )
        for a in ALL_AGENTS
    ]


@router.get("/{agent_id}", response_model=AgentInfo)
async def get_agent(agent_id: str):
    agent = AGENT_MAP.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return AgentInfo(
        id=agent.id,
        name=agent.name,
        title=agent.title,
        domain=agent.domain.value,
        avatar=agent.avatar,
        color=agent.color,
        description=agent.description,
        capabilities=[{"name": c.name, "description": c.description} for c in agent.capabilities],
        keywords=agent.keywords[:10],
    )


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_query(payload: AnalyzeRequest):
    relevant = find_relevant_agents(payload.query, min_score=0.5)
    primary = find_best_agent(payload.query)

    from app.agents.smart_orchestrator import SmartOrchestrator
    orch = SmartOrchestrator()
    analysis = orch._classify_query(payload.query)

    return AnalyzeResponse(
        primary_agent=primary.id,
        relevant_agents=[a.id for a in relevant],
        query_type=analysis,
    )


@router.post("/chat")
async def agent_chat(
    payload: AgentChatRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    project_context = None
    if payload.project_id:
        result = await db.execute(
            select(Project).where(Project.id == payload.project_id)
        )
        project = result.scalar_one_or_none()
        if project:
            project_context = {
                "name": project.name,
                "description": project.description,
                "components": project.components or [],
                "connections": project.connections or [],
                "bom": project.bom or [],
            }

    from app.agents.smart_orchestrator import SmartOrchestrator
    orchestrator = SmartOrchestrator(model=payload.model)

    if payload.multi_agent:
        result = await orchestrator.multi_agent_design(
            query=payload.message,
            project_context=project_context,
        )
        return {
            "response": result["response"],
            "agents_used": result["agents_used"],
            "tokens": result["tokens"],
        }
    else:
        response, tokens = await orchestrator.route_to_agent(
            query=payload.message,
            agent_id=payload.agent_id,
            project_context=project_context,
        )
        return {
            "response": response,
            "agent": tokens.get("agent", "unknown"),
            "agent_name": tokens.get("agent_name", "Unknown"),
            "tokens": tokens,
        }


@router.post("/review/{project_id}")
async def design_review(
    project_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project_data = {
        "name": project.name,
        "description": project.description,
        "components": project.components or [],
        "connections": project.connections or [],
        "pcb_data": project.pcb_data or {},
        "bom": project.bom or [],
    }

    from app.agents.smart_orchestrator import SmartOrchestrator
    orchestrator = SmartOrchestrator()
    review = await orchestrator.design_review(project_data)

    return review
