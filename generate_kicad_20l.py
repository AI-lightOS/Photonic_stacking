"""
LightRail AI: The 20-Layer Photonic Intelligence Stack
Generates a 20-layer KiCad PCB substrate with specific functional layer assignments
optimized for DeepPCB and CircuitMaker.
"""

import json
import os
import uuid
import random

class LightRail20LGenerator:
    def __init__(self, project_name="lightrail_20l"):
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
        self.add('(kicad_pcb (version 20211014) (generator lightrail_20l_gen)')
        self.add('  (general (thickness 2.0))')
        self.add('  (paper "A3")')
        self.add('  (title_block')
        self.add('    (title "LightRail AI: The 20-Layer Photonic Intelligence Stack")')
        self.add('    (company "LightRail Intelligence")')
        self.add('    (rev "4.0")')
        self.add('  )')
        self.add('  (layers')
        
        # Mapping the 20 layers based on the Phase 1-7 Roadmap
        layer_defs = [
            (0, "F.Cu", "signal", "Analog Power Interposer (L1 - Phase 1)"),
            (1, "In1.Cu", "power", "Integrated Light Engine (L2 - Phase 1)"),
            (2, "In2.Cu", "signal", "TFLN 3D Interposer (L3 - Phase 2)"),
            (3, "In3.Cu", "power", "Optical Circuit Switching (L4 - Phase 2)"),
            (4, "In4.Cu", "signal", "Multi-Spectral WDM Plane (L5 - Phase 2)"),
            (5, "In5.Cu", "signal", "Analog Wave Compute (L6 - Phase 3)"),
            (6, "In6.Cu", "power", "Memristive Synaptic Grid (L7 - Phase 3)"),
            (7, "In7.Cu", "signal", "Analog Signal Restoration (L8 - Phase 3)"),
            (8, "In8.Cu", "signal", "Ternary Logic Encoder (L9 - Phase 4)"),
            (9, "In9.Cu", "power", "Spiking Logic Dispatcher (L10 - Phase 4)"),
            (10, "In10.Cu", "signal", "ABFP Handler (L11 - Phase 4)"),
            (11, "In11.Cu", "signal", "Dynamic Tensor Rearrangement (L12 - Phase 4)"),
            (12, "In12.Cu", "power", "Deterministic Kernel Integration (L13 - Phase 5)"),
            (13, "In13.Cu", "signal", "Topology-Aware Routing (L14 - Phase 5)"),
            (14, "In14.Cu", "power", "Collective Optimization Engine (L15 - Phase 5)"),
            (15, "In15.Cu", "signal", "Photonic Compiler (L16 - Phase 6)"),
            (16, "In16.Cu", "signal", "Fabric OS Global Scheduler (L17 - Phase 6)"),
            (17, "In17.Cu", "power", "Framework Adapters / The Shim (L18 - Phase 6)"),
            (18, "In18.Cu", "signal", "Holographic Unified Memory (L19 - Phase 7)"),
            (31, "B.Cu", "signal", "Exascale AI Workload Plane (L20 - Phase 7)")
        ]
        
        for idx, name, ltype, desc in layer_defs:
            self.add(f'    ({idx} "{name}" {ltype}) # {desc}')
            
        self.add('    (36 "B.SilkS" user) (37 "F.SilkS" user) (38 "B.Mask" user) (39 "F.Mask" user)')
        self.add('    (44 "Edge.Cuts" user)')
        self.add('  )')
        
        self.add('  (setup')
        self.add('    (stackup')
        for i, (idx, name, ltype, desc) in enumerate(layer_defs):
            mtype = "copper" if ltype in ["signal", "power"] else "technical"
            self.add(f'      (layer "{name}" (type "{mtype}") (thickness 0.018))')
            if i < len(layer_defs) - 1:
                self.add(f'      (layer "dieletric {i+1}" (type "core") (thickness 0.05) (material "Rogers 4350B") (epsilon_r 3.66))')
        self.add('    )')
        self.add('    (last_trace_width 0.075) (trace_clearance 0.075) (min_trace_width 0.05)')
        self.add('    (via_size 0.15) (via_drill 0.075)')
        self.add('    (net_class "Default" (clearance 0.1) (trace_width 0.075) (via_dia 0.2) (via_drill 0.1))')
        self.add('  )')

    def generate_nets(self):
        self.add('  (net 0 "")')
        core_nets = ["GND", "V_ANALOG", "V_LIGHT", "TFLN_BIAS", "WDM_CTRL", "MEMRISTOR_REF", "TERNARY_CLK", "FABRIC_SYNC"]
        for net in core_nets:
            self.add(f'  (net {self.add_net(net)} "{net}")')
        # Massive net forest for 20L complexity
        for i in range(256):
            self.add(f'  (net {self.add_net(f"WAVE_BUS_{i}")} "WAVE_BUS_{i}")')

    def add_pad(self, num, x, y, w, h, net, shape="rect", layer="F.Cu"):
        net_id = self.nets.get(net, 0)
        self.add(f'    (pad "{num}" smd {shape} (at {x:.3f} {y:.3f}) (size {w} {h}) (layers "{layer}" "F.Paste" "F.Mask") (net {net_id} "{net}"))')

    def add_intelligence_stack(self, cx, cy):
        """The 20-Layer 3D Intelligence Stack Core"""
        tstamp = str(uuid.uuid4())
        self.add(f'  (footprint "LightRail:IntelligenceStack_20L" (layer "F.Cu") (tstamp {tstamp}) (locked)')
        self.add(f'    (at {cx} {cy})')
        self.add(f'    (fp_text reference "CORE1" (at 0 -25) (layer "F.SilkS") (effects (font (size 2 2) (thickness 0.4))))')
        self.add(f'    (fp_text value "20-Layer Photonic Stack" (at 0 25) (layer "F.SilkS") (effects (font (size 1.5 1.5) (thickness 0.3))))')
        
        # Ultra-dense 24x24 BGA (576 pins)
        pitch = 1.0
        for r in range(24):
            for c in range(24):
                px, py = -11.5 + c*pitch, -11.5 + r*pitch
                idx = r * 24 + c
                if 8 < r < 15 and 8 < c < 15: net = "V_ANALOG"
                else: net = f"WAVE_BUS_{idx % 256}"
                self.add_pad(f"{idx+1}", px, py, 0.4, 0.4, net, "circle")
        self.add('  )')

    def generate_layout(self):
        self.add_board_outline(280, 220)
        bx, by = 140, 110
        self.add_intelligence_stack(bx, by)
        
        # Distributed Passive Grid for the 20L Stack
        c_count = 0
        for row in range(40):
            for col in range(50):
                x = 10 + col * 5.5
                y = 10 + row * 5.5
                if 90 < x < 190 and 60 < y < 160: continue # Stack clearance
                
                tstamp = str(uuid.uuid4())
                net = random.choice(["GND", "V_ANALOG", "V_LIGHT"])
                self.add(f'  (footprint "Capacitor_SMD:C_0201_0603Metric" (layer "F.Cu") (tstamp {tstamp}) (locked)')
                self.add(f'    (at {x:.3f} {y:.3f})')
                self.add(f'    (fp_text reference "C{c_count}" (at 0 -0.5) (layer "F.SilkS") (effects (font (size 0.4 0.4) (thickness 0.08))))')
                self.add_pad("1", -0.3, 0, 0.3, 0.4, net)
                self.add_pad("2", 0.3, 0, 0.3, 0.4, "GND")
                self.add('  )')
                c_count += 1
        print(f"Added {c_count} decoupling nodes for 20L stack stability.")

    def add_board_outline(self, w, h):
        self.add(f'  (gr_poly (pts (xy 0 0) (xy {w} 0) (xy {w} {h}) (xy 0 {h})) (layer "Edge.Cuts") (width 0.15) (tstamp {uuid.uuid4()}))')

    def write_files(self):
        self.add(')')
        pcb_file = f"{self.project_name}.kicad_pcb"
        with open(pcb_file, 'w') as f:
            f.write('\n'.join(self.pcb_content))
        print(f"Generated 20-Layer Stack: {pcb_file}")

if __name__ == "__main__":
    gen = LightRail20LGenerator()
    gen.generate_header()
    gen.generate_nets()
    gen.generate_layout()
    gen.write_files()
