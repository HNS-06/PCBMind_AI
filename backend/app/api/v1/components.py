from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db
from app.models.component import Component
from app.schemas.component import ComponentCreate, ComponentResponse, ComponentSearchRequest
from app.api.deps import get_current_user, get_admin_user
from app.models.user import User

router = APIRouter(prefix="/components", tags=["Components"])


@router.get("", response_model=list[ComponentResponse])
async def list_components(
    category: str | None = None,
    search: str | None = None,
    limit: int = Query(default=50, le=200),
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    query = select(Component).where(Component.is_active == True)
    if category:
        query = query.where(Component.category == category)
    if search:
        query = query.where(Component.name.ilike(f"%{search}%"))
    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    return [ComponentResponse.model_validate(c) for c in result.scalars().all()]


@router.get("/categories")
async def list_categories(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = await db.execute(
        select(Component.category, func.count(Component.id))
        .where(Component.is_active == True)
        .group_by(Component.category)
    )
    return [{"category": row[0], "count": row[1]} for row in result.all()]


@router.get("/{component_id}", response_model=ComponentResponse)
async def get_component(
    component_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    from uuid import UUID
    result = await db.execute(select(Component).where(Component.id == UUID(component_id)))
    component = result.scalar_one_or_none()
    if not component:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Component not found")
    return ComponentResponse.model_validate(component)


@router.post("", response_model=ComponentResponse, status_code=201)
async def create_component(
    payload: ComponentCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_admin_user),
):
    component = Component(**payload.model_dump())
    db.add(component)
    await db.flush()
    await db.refresh(component)
    return ComponentResponse.model_validate(component)
