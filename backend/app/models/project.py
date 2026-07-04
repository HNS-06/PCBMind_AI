import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, JSON, Integer, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class ProjectStatus(str, enum.Enum):
    DRAFT = "draft"
    GENERATING = "generating"
    COMPLETED = "completed"
    ERROR = "error"
    ARCHIVED = "archived"


class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, default="")
    prompt = Column(Text, nullable=False)
    status = Column(SAEnum(ProjectStatus), default=ProjectStatus.DRAFT)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    components = Column(JSON, default=list)
    connections = Column(JSON, default=list)
    netlist = Column(JSON, default=list)
    bom = Column(JSON, default=list)
    pcb_data = Column(JSON, default=dict)
    schematic_data = Column(JSON, default=dict)
    firmware_code = Column(Text, default="")
    documentation = Column(Text, default="")
    metadata = Column(JSON, default=dict)
    version = Column(Integer, default=1)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    owner = relationship("User", back_populates="projects")
    files = relationship("GeneratedFile", back_populates="project", cascade="all, delete-orphan")
    conversations = relationship("AIConversation", back_populates="project", cascade="all, delete-orphan")
