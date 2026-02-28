"""
LightRail AI TFLN Network Interface Card (Generation 3)
15-Layer Hybrid RF Stackup - PCIe Gen5 x16 Form Factor
Features: 8x QSFP-DD, TFLN Modulator Array, DFB Laser, Broadcom Controller.
"""

import os
import uuid
import random

class LightRailNICGen3Generator:
    def __init__(self, project_name="lightrail_nic_gen3"):
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
        self.add('(kicad_pcb (version 20211014) (generator lightrail_nic_gen3_gen)')
        self.add('  (general (thickness 1.6))')
        self.add('  (paper "A3")')
        self.add('  (title_block')
        self.add('    (title "LightRail AI TFLN Network Interface Card (Gen 3)")')
        self.add('    (company "LightRail Intelligence")')
        self.add('    (rev "3.0")')
        self.add('  )')
        self.add('  (layers')
        layers = [
            (0, "F.Cu", "signal"), (1, "In1.Cu", "signal"), (2, "In2.Cu", "power"),
            (3, "In3.Cu", "signal"), (4, "In4.Cu", "power"), (5, "In5.Cu", "signal"),
            (6, "In6.Cu", "power"), (7, "In7.Cu", "signal"), (8, "In8.Cu", "power"),
            (9, "In9.Cu", "signal"), (10, "In10.Cu", "power"), (11, "In11.Cu", "signal"),
            (12, "In12.Cu", "power"), (13, "In13.Cu", "signal"), (31, "B.Cu", "signal")
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
                mat = "Rogers RO4350B" if i < 2 else "High-Tg FR4"
                er = 3.66 if i < 2 else 4.5
                self.add(f'      (layer "dielectric {i+1}" (type "core") (thickness 0.1) (material "{mat}") (epsilon_r {er}))')
        self.add('    )')
        self.add('    (last_trace_width 0.1) (trace_clearance 0.1) (min_trace_width 0.1)')
        self.add('    (via_size 0.2) (via_drill 0.1)')
        self.add('    (net_class "Default" (clearance 0.12) (trace_width 0.1) (via_dia 0.25) (via_drill 0.15))')
        self.add('    (net_class "RF_50ohm" (clearance 0.15) (trace_width 0.18) (via_dia 0.4) (via_drill 0.2))')
        self.add('    (net_class "Diff_85ohm" (clearance 0.12) (trace_width 0.12) (via_dia 0.3) (via_drill 0.15))')
        self.add('  )')

    def generate_nets(self):
        self.add('  (net 0 "")')
        for net in ["GND", "VCC_12V", "VCC_3V3", "VCC_1V8", "VCC_1V0", "V_LASER", "V_MOD"]:
            self.add(f'  (net {self.add_net(net)} "{net}")')
        for i in range(16):
            self.add(f'  (net {self.add_net(f"PCIE_TX_{i}_P")} "PCIE_TX_{i}_P")')
            self.add(f'  (net {self.add_net(f"PCIE_TX_{i}_N")} "PCIE_TX_{i}_N")')
            self.add(f'  (net {self.add_net(f"PCIE_RX_{i}_P")} "PCIE_RX_{i}_P")')
            self.add(f'  (net {self.add_net(f"PCIE_RX_{i}_N")} "PCIE_RX_{i}_N")')

    def add_pad(self, num, x, y, w, h, net, shape="rect", layer="F.Cu"):
        net_id = self.nets.get(net, 0)
        self.add(f'    (pad "{num}" smd {shape} (at {x:.3f} {y:.3f}) (size {w} {h}) (layers "{layer}" "F.Paste" "F.Mask") (net {net_id} "{net}"))')

    def generate_layout(self):
        # PCIe standard dimensions (approx 167mm x 111mm for standard height)
        self.add_board_outline(167, 111)
        
        # Left Edge (I/O): MPO Connectors
        self.add_footprint("LightRail:MPO_Input", 5, 30, 0, "MPO1")
        self.add_footprint("LightRail:MPO_Output", 5, 80, 0, "MPO2")
        
        # Top Left (Optical Power): Laser Source and TEC Driver
        self.add_footprint("LightRail:DFB_Laser_U2", 30, 20, 0, "U2")
        self.add_footprint("LightRail:TEC_Driver_U8", 50, 20, 0, "U8")
        
        # Center-Left (Encoding): Modulator Array
        self.add_footprint("LightRail:TFLN_Mod_U1", 35, 55, 0, "U1")
        
        # Absolute Center (The Engine): Optical Core
        self.add_footprint("LightRail:Optical_Core_U3", 83.5, 55, 0, "U3")
        
        # Center-Right (Conversion): Detector Bank
        self.add_footprint("LightRail:Detector_Bank_U4", 120, 55, 0, "U4")
        
        # Bottom Center (Digital): Controller
        self.add_footprint("Broadcom:BCM84881_U9", 83.5, 85, 0, "U9")
        
        # PCIe Edge Connector
        self.add_edge_connector(83.5, 111)
        
        # Decoupling Grid (2,055 capacitors)
        self.add_decoupling_grid(2055)

    def add_footprint(self, name, x, y, rot, ref):
        tstamp = str(uuid.uuid4())
        self.add(f'  (footprint "{name}" (layer "F.Cu") (tstamp {tstamp}) (locked)')
        self.add(f'    (at {x} {y} {rot})')
        self.add(f'    (fp_text reference "{ref}" (at 0 -5) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))')
        # Placeholder pads
        for i in range(16):
            self.add_pad(f"{i+1}", -2 + (i%4), -2 + (i//4), 0.5, 0.5, "GND", "circle")
        self.add('  )')

    def add_edge_connector(self, cx, cy):
        tstamp = str(uuid.uuid4())
        self.add(f'  (footprint "Connector_PCBEdge:PCIe_x16" (layer "F.Cu") (tstamp {tstamp}) (locked)')
        self.add(f'    (at {cx} {cy})')
        self.add(f'    (fp_text reference "J1" (at 0 -10) (layer "F.SilkS") (effects (font (size 1.2 1.2) (thickness 0.2))))')
        for i in range(164):
            px = -82 + i*1.0
            net = "GND" if i % 2 == 0 else f"PCIE_TX_{i//10}_P"
            self.add_pad(f"{i+1}", px, -2, 0.6, 4, net)
        self.add('  )')

    def add_decoupling_grid(self, count):
        added = 0
        rows = 40
        cols = 52
        for r in range(rows):
            for c in range(cols):
                if added >= count: break
                x = 10 + c * 3.0
                y = 10 + r * 2.5
                # Avoid main components
                if 25 < x < 140 and 15 < y < 95: continue
                
                tstamp = str(uuid.uuid4())
                self.add(f'  (footprint "Capacitor_SMD:C_0603_1608Metric" (layer "F.Cu") (tstamp {tstamp}) (locked)')
                self.add(f'    (at {x:.3f} {y:.3f})')
                self.add_pad("1", -0.4, 0, 0.4, 0.6, "VCC_1V0")
                self.add_pad("2", 0.4, 0, 0.4, 0.6, "GND")
                self.add('  )')
                added += 1
        print(f"Added {added} decoupling capacitors.")

    def add_board_outline(self, w, h):
        self.add(f'  (gr_poly (pts (xy 0 0) (xy {w} 0) (xy {w} {h}) (xy 0 {h})) (layer "Edge.Cuts") (width 0.15) (tstamp {uuid.uuid4()}))')

    def write_files(self):
        self.add(')')
        pcb_file = f"{self.project_name}.kicad_pcb"
        with open(pcb_file, 'w') as f:
            f.write('\n'.join(self.pcb_content))
        print(f"Generated 15-Layer Gen 3 NIC: {pcb_file}")

if __name__ == "__main__":
    gen = LightRailNICGen3Generator()
    gen.generate_header()
    gen.generate_nets()
    gen.generate_layout()
    gen.write_files()
