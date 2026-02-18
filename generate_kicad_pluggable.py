"""
LightRail AI CPO Interconnect - 15-Layer KiCad Generator
Matches CPO Architecture: Central NCE Core + 8 Peripheral O-Tiles (TFLN)
High-Density Design for DeepPCB Auto-Router
"""

import json
import os
import uuid
import random

class LightRailCPOGenerator:
    def __init__(self, project_name="lightrail_cpo"):
        self.project_name = project_name
        self.pcb_content = []
        self.net_id = 0
        self.nets = {}
        
    def add(self, line):
        self.pcb_content.append(line)
        
    def add_net(self, name):
        if name in self.nets:
            return self.nets[name]
        self.net_id += 1
        self.nets[name] = self.net_id
        return self.net_id

    def generate_header(self):
        self.add('(kicad_pcb (version 20211014) (generator lightrail_cpo_gen)')
        self.add('  (general (thickness 1.6))')
        self.add('  (paper "A3")')
        self.add('  (title_block')
        self.add('    (title "LightRail AI Co-Packaged Optics (CPO) Interconnect")')
        self.add('    (company "LightRail Intelligence")')
        self.add('    (rev "3.0")')
        self.add('  )')
        self.add('  (layers')
        layers = [
            (0, "F.Cu", "signal"), (1, "In1.Cu", "power"), (2, "In2.Cu", "signal"),
            (3, "In3.Cu", "power"), (4, "In4.Cu", "signal"), (5, "In5.Cu", "power"),
            (6, "In6.Cu", "power"), (7, "In7.Cu", "signal"), (8, "In8.Cu", "power"),
            (9, "In9.Cu", "power"), (10, "In10.Cu", "signal"), (11, "In11.Cu", "power"),
            (12, "In12.Cu", "power"), (13, "In13.Cu", "power"), (31, "B.Cu", "signal")
        ]
        for idx, name, ltype in layers:
            self.add(f'    ({idx} "{name}" {ltype})')
        self.add('    (36 "B.SilkS" user) (37 "F.SilkS" user) (38 "B.Mask" user) (39 "F.Mask" user)')
        self.add('    (44 "Edge.Cuts" user)')
        self.add('  )')
        
        self.add('  (setup')
        self.add('    (stackup')
        for i, (idx, name, ltype) in enumerate(layers):
            mtype = "copper" if ltype in ["signal", "power"] else "technical"
            self.add(f'      (layer "{name}" (type "{mtype}") (thickness 0.035))')
            if i < len(layers) - 1:
                mat = "Rogers 4350B" if i < 2 else "FR4"
                er = 3.66 if i < 2 else 4.5
                self.add(f'      (layer "dielectric {i+1}" (type "core") (thickness 0.1) (material "{mat}") (epsilon_r {er}))')
        self.add('    )')
        self.add('    (last_trace_width 0.1) (trace_clearance 0.1) (min_trace_width 0.1)')
        self.add('    (via_size 0.2) (via_drill 0.1)')
        self.add('    (net_class "Default" (clearance 0.1) (trace_width 0.1) (via_dia 0.25) (via_drill 0.15))')
        rf_nets = [f'"O_TILE_{t}_RF_{ch}"' for t in range(8) for ch in range(4)]
        self.add(f'    (net_class "RF_50ohm" (clearance 0.1) (trace_width 0.15) (via_dia 0.4) (via_drill 0.2) (net {" ".join(rf_nets)}))')
        self.add('  )')

    def generate_nets(self):
        self.add('  (net 0 "")')
        for net in ["GND", "VCC_1V0", "VCC_1V8", "VCC_3V3", "VCC_12V", "GND_ANALOG", "V_BIAS"]:
            self.add(f'  (net {self.add_net(net)} "{net}")')
        # Bus nets for O-Tiles and SerDes
        for t in range(8):
            for ch in range(4):
                self.add(f'  (net {self.add_net(f"O_TILE_{t}_RF_{ch}")} "O_TILE_{t}_RF_{ch}")')
        for lane in range(64):
            self.add(f'  (net {self.add_net(f"NCE_PCIE_L{lane}")} "NCE_PCIE_L{lane}")')

    def add_pad(self, num, x, y, w, h, net, shape="rect", layer="F.Cu"):
        net_id = self.nets.get(net, 0)
        self.add(f'    (pad "{num}" smd {shape} (at {x:.3f} {y:.3f}) (size {w} {h}) (layers "{layer}" "F.Paste" "F.Mask") (net {net_id} "{net}"))')

    def add_nce_core(self, cx, cy):
        """Large Central LightRail AI Neural Compute Engine (NCE) BGA"""
        tstamp = str(uuid.uuid4())
        size = 36 # 36mm x 36mm
        self.add(f'  (footprint "LightRail:NCE_CORE_BGA" (layer "F.Cu") (tstamp {tstamp})')
        self.add(f'    (at {cx} {cy})')
        self.add(f'    (fp_text reference "LightRail AI" (at 0 0) (layer "F.SilkS") (effects (font (size 2.5 2.5) (thickness 0.4) bold)))')
        self.add(f'    (fp_text value "NCE-CPO-G3" (at 0 5) (layer "F.SilkS") (effects (font (size 1.2 1.2) (thickness 0.2))))')
        # Dense BGA Grid (18x18 = 324 pads)
        pitch = 1.8
        for r in range(18):
            for c in range(18):
                px, py = -15.3 + c*pitch, -15.3 + r*pitch
                idx = r * 18 + c
                if 7 < r < 10 and 7 < c < 10: net = "VCC_1V0" # Power center
                elif idx < 64: net = f"NCE_PCIE_L{idx}"
                elif idx < 128: net = f"O_TILE_{idx % 8}_RF_{idx % 4}"
                else: net = "GND"
                self.add_pad(f"{r}_{c}", px, py, 0.6, 0.6, net, "circle")
        self.add('  )')

    def add_o_tile(self, cx, cy, rot, tid):
        """Peripheral Optical Tile (O-Tile)"""
        tstamp = str(uuid.uuid4())
        self.add(f'  (footprint "LightRail:O_TILE_TFLN" (layer "F.Cu") (tstamp {tstamp})')
        self.add(f'    (at {cx} {cy} {rot})')
        self.add(f'    (fp_text reference "OT{tid}" (at 0 -6) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))')
        # Local Modulator Pads
        for i in range(4):
            self.add_pad(f"RF{i}", -3.75 + i*2.5, 4, 0.4, 1.2, f"O_TILE_{tid}_RF_{i}")
        # Thermal / GND Pad
        self.add_pad("TH", 0, 0, 10, 8, "GND", "rect")
        # Fiber Coupler Entry Silk
        self.add(f'    (fp_line (start -5 -5) (end 5 -5) (layer "F.SilkS") (width 0.1))')
        self.add('  )')

    def add_passive(self, ref, x, y, net1, net2, rot=0, ptype="C"):
        tstamp = str(uuid.uuid4())
        self.add(f'  (footprint "SMD:{ptype}_0402" (layer "F.Cu") (tstamp {tstamp})')
        self.add(f'    (at {x} {y} {rot})')
        self.add_pad("1", -0.5, 0, 0.5, 0.6, net1)
        self.add_pad("2", 0.5, 0, 0.5, 0.6, net2)
        self.add('  )')

    def add_edge_connector(self, cx, cy):
        tstamp = str(uuid.uuid4())
        self.add(f'  (footprint "TE:PCIe_Gen5_x16" (layer "F.Cu") (tstamp {tstamp})')
        self.add(f'    (at {cx} {cy})')
        for i in range(64):
            px = -31.5 + i*1.0
            self.add_pad(f"{i+1}", px, 0, 0.6, 4, f"NCE_PCIE_L{i}")
        self.add('  )')

    def generate_layout(self):
        # 240mm x 180mm High Precision PCB
        self.add_board_outline(240, 180)
        
        # Central CPO Module (Center of Board)
        bx, by = 120, 80
        self.add_nce_core(bx, by)
        
        # Surround with 8 Optical Tiles (2 North, 2 South, 2 East, 2 West)
        # matches the CPO "butterfly" or "surround" architecture
        positions = [
            (bx-25, by-35, 0), (bx+25, by-35, 0),    # North
            (bx-25, by+35, 180), (bx+25, by+35, 180),# South
            (bx-45, by-10, 90), (bx-45, by+10, 90),  # West
            (bx+45, by-10, 270), (bx+45, by+10, 270)  # East
        ]
        for i, (px, py, pr) in enumerate(positions):
            self.add_o_tile(px, py, pr, i)

        # Bottom Edge Connector
        self.add_edge_connector(120, 170)
        
        # Power Delivery (Distributed around CPO)
        for i in range(20):
            # Concentrated decoupling around NCE
            ang = i * (3.14159 * 2 / 20)
            rx, ry = bx + 40 * 1.1 * 1, by + 40 * 1.1 * 1
            # Actual placement ring
            rx = bx + (50 * (i % 2 + 1.2)) * (1 if i%2 else -1)
            ry = by + (i*5 - 50)
            self.add_passive(f"C_NCE_{i}", bx + 55 * 0.8 * (i-10)/5, by-60, "VCC_1V0", "GND")
            
        # Dense Fill Passives (Fill all quadrants)
        c_count = 0
        for row in range(30):
            for col in range(60):
                x = 10 + col * 3.8
                y = 10 + row * 3.0
                # Skip the CPO module area
                if 50 < x < 190 and 30 < y < 130: continue
                # Skip PCIe
                if 80 < x < 160 and 150 < y < 180: continue
                
                self.add_passive(f"CAP_{c_count}", x, y, random.choice(["VCC_1V8", "VCC_3V3", "VCC_12V"]), "GND", 90)
                c_count += 1

    def add_board_outline(self, w, h):
        self.add(f'  (gr_poly (pts (xy 0 0) (xy {w} 0) (xy {w} {h}) (xy 0 {h})) (layer "Edge.Cuts") (width 0.15) (tstamp {uuid.uuid4()}))')

    def write_files(self):
        self.add(')')
        pcb_file = f"{self.project_name}.kicad_pcb"
        with open(pcb_file, 'w') as f:
            f.write('\n'.join(self.pcb_content))
        pro_file = f"{self.project_name}.kicad_pro"
        pro_content = {
            "meta": {"version": 1},
            "project": {"name": "LightRail_CPO", "description": "15-Layer Co-Packaged Optics Board"},
            "pcbnew": {"design_settings": {"rules": {"min_copper_edge_clearance": 0.1}}}
        }
        with open(pro_file, 'w') as f:
            json.dump(pro_content, f, indent=2)
        print(f"Generated CPO Architecture: {pcb_file}")

if __name__ == "__main__":
    gen = LightRailCPOGenerator()
    gen.generate_header()
    gen.generate_nets()
    gen.generate_layout()
    gen.write_files()
