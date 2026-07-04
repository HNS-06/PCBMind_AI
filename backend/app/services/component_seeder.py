import json
from app.core.database import async_session
from app.models.component import Component
from sqlalchemy import select


async def seed_components():
    """Seed component library from JSON file."""
    with open("component-library/components.json", "r") as f:
        data = json.load(f)

    async with async_session() as db:
        for category, components in data["categories"].items():
            for comp_data in components:
                result = await db.execute(
                    select(Component).where(
                        Component.manufacturer_part_number == comp_data.get("part_number", "")
                    )
                )
                existing = result.scalar_one_or_none()
                if existing:
                    continue

                component = Component(
                    name=comp_data["name"],
                    manufacturer=comp_data.get("manufacturer", ""),
                    manufacturer_part_number=comp_data.get("part_number", ""),
                    description=comp_data.get("description", ""),
                    category=comp_data.get("category", category),
                    subcategory=comp_data.get("subcategory", ""),
                    package=comp_data.get("package", ""),
                    footprint=comp_data.get("footprint", ""),
                    voltage_rating=comp_data.get("voltage_rating"),
                    current_rating=comp_data.get("current_rating"),
                    price=comp_data.get("price", 0.0),
                    datasheet_url=comp_data.get("datasheet", ""),
                    kicad_symbol=comp_data.get("kicad_symbol", ""),
                    kicad_footprint=comp_data.get("kicad_footprint", ""),
                    tags=comp_data.get("tags", [category.lower()]),
                    specs=comp_data.get("specs", {}),
                )
                db.add(component)

        await db.commit()
        print(f"Seeded components from {len(data['categories'])} categories")
