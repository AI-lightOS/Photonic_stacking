"""
EasyEDA JSON Format Generator
Creates EasyEDA-compatible JSON for PCB design import
"""

import json
import math

class EasyEDAGenerator:
    def __init__(self, project_name="tfln_modulator"):
        self.project_name = project_name
        self.shapes = []
        self.components = []
        self.nets = []
        self.tracks = []
        self.shape_id = 1000
        
    def get_id(self):
        self.shape_id += 1
        return f"gge{self.shape_id}"
    
    def add_board_outline(self, width=100, height=80):
        """Add board outline (in mils, EasyEDA uses mils)"""
        w_mil = width * 39.37  # mm to mils
        h_mil = height * 39.37
        self.shapes.append({
            "gId": self.get_id(),
            "layerid": "1",  # Board outline layer
            "pathStr": f"M 0 0 L {w_mil} 0 L {w_mil} {h_mil} L 0 {h_mil} Z",
            "strokeWidth": 10
        })
    
    def add_component(self, ref, x, y, package="SOIC-8", rotation=0):
        """Add a component"""
        x_mil = x * 39.37
        y_mil = y * 39.37
        self.components.append({
            "gId": self.get_id(),
            "head": {
                "x": x_mil,
                "y": y_mil,
                "rotation": rotation
            },
            "ref": ref,
            "package": package,
            "layer": "1"  # Top layer
        })
    
    def add_pad(self, x, y, width=1.5, height=2.5, net=""):
        """Add a SMD pad"""
        x_mil = x * 39.37
        y_mil = y * 39.37
        w_mil = width * 39.37
        h_mil = height * 39.37
        self.shapes.append({
            "gId": self.get_id(),
            "layerid": "1",
            "x": x_mil,
            "y": y_mil,
            "width": w_mil,
            "height": h_mil,
            "type": "PAD",
            "shape": "RECT",
            "net": net
        })
    
    def add_track(self, x1, y1, x2, y2, width=0.25, layer="1", net=""):
        """Add a copper track"""
        self.tracks.append({
            "gId": self.get_id(),
            "layerid": layer,
            "net": net,
            "pointArr": [
                {"x": x1 * 39.37, "y": y1 * 39.37},
                {"x": x2 * 39.37, "y": y2 * 39.37}
            ],
            "strokeWidth": width * 39.37
        })
    
    def add_via(self, x, y, diameter=0.6, drill=0.3, net=""):
        """Add a via"""
        self.shapes.append({
            "gId": self.get_id(),
            "type": "VIA",
            "x": x * 39.37,
            "y": y * 39.37,
            "diameter": diameter * 39.37,
            "drill": drill * 39.37,
            "net": net
        })
    
    def generate_design(self):
        """Generate complete TFLN design"""
        # Board outline
        self.add_board_outline(100, 80)
        
        # Add nets
        self.nets = ["GND", "+3V3", "+1V8", "+5V", "PCIE_TX", "PCIE_RX", "LASER_EN", "PD_OUT"]
        
        # Main processor U1 at center
        cx, cy = 50, 40
        self.add_component("U1", cx, cy, "BGA-256", 0)
        
        # Add BGA pads (16x16 grid)
        for row in range(16):
            for col in range(16):
                px = cx - 7.5 + col
                py = cy - 7.5 + row
                self.add_pad(px, py, 0.4, 0.4, "GND" if (row + col) % 4 == 0 else "")
        
        # Power management ICs
        self.add_component("U5", 15, 60, "SOIC-8", 0)
        self.add_component("U6", 25, 60, "SOIC-8", 0)
        self.add_component("U7", 35, 60, "SOIC-8", 0)
        
        # Optical components
        self.add_component("U2", 25, 30, "SOIC-8", 0)
        self.add_component("U3", 75, 30, "SOIC-8", 0)
        
        # RF Driver
        self.add_component("U4", 50, 20, "QFN-16", 0)
        
        # Add power routing
        # +3V3 rail across top
        self.add_track(10, 65, 90, 65, 1.0, "1", "+3V3")
        
        # GND plane connections (vias)
        for x in range(15, 90, 10):
            self.add_via(x, 70, 0.6, 0.3, "GND")
        
        # Power delivery to main chip
        self.add_track(15, 65, 15, 40, 0.5, "1", "+3V3")
        self.add_track(15, 40, 42, 40, 0.5, "1", "+3V3")
        
        # Signal routing from U2 (Laser) to U1
        self.add_track(29, 30, 42, 35, 0.25, "1", "LASER_EN")
        
        # Signal routing from U1 to U3 (Photodetector)
        self.add_track(58, 35, 71, 30, 0.25, "1", "PD_OUT")
        
        # PCIe differential pairs (simplified)
        for i in range(8):
            y_offset = i * 2
            self.add_track(50, 55 + y_offset, 50, 75, 0.15, "1", f"PCIE_TX{i}_P")
            self.add_track(51, 55 + y_offset, 51, 75, 0.15, "1", f"PCIE_TX{i}_N")
        
        # Decoupling capacitors
        cap_positions = [(45, 35), (55, 35), (45, 45), (55, 45)]
        for i, (x, y) in enumerate(cap_positions):
            self.add_component(f"C{i+1}", x, y, "0603", 0)
            # Connect to power and ground
            self.add_track(x, y, x, y + 2, 0.3, "1", "+3V3")
            self.add_via(x, y + 2, 0.4, 0.2, "GND")
    
    def export_json(self):
        """Export to EasyEDA JSON format"""
        design = {
            "head": {
                "docType": "5",  # PCB document
                "editorVersion": "6.5.0",
                "title": self.project_name,
                "description": "TFLN Photonic Modulator PCB"
            },
            "canvas": "CA~1000~1000~#000000~yes~#FFFFFF~10~1000~1000~line~0.5~pixel~5~0~0",
            "shape": self.shapes,
            "TRACK": self.tracks,
            "LIB": self.components,
            "netlist": self.nets
        }
        
        filename = f"{self.project_name}_easyeda.json"
        with open(filename, 'w') as f:
            json.dump(design, f, indent=2)
        print(f"Generated {filename}")
        return filename


if __name__ == "__main__":
    gen = EasyEDAGenerator()
    gen.generate_design()
    gen.export_json()
    print("✅ EasyEDA JSON ready for import!")
