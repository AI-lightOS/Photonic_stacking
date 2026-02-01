"""
Enhanced KiCad PCB Generator
Creates a complete KiCad project with all BOM components for DeepPCB routing
"""

import os
import json

class EnhancedKiCadGenerator:
    def __init__(self, project_name="tfln_modulator"):
        self.project_name = project_name
        self.pcb_content = []
        self.net_id = 0
        self.nets = {}
        
    def add(self, line):
        self.pcb_content.append(line)
        
    def add_net(self, name):
        self.net_id += 1
        self.nets[name] = self.net_id
        return self.net_id

    def generate_header(self):
        self.add('(kicad_pcb (version 20211014) (generator enhanced_generator)')
        self.add('  (general')
        self.add('    (thickness 1.6)')
        self.add('  )')
        self.add('  (paper "A3")')
        
        # 12-layer stackup
        self.add('  (layers')
        self.add('    (0 "F.Cu" signal)')
        self.add('    (1 "In1.Cu" power)')
        self.add('    (2 "In2.Cu" signal)')
        self.add('    (3 "In3.Cu" power)')
        self.add('    (4 "In4.Cu" signal)')
        self.add('    (5 "In5.Cu" signal)')
        self.add('    (6 "In6.Cu" power)')
        self.add('    (7 "In7.Cu" signal)')
        self.add('    (8 "In8.Cu" power)')
        self.add('    (9 "In9.Cu" signal)')
        self.add('    (10 "In10.Cu" signal)')
        self.add('    (31 "B.Cu" signal)')
        self.add('    (32 "B.Adhes" user)')
        self.add('    (33 "F.Adhes" user)')
        self.add('    (34 "B.Paste" user)')
        self.add('    (35 "F.Paste" user)')
        self.add('    (36 "B.SilkS" user)')
        self.add('    (37 "F.SilkS" user)')
        self.add('    (38 "B.Mask" user)')
        self.add('    (39 "F.Mask" user)')
        self.add('    (40 "Dwgs.User" user)')
        self.add('    (44 "Edge.Cuts" user)')
        self.add('  )')

    def generate_setup(self):
        self.add('  (setup')
        self.add('    (pad_to_mask_clearance 0.05)')
        self.add('    (grid_origin 0 0)')
        self.add('  )')

    def generate_nets(self):
        # Define all nets
        self.add('  (net 0 "")')
        
        # Power nets
        for net_name in ["GND", "+3V3", "+1V8", "+5V", "VCC_IO"]:
            nid = self.add_net(net_name)
            self.add(f'  (net {nid} "{net_name}")')
        
        # Signal nets - PCIe
        for i in range(16):
            for suffix in ["_TX_P", "_TX_N", "_RX_P", "_RX_N"]:
                net_name = f"PCIE{i}{suffix}"
                nid = self.add_net(net_name)
                self.add(f'  (net {nid} "{net_name}")')
        
        # Optical control signals
        for sig in ["LASER_EN", "LASER_MOD", "PD_OUT", "TEC_CTRL", "MZM_BIAS"]:
            nid = self.add_net(sig)
            self.add(f'  (net {nid} "{sig}")')

    def add_footprint(self, ref, value, x, y, w, h, pads=2, net_assignments=None):
        """Add a generic SMD footprint"""
        self.add(f'  (footprint "Package_SO:SOIC-{pads}" (layer "F.Cu")')
        self.add(f'    (at {x} {y})')
        self.add(f'    (descr "{value}")')
        self.add(f'    (attr smd)')
        self.add(f'    (fp_text reference "{ref}" (at 0 {-h/2 - 1}) (layer "F.SilkS")')
        self.add(f'      (effects (font (size 1 1) (thickness 0.15)))')
        self.add('    )')
        self.add(f'    (fp_text value "{value}" (at 0 {h/2 + 1}) (layer "F.Fab")')
        self.add(f'      (effects (font (size 1 1) (thickness 0.15)))')
        self.add('    )')
        
        # Add pads
        pad_pitch = w / (pads/2 + 1)
        for i in range(pads):
            px = -w/2 + pad_pitch * ((i % (pads//2)) + 1)
            py = -h/2 if i < pads//2 else h/2
            net_id = 0
            if net_assignments and i < len(net_assignments):
                net_name = net_assignments[i]
                net_id = self.nets.get(net_name, 0)
            self.add(f'    (pad "{i+1}" smd rect (at {px:.2f} {py:.2f}) (size 0.6 1.2) (layers "F.Cu" "F.Paste" "F.Mask") (net {net_id} ""))')
        
        self.add('  )')

    def add_bga_footprint(self, ref, value, x, y, size, pins):
        """Add a BGA-style footprint for the main processor"""
        self.add(f'  (footprint "Package_BGA:BGA-{pins}" (layer "F.Cu")')
        self.add(f'    (at {x} {y})')
        self.add(f'    (descr "{value}")')
        self.add(f'    (attr smd)')
        self.add(f'    (fp_text reference "{ref}" (at 0 {-size/2 - 2}) (layer "F.SilkS")')
        self.add(f'      (effects (font (size 1.5 1.5) (thickness 0.2)))')
        self.add('    )')
        
        # Add BGA pads in a grid
        grid_size = int(pins ** 0.5)
        pitch = size / (grid_size + 1)
        pad_num = 1
        for row in range(grid_size):
            for col in range(grid_size):
                px = -size/2 + pitch * (col + 1)
                py = -size/2 + pitch * (row + 1)
                self.add(f'    (pad "{pad_num}" smd circle (at {px:.2f} {py:.2f}) (size 0.4 0.4) (layers "F.Cu" "F.Paste" "F.Mask") (net 0 ""))')
                pad_num += 1
        
        self.add('  )')

    def add_board_outline(self, width=100, height=80):
        """Add board edge cuts"""
        self.add(f'  (gr_rect (start 0 0) (end {width} {height}) (layer "Edge.Cuts") (width 0.15))')

    def generate_components(self):
        # Board outline (100mm x 80mm)
        self.add_board_outline(100, 80)
        
        # U1: TFLN Mach-Zehnder Modulator (main chip, center)
        self.add_bga_footprint("U1", "TFLN-MZM-400G", 50, 40, 20, 256)
        
        # U2: DFB Laser Diode
        self.add_footprint("U2", "TLN-1550-100", 25, 30, 8, 6, 8, ["GND", "+3V3", "LASER_EN", "LASER_MOD"])
        
        # U3: Photodetector
        self.add_footprint("U3", "XPDV4120R", 75, 30, 6, 4, 6, ["GND", "PD_OUT", "+3V3"])
        
        # U4: RF Driver
        self.add_footprint("U4", "HMC8410", 50, 20, 10, 8, 16)
        
        # U5-U7: Power Management ICs
        self.add_footprint("U5", "MAX3669", 15, 60, 6, 4, 8, ["GND", "+5V", "+3V3"])
        self.add_footprint("U6", "TPS7A4700", 25, 60, 4, 3, 6, ["GND", "+3V3", "+1V8"])
        self.add_footprint("U7", "LT8614", 35, 60, 5, 4, 8, ["+5V", "GND", "+3V3"])
        
        # U8: TEC Controller
        self.add_footprint("U8", "MPT5000", 85, 60, 8, 6, 16, ["GND", "+5V", "TEC_CTRL"])
        
        # U9: SerDes
        self.add_footprint("U9", "BCM84881", 50, 60, 12, 10, 64)
        
        # U10: Clock Generator
        self.add_footprint("U10", "Si5395A", 70, 60, 6, 5, 24)
        
        # Decoupling capacitors around the main chip
        cap_positions = [
            (40, 30), (60, 30), (40, 50), (60, 50),
            (35, 35), (65, 35), (35, 45), (65, 45),
            (45, 25), (55, 25), (45, 55), (55, 55)
        ]
        for i, (x, y) in enumerate(cap_positions):
            self.add_footprint(f"C{i+1}", "10uF", x, y, 2, 1.2, 2, ["GND", "+3V3"])
        
        # PCIe edge connector (bottom)
        self.add(f'  (footprint "Connector_PCIe:PCIe_x16" (layer "F.Cu")')
        self.add(f'    (at 50 75)')
        self.add(f'    (descr "PCIe x16 Edge Connector")')
        self.add(f'    (fp_text reference "J1" (at 0 -5) (layer "F.SilkS")')
        self.add(f'      (effects (font (size 1 1) (thickness 0.15)))')
        self.add('    )')
        # Add edge connector pads
        for i in range(98):  # PCIe x16 has ~98 pins
            px = -48 + i
            self.add(f'    (pad "{i+1}" smd rect (at {px} 0) (size 0.6 3) (layers "F.Cu" "F.Paste" "F.Mask") (net 0 ""))')
        self.add('  )')
        
        # Add routing traces
        self.generate_routing()

    def add_segment(self, x1, y1, x2, y2, width=0.25, layer="F.Cu", net_id=0):
        """Add a copper trace segment"""
        self.add(f'  (segment (start {x1} {y1}) (end {x2} {y2}) (width {width}) (layer "{layer}") (net {net_id}))')
    
    def add_via(self, x, y, size=0.6, drill=0.3, net_id=0):
        """Add a via"""
        self.add(f'  (via (at {x} {y}) (size {size}) (drill {drill}) (layers "F.Cu" "B.Cu") (net {net_id}))')

    def generate_routing(self):
        """Generate pre-routed traces for power and signals"""
        gnd_net = self.nets.get("GND", 1)
        v33_net = self.nets.get("+3V3", 2)
        v18_net = self.nets.get("+1V8", 3)
        
        # Power rail +3V3 across top of board
        self.add_segment(10, 65, 90, 65, 1.0, "F.Cu", v33_net)
        
        # Power connections to main chip area
        self.add_segment(25, 65, 25, 50, 0.5, "F.Cu", v33_net)
        self.add_segment(75, 65, 75, 50, 0.5, "F.Cu", v33_net)
        
        # Ground vias along power rail
        for x in range(15, 90, 10):
            self.add_via(x, 68, 0.6, 0.3, gnd_net)
        
        # Signal routing from U2 (Laser) to U1 (Main Chip)
        laser_en = self.nets.get("LASER_EN", 0)
        self.add_segment(29, 30, 35, 35, 0.2, "F.Cu", laser_en)
        self.add_segment(35, 35, 42, 35, 0.2, "F.Cu", laser_en)
        
        # Signal routing from U1 to U3 (Photodetector)
        pd_out = self.nets.get("PD_OUT", 0)
        self.add_segment(58, 35, 65, 35, 0.2, "F.Cu", pd_out)
        self.add_segment(65, 35, 71, 30, 0.2, "F.Cu", pd_out)
        
        # PCIe differential pairs from J1 to U9
        for i in range(8):
            pcie_tx_p = self.nets.get(f"PCIE{i}_TX_P", 0)
            pcie_tx_n = self.nets.get(f"PCIE{i}_TX_N", 0)
            x_base = 30 + i * 2.5
            # Differential pair routing
            self.add_segment(x_base, 75, x_base, 65, 0.15, "F.Cu", pcie_tx_p)
            self.add_segment(x_base + 0.3, 75, x_base + 0.3, 65, 0.15, "F.Cu", pcie_tx_n)
        
        # Decoupling cap connections to GND plane (vias)
        cap_positions = [
            (40, 30), (60, 30), (40, 50), (60, 50),
            (35, 35), (65, 35), (35, 45), (65, 45)
        ]
        for x, y in cap_positions:
            self.add_via(x, y + 1, 0.4, 0.2, gnd_net)

    def write_files(self):
        # Close the PCB file
        self.add(')')
        
        # Write PCB file
        pcb_file = f"{self.project_name}.kicad_pcb"
        with open(pcb_file, 'w') as f:
            f.write('\n'.join(self.pcb_content))
        print(f"Generated {pcb_file}")
        
        # Update project file
        project_data = {
            "board": {
                "design_settings": {
                    "defaults": {
                        "board_outline_line_width": 0.1,
                        "copper_line_width": 0.2
                    },
                    "rules": {
                        "min_copper_edge_clearance": 0.5,
                        "min_track_width": 0.2
                    },
                    "track_widths": [0.2, 0.3, 0.5, 1.0],
                    "via_dimensions": [{"diameter": 0.6, "drill": 0.3}]
                }
            },
            "meta": {
                "filename": f"{self.project_name}.kicad_pro",
                "version": 1
            },
            "net_settings": {
                "classes": [{
                    "name": "Default",
                    "clearance": 0.2,
                    "track_width": 0.2,
                    "via_diameter": 0.6,
                    "via_drill": 0.3
                }]
            },
            "pcbnew": {},
            "schematic": {},
            "sheets": [],
            "text_variables": {}
        }
        
        pro_file = f"{self.project_name}.kicad_pro"
        with open(pro_file, 'w') as f:
            json.dump(project_data, f, indent=2)
        print(f"Updated {pro_file}")


if __name__ == "__main__":
    gen = EnhancedKiCadGenerator()
    gen.generate_header()
    gen.generate_setup()
    gen.generate_nets()
    gen.generate_components()
    gen.write_files()
    print("\\n✅ KiCad project ready for DeepPCB!")
