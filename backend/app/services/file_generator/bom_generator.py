import csv
import io
import json


class BOMGenerator:
    """Generates Bill of Materials in multiple formats."""

    def generate_csv(self, project) -> str:
        bom = project.bom or []
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow([
            "Reference",
            "Component",
            "Value",
            "Package/Footprint",
            "Quantity",
            "Manufacturer",
            "Part Number",
            "Unit Price (USD)",
            "Total Price (USD)",
            "Supplier",
            "Datasheet",
            "Alternatives",
        ])

        for item in bom:
            qty = item.get("quantity", 1)
            price = item.get("price", 0.0)
            writer.writerow([
                item.get("ref", ""),
                item.get("name", ""),
                item.get("value", ""),
                item.get("package", ""),
                qty,
                item.get("manufacturer", ""),
                item.get("part_number", ""),
                f"{price:.4f}",
                f"{price * qty:.4f}",
                item.get("supplier", ""),
                item.get("datasheet", ""),
                ", ".join(item.get("alternatives", [])),
            ])

        total_cost = sum(item.get("price", 0) * item.get("quantity", 1) for item in bom)
        total_qty = sum(item.get("quantity", 1) for item in bom)
        writer.writerow([])
        writer.writerow(["", "", "", "", total_qty, "", "", "", f"{total_cost:.2f}", "", "", ""])

        return output.getvalue()

    def generate_json(self, project) -> dict:
        bom = project.bom or []
        total_cost = sum(item.get("price", 0) * item.get("quantity", 1) for item in bom)
        total_qty = sum(item.get("quantity", 1) for item in bom)

        categories = {}
        for item in bom:
            cat = item.get("name", "Other")
            if cat not in categories:
                categories[cat] = {"items": [], "subtotal": 0}
            categories[cat]["items"].append(item)
            categories[cat]["subtotal"] += item.get("price", 0) * item.get("quantity", 1)

        return {
            "project_name": project.name,
            "total_components": len(bom),
            "total_quantity": total_qty,
            "total_cost_usd": round(total_cost, 2),
            "currency": "USD",
            "categories": categories,
            "items": bom,
            "cost_breakdown": {
                "mcu": sum(i.get("price", 0) * i.get("quantity", 1) for i in bom if "MCU" in i.get("name", "").upper()),
                "sensors": sum(i.get("price", 0) * i.get("quantity", 1) for i in bom if "SENSOR" in i.get("name", "").upper()),
                "passives": sum(i.get("price", 0) * i.get("quantity", 1) for i in bom if any(p in i.get("name", "").upper() for p in ["RESISTOR", "CAPACITOR", "INDUCTOR"])),
                "connectors": sum(i.get("price", 0) * i.get("quantity", 1) for i in bom if "CONNECTOR" in i.get("name", "").upper()),
                "other": sum(i.get("price", 0) * i.get("quantity", 1) for i in bom if not any(p in i.get("name", "").upper() for p in ["MCU", "SENSOR", "RESISTOR", "CAPACITOR", "INDUCTOR", "CONNECTOR"])),
            },
        }

    def generate_altium(self, project) -> str:
        bom = project.bom or []
        lines = [
            "Design Item ID\tDesignator\tQuantity\tManufacturer\tManufacturer Part Number\tDescription\tPrice\tSupplier",
        ]
        for item in bom:
            lines.append(
                f"{item.get('name', '')}\t{item.get('ref', '')}\t{item.get('quantity', 1)}\t"
                f"{item.get('manufacturer', '')}\t{item.get('part_number', '')}\t"
                f"{item.get('value', '')} {item.get('package', '')}\t"
                f"{item.get('price', 0):.4f}\t{item.get('supplier', '')}"
            )
        return '\n'.join(lines)
