import uuid
import zipfile
import io
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.user import User
from app.models.project import Project
from app.api.deps import get_current_user

router = APIRouter(prefix="/export", tags=["Export"])


@router.get("/{project_id}/kicad")
async def export_kicad(
    project_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == user.id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    from app.services.file_generator.kicad_generator import KiCadGenerator
    generator = KiCadGenerator()

    sch_content = generator.generate_schematic(project)
    pcb_content = generator.generate_pcb(project)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f"{project.name}.kicad_sch", sch_content)
        zf.writestr(f"{project.name}.kicad_pcb", pcb_content)
    zip_buffer.seek(0)

    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={project.name}.zip"},
    )


@router.get("/{project_id}/gerber")
async def export_gerber(
    project_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == user.id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    from app.services.file_generator.gerber_generator import GerberGenerator
    generator = GerberGenerator()

    gerber_files = generator.generate(project)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for filename, content in gerber_files.items():
            zf.writestr(filename, content)
    zip_buffer.seek(0)

    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={project.name}_gerber.zip"},
    )


@router.get("/{project_id}/bom")
async def export_bom(
    project_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == user.id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    import csv
    import io

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Component", "Value", "Package", "Quantity", "Manufacturer", "Part Number", "Price", "Supplier"])

    for item in (project.bom or []):
        writer.writerow([
            item.get("name", ""),
            item.get("value", ""),
            item.get("package", ""),
            item.get("quantity", 1),
            item.get("manufacturer", ""),
            item.get("part_number", ""),
            item.get("price", 0),
            item.get("supplier", ""),
        ])

    csv_content = output.getvalue()
    return StreamingResponse(
        io.BytesIO(csv_content.encode()),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={project.name}_bom.csv"},
    )


@router.get("/{project_id}/firmware")
async def export_firmware(
    project_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == user.id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return StreamingResponse(
        io.BytesIO((project.firmware_code or "").encode()),
        media_type="text/x-python",
        headers={"Content-Disposition": f"attachment; filename={project.name}_firmware.py"},
    )
