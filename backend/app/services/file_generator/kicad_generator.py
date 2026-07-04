class KiCadGenerator:
    """Generates KiCad schematic and PCB files from project data."""

    def generate_schematic(self, project) -> str:
        components = project.components or []
        schematic_data = project.schematic_data or {}
        placed = schematic_data.get("components", [])

        lines = [
            '(kicad_sch (version 20230121) (generator "PCBMind AI")',
            f'  (uuid "pcbmind-{project.id}")',
            f'  (paper "A4")',
            '',
            '  (lib_symbols',
        ]

        for comp in components:
            sym_name = comp.get("type", "Device:R")
            lines.append(f'    (symbol "{sym_name}" (pin_names (offset 1.016))')
            lines.append(f'      (property "Reference" "R" (at 0 0 0))')
            lines.append(f'      (property "Value" "{comp.get("value", "")}" (at 0 -2.54 0))')
            lines.append(f'      (property "Footprint" "{comp.get("package", "")}" (at 0 0 0))')
            lines.append(f'    )')
        lines.append('  )')

        for comp in placed:
            ref = comp.get("id", "U?")
            comp_type = comp.get("type", "")
            x = comp.get("x", 0)
            y = comp.get("y", 0)
            lines.append(f'  (symbol (lib_id "{comp_type}") (at {x} {y} 0)')
            lines.append(f'    (property "Reference" "{ref}" (at 0 -3 0))')
            lines.append(f'    (property "Value" "{comp_type}" (at 0 3 0))')
            lines.append(f'    (pin "{ref}" (uuid "pin-{ref}"))')
            lines.append(f'  )')

        connections = project.connections or []
        for conn in connections:
            net_name = conn.get("net_name", "")
            pins = conn.get("pins", [])
            if len(pins) >= 2:
                p1 = pins[0]
                p2 = pins[1]
                lines.append(f'  (wire (pts (xy {p1.get("x", 0)} {p1.get("y", 0)}) (xy {p2.get("x", 0)} {p2.get("y", 0)})))')
                lines.append(f'  (net_label "{net_name}" (at {p1.get("x", 0)} {p1.get("y", 0)} 0))')

        lines.append(')')
        return '\n'.join(lines)

    def generate_pcb(self, project) -> str:
        components = project.components or []
        pcb_data = project.pcb_data or {}
        board = pcb_data.get("board", {})
        placed = pcb_data.get("components", [])

        lines = [
            '(kicad_pcb (version 20221018) (generator "PCBMind AI")',
            f'  (general (thickness 1.6))',
            f'  (paper "A4")',
            f'  (layers',
            f'    (0 "F.Cu" signal)',
            f'    (31 "B.Cu" signal)',
            f'    (32 "B.Adhes" user "B.Adhesive")',
            f'    (33 "F.Adhes" user "F.Adhesive")',
            f'    (34 "B.Paste" user)',
            f'    (35 "F.Paste" user)',
            f'    (36 "B.SilkS" user "B.Silkscreen")',
            f'    (37 "F.SilkS" user "F.Silkscreen")',
            f'    (38 "B.Mask" user "B.Mask")',
            f'    (39 "F.Mask" user "F.Mask")',
            f'    (44 "Edge.Cuts" user)',
            f'  )',
            f'  (setup (stackup',
            f'    (layer "F.SilkS" (type "Top Silk Screen"))',
            f'    (layer "F.Paste" (type "Top Solder Paste"))',
            f'    (layer "F.Mask" (type "Top Solder Mask") (thickness 0.01))',
            f'    (layer "F.Cu" (type "copper") (thickness 0.035))',
            f'    (layer "dielectric 1" (type "core") (thickness 1.556) (material "FR4") (epsilon_r 4.5))',
            f'    (layer "B.Cu" (type "copper") (thickness 0.035))',
            f'    (layer "B.Mask" (type "Bottom Solder Mask") (thickness 0.01))',
            f'    (layer "B.Paste" (type "Bottom Solder Paste"))',
            f'    (layer "B.SilkS" (type "Bottom Silk Screen"))',
            f'  ))',
            '',
        ]

        width = board.get("width_mm", 80)
        height = board.get("height_mm", 60)
        lines.append(f'  (gr_rect (start 0 0) (end {width} {height}) (layer "Edge.Cuts") (width 0.05) (fill none))')
        lines.append('')

        for comp in placed:
            ref = comp.get("id", "U?")
            x = comp.get("x", 10)
            y = comp.get("y", 10)
            layer = comp.get("layer", "F.Cu")
            footprint = comp.get("footprint", "SMD")
            lines.append(f'  (footprint "{footprint}" (layer "{layer}")')
            lines.append(f'    (at {x} {y})')
            lines.append(f'    (property "Reference" "{ref}" (at 0 -3 0) (layer "F.SilkS") (uuid "ref-{ref}"))')
            lines.append(f'  )')

        copper_pours = pcb_data.get("copper_pours", [])
        for pour in copper_pours:
            net = pour.get("net", "GND")
            layer = pour.get("layer", "B.Cu")
            clearance = pour.get("clearance_mm", 0.2)
            lines.append(f'  (zone (net 0) (net_name "{net}") (layer "{layer}")')
            lines.append(f'    (hatch edge 0.5)')
            lines.append(f'    (connect_pads (clearance {clearance}))')
            lines.append(f'  )')

        lines.append(')')
        return '\n'.join(lines)
