import zipfile
import io
import json
from app.services.file_generator.kicad_generator import KiCadGenerator
from app.services.file_generator.gerber_generator import GerberGenerator
from app.services.file_generator.bom_generator import BOMGenerator
from app.services.file_generator.wiring_diagram import WiringDiagramGenerator


class ProjectArchiver:
    """Creates complete project archive with all generated files."""

    def __init__(self):
        self.kicad = KiCadGenerator()
        self.gerber = GerberGenerator()
        self.bom = BOMGenerator()
        self.wiring = WiringDiagramGenerator()

    def create_archive(self, project) -> io.BytesIO:
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(
                f"{project.name}/{project.name}.kicad_sch",
                self.kicad.generate_schematic(project),
            )
            zf.writestr(
                f"{project.name}/{project.name}.kicad_pcb",
                self.kicad.generate_pcb(project),
            )

            gerber_files = self.gerber.generate(project)
            for filename, content in gerber_files.items():
                zf.writestr(f"{project.name}/gerber/{filename}", content)

            zf.writestr(
                f"{project.name}/bom/{project.name}_bom.csv",
                self.bom.generate_csv(project),
            )
            zf.writestr(
                f"{project.name}/bom/{project.name}_bom.json",
                json.dumps(self.bom.generate_json(project), indent=2),
            )

            zf.writestr(
                f"{project.name}/docs/wiring_diagram.md",
                self.wiring.generate(project),
            )

            if project.firmware_code:
                zf.writestr(
                    f"{project.name}/firmware/main.py",
                    project.firmware_code,
                )

            if project.documentation:
                zf.writestr(
                    f"{project.name}/docs/README.md",
                    project.documentation,
                )

            zf.writestr(
                f"{project.name}/project.json",
                json.dumps({
                    "name": project.name,
                    "description": project.description,
                    "version": project.version,
                    "generated_by": "PCBMind AI",
                    "components_count": len(project.components or []),
                    "connections_count": len(project.connections or []),
                }, indent=2),
            )

        zip_buffer.seek(0)
        return zip_buffer
