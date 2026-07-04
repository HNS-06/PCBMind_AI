import pytest
from app.services.file_generator.kicad_generator import KiCadGenerator
from app.services.file_generator.gerber_generator import GerberGenerator
from app.services.file_generator.bom_generator import BOMGenerator
from app.services.file_generator.wiring_diagram import WiringDiagramGenerator
from app.services.eda.design_rules import DesignRuleChecker


class MockProject:
    def __init__(self):
        self.id = "test-123"
        self.name = "TestProject"
        self.description = "A test project"
        self.version = 1
        self.components = [
            {"ref": "U1", "type": "MCU", "name": "ESP32", "value": "ESP32-WROOM-32E",
             "package": "Module", "x": 50, "y": 30, "layer": "F.Cu"},
            {"ref": "R1", "type": "Resistor", "name": "10K", "value": "10K",
             "package": "0402", "x": 20, "y": 20, "layer": "F.Cu"},
            {"ref": "C1", "type": "Capacitor", "name": "100nF", "value": "100nF",
             "package": "0402", "x": 30, "y": 25, "layer": "F.Cu"},
        ]
        self.connections = [
            {"net_name": "VCC", "description": "Power rail", "type": "power",
             "pins": [{"component": "U1", "pin": "3V3"}, {"component": "R1", "pin": "pin1"}]},
            {"net_name": "SDA", "description": "I2C Data", "type": "signal",
             "pins": [{"component": "U1", "pin": "GPIO21"}, {"component": "U2", "pin": "SDA"}]},
        ]
        self.netlist = []
        self.bom = [
            {"ref": "U1", "name": "ESP32", "value": "ESP32-WROOM-32E", "package": "Module",
             "quantity": 1, "manufacturer": "Espressif", "part_number": "ESP32-WROOM-32E-N4",
             "price": 2.50, "supplier": "DigiKey", "alternatives": []},
            {"ref": "R1", "name": "Resistor", "value": "10K", "package": "0402",
             "quantity": 1, "manufacturer": "Yageo", "part_number": "RC0402FR-0710KL",
             "price": 0.001, "supplier": "LCSC", "alternatives": []},
        ]
        self.pcb_data = {
            "board": {"width_mm": 80, "height_mm": 60, "layers": 2},
            "components": [
                {"id": "U1", "footprint": "Module", "x": 40, "y": 30, "rotation": 0, "layer": "F.Cu"},
                {"id": "R1", "footprint": "0402", "x": 20, "y": 20, "rotation": 0, "layer": "F.Cu"},
            ],
            "tracks": [],
            "vias": [],
            "copper_pours": [{"net": "GND", "layer": "B.Cu", "clearance_mm": 0.2}],
        }
        self.schematic_data = {
            "components": [
                {"id": "U1", "type": "MCU", "value": "ESP32", "x": 100, "y": 100},
            ],
            "connections": self.connections,
        }
        self.firmware_code = "#include <Arduino.h>\nvoid setup() {}\nvoid loop() {}"
        self.documentation = "# Test Project\nThis is a test."
        self.metadata = {}


def test_kicad_schematic():
    gen = KiCadGenerator()
    project = MockProject()
    sch = gen.generate_schematic(project)
    assert "kicad_sch" in sch
    assert project.name in sch
    assert "U1" in sch
    assert "R1" in sch


def test_kicad_pcb():
    gen = KiCadGenerator()
    project = MockProject()
    pcb = gen.generate_pcb(project)
    assert "kicad_pcb" in pcb
    assert "F.Cu" in pcb
    assert "B.Cu" in pcb
    assert "Edge.Cuts" in pcb


def test_gerber_generation():
    gen = GerberGenerator()
    project = MockProject()
    files = gen.generate(project)
    assert f"{project.name}.GTL" in files
    assert f"{project.name}.GBL" in files
    assert f"{project.name}.GTS" in files
    assert f"{project.name}.GBS" in files
    assert f"{project.name}.GTO" in files
    assert f"{project.name}.GBO" in files
    assert f"{project.name}.GKO" in files
    assert f"{project.name}.DRL" in files


def test_bom_csv():
    gen = BOMGenerator()
    project = MockProject()
    csv = gen.generate_csv(project)
    assert "ESP32" in csv
    assert "Resistor" in csv
    assert "2.50" in csv


def test_bom_json():
    gen = BOMGenerator()
    project = MockProject()
    data = gen.generate_json(project)
    assert data["project_name"] == "TestProject"
    assert data["total_components"] == 2
    assert data["total_cost_usd"] > 0


def test_wiring_diagram():
    gen = WiringDiagramGenerator()
    project = MockProject()
    diagram = gen.generate(project)
    assert "Wiring Diagram" in diagram
    assert "U1" in diagram
    assert "VCC" in diagram


def test_design_rules_pass():
    checker = DesignRuleChecker()
    pcb_data = {
        "board": {"width_mm": 80, "height_mm": 60},
        "components": [
            {"id": "U1", "x": 40, "y": 30},
            {"id": "R1", "x": 20, "y": 20},
        ],
        "tracks": [{"width_mm": 0.3, "net": "VCC"}],
        "vias": [{"diameter_mm": 0.6, "drill_mm": 0.3}],
    }
    result = checker.check(pcb_data)
    assert result["passed"] is True
    assert result["errors"] == 0


def test_design_rules_fail():
    checker = DesignRuleChecker()
    pcb_data = {
        "board": {"width_mm": 80, "height_mm": 60},
        "components": [
            {"id": "U1", "x": -5, "y": 30},
        ],
        "tracks": [{"width_mm": 0.1, "net": "VCC"}],
        "vias": [{"diameter_mm": 0.3, "drill_mm": 0.1}],
    }
    result = checker.check(pcb_data)
    assert result["passed"] is False
    assert result["errors"] > 0


def test_component_outside_board():
    checker = DesignRuleChecker()
    pcb_data = {
        "board": {"width_mm": 80, "height_mm": 60},
        "components": [
            {"id": "U1", "x": 90, "y": 30},
        ],
        "tracks": [],
        "vias": [],
    }
    result = checker.check(pcb_data)
    assert any("outside board" in i["message"] for i in result["issues"])
