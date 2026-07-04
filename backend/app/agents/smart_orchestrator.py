"""
Smart Agent Orchestrator - Routes queries to specialized agents and combines their expertise.
"""
import json
import asyncio
from app.agents.specialized_agents import (
    ALL_AGENTS, AGENT_MAP, find_best_agent, find_relevant_agents,
    SpecializedAgent, AgentDomain,
)
from app.services.ai.ai_service import AIService


class SmartOrchestrator:
    def __init__(self, model: str = "groq"):
        self.ai = AIService()
        self.model = model

    async def analyze_query(self, query: str) -> dict:
        """Analyze a query and determine which agents should handle it."""
        relevant = find_relevant_agents(query, min_score=0.5)
        primary = find_best_agent(query)

        return {
            "primary_agent": primary.id,
            "relevant_agents": [a.id for a in relevant],
            "query_type": self._classify_query(query),
        }

    def _classify_query(self, query: str) -> str:
        q = query.lower()
        if any(w in q for w in ["design", "build", "create", "make", "schematic"]):
            return "design_request"
        elif any(w in q for w in ["why", "explain", "how", "what"]):
            return "question"
        elif any(w in q for w in ["change", "modify", "replace", "swap", "update"]):
            return "modification"
        elif any(w in q for w in ["check", "review", "verify", "validate"]):
            return "review"
        elif any(w in q for w in ["optimize", "reduce", "cheaper", "improve"]):
            return "optimization"
        return "general"

    async def route_to_agent(
        self,
        query: str,
        agent_id: str | None = None,
        project_context: dict | None = None,
    ) -> tuple[str, dict]:
        """Route a query to a specific or auto-selected agent."""
        if agent_id and agent_id in AGENT_MAP:
            agent = AGENT_MAP[agent_id]
        else:
            agent = find_best_agent(query)

        system_prompt = agent.system_prompt
        if project_context:
            system_prompt += f"\n\nCURRENT PROJECT CONTEXT:\n{json.dumps(project_context, indent=2)}"

        response, tokens = await self.ai.generate(
            prompt=query,
            system_prompt=system_prompt,
            model=self.model,
            temperature=agent.temperature,
            max_tokens=agent.max_tokens,
        )
        return response, {
            "agent": agent.id,
            "agent_name": agent.name,
            **tokens,
        }

    async def multi_agent_design(
        self,
        query: str,
        project_context: dict | None = None,
    ) -> dict:
        """
        Run multiple agents on the same query and combine their outputs.
        Used for comprehensive design tasks.
        """
        relevant = find_relevant_agents(query, min_score=1.0)
        if not relevant:
            relevant = [find_best_agent(query)]

        tasks = []
        for agent in relevant[:4]:
            ctx = project_context or {}
            system_prompt = agent.system_prompt
            system_prompt += f"\n\nPROJECT CONTEXT:\n{json.dumps(ctx, indent=2)}"

            tasks.append(self.ai.generate(
                prompt=query,
                system_prompt=system_prompt,
                model=self.model,
                temperature=agent.temperature,
                max_tokens=agent.max_tokens,
            ))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        combined_responses = []
        all_tokens = {}
        for i, result in enumerate(results):
            agent = relevant[i]
            if isinstance(result, Exception):
                combined_responses.append(f"[{agent.name}] Error: {str(result)}")
            else:
                response, tokens = result
                combined_responses.append(f"## {agent.avatar} {agent.name}\n\n{response}")
                all_tokens[agent.id] = tokens

        combined_output = "\n\n---\n\n".join(combined_responses)

        return {
            "response": combined_output,
            "agents_used": [a.id for a in relevant[:4]],
            "tokens": all_tokens,
        }

    async def design_review(
        self,
        project_data: dict,
        focus_areas: list[str] | None = None,
    ) -> dict:
        """
        Run a comprehensive design review using multiple specialized agents.
        """
        review_agents = [
            AGENT_MAP.get("power_systems"),
            AGENT_MAP.get("signal_integrity"),
            AGENT_MAP.get("thermal_management"),
            AGENT_MAP.get("safety_protection"),
            AGENT_MAP.get("design_for_manufacturing"),
            AGENT_MAP.get("cost_optimization"),
        ]
        review_agents = [a for a in review_agents if a is not None]

        if focus_areas:
            review_agents = [
                a for a in review_agents
                if any(f in a.keywords for f in focus_areas)
            ] or review_agents[:3]

        tasks = []
        for agent in review_agents:
            system_prompt = agent.system_prompt
            system_prompt += "\n\nReview the following project and identify issues, improvements, and risks."
            system_prompt += f"\n\nPROJECT DATA:\n{json.dumps(project_data, indent=2)}"

            tasks.append(self.ai.generate(
                prompt="Perform a thorough design review of this project. Identify issues, risks, and improvements.",
                system_prompt=system_prompt,
                model=self.model,
                temperature=agent.temperature,
                max_tokens=agent.max_tokens,
            ))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        reviews = []
        for i, result in enumerate(results):
            agent = review_agents[i]
            if isinstance(result, Exception):
                reviews.append({
                    "agent": agent.id,
                    "agent_name": agent.name,
                    "status": "error",
                    "error": str(result),
                })
            else:
                response, tokens = result
                reviews.append({
                    "agent": agent.id,
                    "agent_name": agent.name,
                    "avatar": agent.avatar,
                    "review": response,
                    "tokens": tokens,
                })

        return {
            "reviews": reviews,
            "total_agents": len(reviews),
        }
