import uuid
import enum
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Enum as SAEnum, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class FileType(str, enum.Enum):
    KICAD_SCH = "kicad_sch"
    KICAD_PCB = "kicad_pcb"
    GERBER = "gerber"
    DRILL = "drill"
    BOM = "bom"
    FIRMWARE = "firmware"
    SCHEMATIC_PDF = "schematic_pdf"
    PCB_3D_STEP = "pcb_3d_step"
    PCB_3D_WRL = "pcb_3d_wrl"
    WIRING_DIAGRAM = "wiring_diagram"
    DOCUMENTATION = "documentation"
    PROJECT_ARCHIVE = "project_archive"


class GeneratedFile(Base):
    __tablename__ = "generated_files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    file_type = Column(SAEnum(FileType), nullable=False)
    filename = Column(String(500), nullable=False)
    filepath = Column(String(1000), nullable=False)
    file_size = Column(BigInteger, default=0)
    mime_type = Column(String(100), default="")
    version = Column(Integer, default=1)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    project = relationship("Project", back_populates="files")
