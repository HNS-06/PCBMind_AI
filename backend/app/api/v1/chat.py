import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.user import User
from app.models.project import Project
from app.models.conversation import AIConversation
from app.schemas.chat import ChatRequest, ChatResponse, ChatMessage
from app.api.deps import get_current_user
from datetime import datetime, timezone

router = APIRouter(prefix="/chat", tags=["AI Chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from app.services.ai.ai_service import AIService
    ai_service = AIService()

    conversation = None
    if payload.conversation_id:
        result = await db.execute(
            select(AIConversation).where(
                AIConversation.id == payload.conversation_id,
                AIConversation.user_id == user.id,
            )
        )
        conversation = result.scalar_one_or_none()

    if not conversation:
        conversation = AIConversation(
            user_id=user.id,
            project_id=payload.project_id,
            model_used=payload.model,
        )
        db.add(conversation)
        await db.flush()

    project_context = None
    if payload.project_id:
        result = await db.execute(
            select(Project).where(Project.id == payload.project_id)
        )
        project_context = result.scalar_one_or_none()

    response_text, tokens = await ai_service.chat(
        message=payload.message,
        project_context=project_context,
        conversation_history=conversation.messages or [],
        model=payload.model,
    )

    user_msg = ChatMessage(role="user", content=payload.message, timestamp=datetime.now(timezone.utc))
    assistant_msg = ChatMessage(role="assistant", content=response_text, timestamp=datetime.now(timezone.utc))

    messages = conversation.messages or []
    messages.append(user_msg.model_dump())
    messages.append(assistant_msg.model_dump())
    conversation.messages = messages

    total_tokens = conversation.tokens_used or {}
    for key, val in tokens.items():
        total_tokens[key] = total_tokens.get(key, 0) + val
    conversation.tokens_used = total_tokens

    await db.flush()

    return ChatResponse(
        conversation_id=conversation.id,
        message=assistant_msg,
        tokens_used=tokens,
    )
