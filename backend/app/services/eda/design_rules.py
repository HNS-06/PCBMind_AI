class DesignRuleChecker:
    """Checks PCB design against manufacturing rules."""

    DEFAULT_RULES = {
        "min_trace_width_mm": 0.2,
        "min_clearance_mm": 0.2,
        "min_hole_diameter_mm": 0.3,
        "min_via_diameter_mm": 0.6,
        "min_via_drill_mm": 0.2,
        "min_silk_width_mm": 0.15,
        "min_silk_text_mm": 0.8,
        "board_edge_clearance_mm": 0.5,
        "min_annular_ring_mm": 0.15,
        "max_aspect_ratio": 10,
        "min_copper_to_edge_mm": 0.2,
    }

    def __init__(self, custom_rules: dict = None):
        self.rules = {**self.DEFAULT_RULES, **(custom_rules or {})}

    def check(self, pcb_data: dict) -> dict:
        issues = []
        warnings = []
        info = []

        board = pcb_data.get("board", {})
        components = pcb_data.get("components", [])
        tracks = pcb_data.get("tracks", [])
        vias = pcb_data.get("vias", [])

        board_width = board.get("width_mm", 80)
        board_height = board.get("height_mm", 60)

        for comp in components:
            x = comp.get("x", 0)
            y = comp.get("y", 0)
            if x < 0 or y < 0 or x > board_width or y > board_height:
                issues.append({
                    "severity": "error",
                    "type": "placement",
                    "message": f"Component {comp.get('id', '?')} placed outside board outline",
                    "location": f"({x}, {y})",
                })
            if x < self.rules["board_edge_clearance_mm"] or y < self.rules["board_edge_clearance_mm"]:
                warnings.append({
                    "severity": "warning",
                    "type": "clearance",
                    "message": f"Component {comp.get('id', '?')} too close to board edge",
                    "location": f"({x}, {y})",
                })

        for track in tracks:
            width = track.get("width_mm", 0.25)
            if width < self.rules["min_trace_width_mm"]:
                issues.append({
                    "severity": "error",
                    "type": "trace_width",
                    "message": f"Trace width {width}mm below minimum {self.rules['min_trace_width_mm']}mm",
                })

        for via in vias:
            diameter = via.get("diameter_mm", 0.6)
            drill = via.get("drill_mm", 0.3)
            if diameter < self.rules["min_via_diameter_mm"]:
                issues.append({
                    "severity": "error",
                    "type": "via_size",
                    "message": f"Via diameter {diameter}mm below minimum",
                })
            if drill < self.rules["min_via_drill_mm"]:
                issues.append({
                    "severity": "error",
                    "type": "via_drill",
                    "message": f"Via drill {drill}mm below minimum",
                })
            if diameter / drill > self.rules["max_aspect_ratio"]:
                warnings.append({
                    "severity": "warning",
                    "type": "aspect_ratio",
                    "message": f"Via aspect ratio {diameter/drill:.1f} exceeds {self.rules['max_aspect_ratio']}",
                })

        uncovered = [c for c in components if not c.get("has_copper_pour")]
        if uncovered and len(components) > 3:
            info.append({
                "severity": "info",
                "type": "ground",
                "message": f"Consider adding ground copper pour for {len(uncovered)} components without explicit ground connection",
            })

        return {
            "passed": len(issues) == 0,
            "errors": len(issues),
            "warnings": len(warnings),
            "info": len(info),
            "issues": issues,
            "warnings": warnings,
            "info_messages": info,
            "rules_applied": self.rules,
        }
