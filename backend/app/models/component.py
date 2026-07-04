import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Text, JSON, Float, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class Component(Base):
    __tablename__ = "components"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, index=True)
    manufacturer = Column(String(255), default="")
    manufacturer_part_number = Column(String(255), default="")
    description = Column(Text, default="")
    category = Column(String(100), index=True, nullable=False)
    subcategory = Column(String(100), default="")
    package = Column(String(100), default="")
    footprint = Column(String(100), default="")
    value = Column(String(100), default="")
    voltage_rating = Column(Float, nullable=True)
    current_rating = Column(Float, nullable=True)
    power_rating = Column(Float, nullable=True)
    tolerance = Column(String(50), default="")
    temperature_range = Column(String(100), default="")
    price = Column(Float, default=0.0)
    currency = Column(String(10), default="USD")
    datasheet_url = Column(String(500), default="")
    octopart_id = Column(String(100), default="")
    mouser_part_number = Column(String(100), default="")
    digikey_part_number = Column(String(100), default="")
    kicad_symbol = Column(String(255), default="")
    kicad_footprint = Column(String(255), default="")
    step_model = Column(String(255), default="")
    is_active = Column(Boolean, default=True)
    tags = Column(JSON, default=list)
    specs = Column(JSON, default=dict)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
