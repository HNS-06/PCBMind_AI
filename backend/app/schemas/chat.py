from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str
    timestamp: datetime | None = None
    metadata: dict = {}


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    project_id: UUID | None = None
    conversation_id: UUID | None = None
    model: str = "groq"


class ChatResponse(BaseModel):
    conversation_id: UUID
    message: ChatMessage
    tokens_used: dict = {}


class ConversationResponse(BaseModel):
    id: UUID
    title: str
    messages: list[ChatMessage]
    model_used: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
