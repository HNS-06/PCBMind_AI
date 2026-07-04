from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class ComponentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    manufacturer: str = ""
    manufacturer_part_number: str = ""
    description: str = ""
    category: str = Field(..., min_length=1)
    subcategory: str = ""
    package: str = ""
    footprint: str = ""
    value: str = ""
    voltage_rating: float | None = None
    current_rating: float | None = None
    power_rating: float | None = None
    tolerance: str = ""
    temperature_range: str = ""
    price: float = 0.0
    currency: str = "USD"
    datasheet_url: str = ""
    octopart_id: str = ""
    mouser_part_number: str = ""
    digikey_part_number: str = ""
    kicad_symbol: str = ""
    kicad_footprint: str = ""
    step_model: str = ""
    tags: list[str] = []
    specs: dict = {}


class ComponentResponse(BaseModel):
    id: UUID
    name: str
    manufacturer: str
    manufacturer_part_number: str
    description: str
    category: str
    subcategory: str
    package: str
    footprint: str
    value: str
    voltage_rating: float | None
    current_rating: float | None
    power_rating: float | None
    tolerance: str
    temperature_range: str
    price: float
    currency: str
    datasheet_url: str
    kicad_symbol: str
    kicad_footprint: str
    tags: list[str]
    specs: dict
    created_at: datetime

    class Config:
        from_attributes = True


class ComponentSearchRequest(BaseModel):
    category: str | None = None
    search: str | None = None
    tags: list[str] = []
    min_price: float | None = None
    max_price: float | None = None
    limit: int = Field(default=50, le=200)
