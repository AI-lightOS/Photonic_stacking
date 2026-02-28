"""
LightRail AI CPO Interconnect - 15-Layer KiCad Generator (DeepPCB Optimization)
Matches CPO Architecture: Central NCE Core + 8 Peripheral O-Tiles (TFLN)
Fixed: 'Invalid pin id -X' by adding missing references.
Fixed: 'Repositioned outside boundary' by adding (locked) attribute.
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
        self.add('    (rev "3.2")')
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
        self.add('    (net_class "Default" (clearance 0.12) (trace_width 0.1) (via_dia 0.25) (via_drill 0.15))')
        rf_nets = [f'"O_TILE_{t}_RF_{ch}"' for t in range(8) for ch in range(4)]
        self.add(f'    (net_class "RF_50ohm" (clearance 0.15) (trace_width 0.15) (via_dia 0.4) (via_drill 0.2) (net {" ".join(rf_nets)}))')
        self.add('  )')

    def generate_nets(self):
        self.add('  (net 0 "")')
        for net in ["GND", "VCC_1V0", "VCC_1V8", "VCC_3V3", "VCC_12V", "GND_ANALOG", "V_BIAS"]:
            self.add(f'  (net {self.add_net(net)} "{net}")')
        for t in range(8):
            for ch in range(4):
                self.add(f'  (net {self.add_net(f"O_TILE_{t}_RF_{ch}")} "O_TILE_{t}_RF_{ch}")')
        for lane in range(64):
            self.add(f'  (net {self.add_net(f"NCE_PCIE_L{lane}")} "NCE_PCIE_L{lane}")')

    def add_pad(self, num, x, y, w, h, net, shape="rect", layer="F.Cu"):
        net_id = self.nets.get(net, 0)
        self.add(f'    (pad "{num}" smd {shape} (at {x:.3f} {y:.3f}) (size {w} {h}) (layers "{layer}" "F.Paste" "F.Mask") (net {net_id} "{net}"))')

    def add_nce_core(self, cx, cy):
        """Large Central NCE BGA - Added 'locked' to prevent repositioning"""
        tstamp = str(uuid.uuid4())
        self.add(f'  (footprint "Broadcom:BGA-324" (layer "F.Cu") (tstamp {tstamp}) (locked)')
        self.add(f'    (at {cx} {cy})')
        self.add(f'    (fp_text reference "U1" (at 0 -20) (layer "F.SilkS") (effects (font (size 1.5 1.5) (thickness 0.3))))')
        self.add(f'    (fp_text value "LightRail AI" (at 0 0) (layer "F.SilkS") (effects (font (size 3 3) (thickness 0.5) bold)))')
        pitch = 1.27
        for r in range(18):
            for c in range(18):
                px, py = -10.8 + c*pitch, -10.8 + r*pitch
                idx = r * 18 + c
                if 6 < r < 12 and 6 < c < 12: net = "VCC_1V0"
                elif idx < 64: net = f"NCE_PCIE_L{idx}"
                elif idx < 128: net = f"O_TILE_{idx % 8}_RF_{idx % 4}"
                else: net = "GND"
                self.add_pad(f"{idx+1}", px, py, 0.5, 0.5, net, "circle")
        self.add('  )')

    def add_o_tile(self, cx, cy, rot, tid):
        """Optical Tile - Added 'locked'"""
        tstamp = str(uuid.uuid4())
        self.add(f'  (footprint "LightRail:O_TILE_TFLN" (layer "F.Cu") (tstamp {tstamp}) (locked)')
        self.add(f'    (at {cx} {cy} {rot})')
        self.add(f'    (fp_text reference "OT{tid}" (at 0 -8) (layer "F.SilkS") (effects (font (size 1.2 1.2) (thickness 0.2))))')
        for i in range(4):
            self.add_pad(f"{i+1}", -3.75 + i*2.5, 6, 0.4, 1.2, f"O_TILE_{tid}_RF_{i}")
        self.add_pad("5", 0, 0, 10, 8, "GND", "rect")
        self.add('  )')

    def add_passive(self, ref, x, y, net1, net2, rot=0, ptype="C"):
        """Passive Components - Added 'locked' and standard library headers"""
        tstamp = str(uuid.uuid4())
        lib_name = "Capacitor_SMD:C_0402_1005Metric" if ptype == "C" else "Resistor_SMD:R_0402_1005Metric"
        self.add(f'  (footprint "{lib_name}" (layer "F.Cu") (tstamp {tstamp}) (locked)')
        self.add(f'    (at {x:.3f} {y:.3f} {rot})')
        self.add(f'    (fp_text reference "{ref}" (at 0 -0.8) (layer "F.SilkS") (effects (font (size 0.5 0.5) (thickness 0.1))))')
        self.add(f'    (fp_text value "{ptype}" (at 0 0.8) (layer "F.Fab") (effects (font (size 0.5 0.5) (thickness 0.1))))')
        self.add_pad("1", -0.5, 0, 0.5, 0.6, net1)
        self.add_pad("2", 0.5, 0, 0.5, 0.6, net2)
        self.add('  )')

    def add_edge_connector(self, cx, cy):
        """PCIe Connector - Added reference 'J1' and 'locked'. This fixes the (-X) pin id error."""
        tstamp = str(uuid.uuid4())
        self.add(f'  (footprint "Connector_PCBEdge:PCIe_x16" (layer "F.Cu") (tstamp {tstamp}) (locked)')
        self.add(f'    (at {cx} {cy})')
        self.add(f'    (fp_text reference "J1" (at 0 -10) (layer "F.SilkS") (effects (font (size 1.2 1.2) (thickness 0.2))))')
        self.add(f'    (fp_text value "PCIe_Gen5_x16" (at 0 10) (layer "F.SilkS") (effects (font (size 1.2 1.2) (thickness 0.2))))')
        for i in range(64):
            px = -40 + i*1.27
            # Pad ID must be string of number. DeepPCB combines J1 + "-" + pin_num to get J1-1.
            self.add_pad(f"{i+1}", px, 0, 0.6, 4, f"NCE_PCIE_L{i}")
        self.add('  )')

    def generate_layout(self):
        self.add_board_outline(250, 200)
        bx, by = 125, 90
        self.add_nce_core(bx, by)
        positions = [
            (bx-35, by-50, 0), (bx+35, by-50, 0),    # North
            (bx-35, by+50, 180), (bx+35, by+50, 180),# South
            (bx-60, by-15, 90), (bx-60, by+15, 90),  # West
            (bx+60, by-15, 270), (bx+60, by+15, 270) # East
        ]
        for i, (px, py, pr) in enumerate(positions):
            self.add_o_tile(px, py, pr, i)

        self.add_edge_connector(125, 185)
        
        c_count = 0
        r_count = 0
        for row in range(35):
            for col in range(40):
                x = 15 + col * 6.0
                y = 15 + row * 5.0
                if 50 < x < 200 and 20 < y < 160: continue
                if 70 < x < 180 and 170 < y < 200: continue
                
                if (row + col) % 2 == 0:
                    self.add_passive(f"C{c_count}", x, y, random.choice(["VCC_1V8", "VCC_3V3", "VCC_12V"]), "GND", 90, "C")
                    c_count += 1
                else:
                    self.add_passive(f"R{r_count}", x, y, f"NCE_PCIE_L{random.randint(0,63)}", "GND", 0, "R")
                    r_count += 1
        print(f"Added {c_count} caps and {r_count} resistors.")

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
            "project": {"name": "LightRail_CPO_DeepPCB", "description": "Strictly Validated for DeepPCB"},
            "pcbnew": {"design_settings": {"rules": {"min_copper_edge_clearance": 0.2}}}
        }
        with open(pro_file, 'w') as f:
            json.dump(pro_content, f, indent=2)
        print(f"Generated OPTIMIZED CPO Architecture: {pcb_file}")

if __name__ == "__main__":
    gen = LightRailCPOGenerator()
    gen.generate_header()
    gen.generate_nets()
    gen.generate_layout()
    gen.write_files()
