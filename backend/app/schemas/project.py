from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Any


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str = ""
    prompt: str = Field(..., min_length=1)


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    prompt: str | None = None
    status: str | None = None
    components: list[dict] | None = None
    connections: list[dict] | None = None
    netlist: list[dict] | None = None
    bom: list[dict] | None = None
    pcb_data: dict | None = None
    schematic_data: dict | None = None
    firmware_code: str | None = None
    documentation: str | None = None


class ProjectResponse(BaseModel):
    id: UUID
    name: str
    description: str
    prompt: str
    status: str
    components: list[dict]
    connections: list[dict]
    netlist: list[dict]
    bom: list[dict]
    pcb_data: dict
    schematic_data: dict
    firmware_code: str
    documentation: str
    metadata: dict = Field(..., validation_alias="project_metadata")
    version: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    projects: list[ProjectResponse]
    total: int
    page: int
    per_page: int


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="Natural language project description")
    model: str = Field(default="groq", description="AI model to use")
    options: dict[str, Any] = Field(default_factory=dict)


class GenerateResponse(BaseModel):
    project_id: UUID
    status: str
    message: str
