"""
LightRail AI Accelerator KiCad PCB Generator (V2 Compliance)
- Strict S-expression ordering (Setup > Nets > Footprints > Graphics)
- Footprint rotation fields always included (at X Y 0)
- Used-nets-only netlist (Removes noisy dummy nets)
- Perfectly closed gr_line board outline segments at the end of file
"""

import json
import random
import math

class LightRailKiCadGenerator:
    def __init__(self, project_name="tfln_modulator"):
        self.project_name = project_name
        self.net_id_counter = 0
        self.nets = {} # name -> id
        self.used_nets = set()
        self.footprints = []
        self.graphics = []
        random.seed(42)

    def get_net_id(self, name):
        if not name: return 0
        self.used_nets.add(name)
        if name in self.nets:
            return self.nets[name]
        self.net_id_counter += 1
        self.nets[name] = self.net_id_counter
        return self.net_id_counter

    def add_pad(self, num, x, y, w, h, net, shape="rect"):
        nid = self.get_net_id(net)
        net_str = f'(net {nid} "{net}")' if net else ""
        return f'    (pad "{num}" smd {shape} (at {x:.3f} {y:.3f}) (size {w} {h}) (layers "F.Cu" "F.Paste" "F.Mask") {net_str})'

    def add_bga(self, ref, cx, cy, size, rows, cols, nets):
        fp = [f'  (footprint "BGA:{ref}" (layer "F.Cu") (at {cx} {cy} 0) (attr smd)']
        fp.append(f'    (fp_text reference "{ref}" (at 0 {-size/2 - 5} 0) (layer "F.SilkS") (effects (font (size 2 2) (thickness 0.25))))')
        
        pitch = size / (max(rows, cols) + 1)
        idx = 0
        for r in range(rows):
            for c in range(cols):
                px = -size/2 + pitch * (c + 1)
                py = -size/2 + pitch * (r + 1)
                net = nets[idx % len(nets)] if nets else "GND"
                fp.append(self.add_pad(idx+1, px, py, 0.3, 0.3, net, "circle"))
                idx += 1
        fp.append('  )')
        self.footprints.append('\n'.join(fp))

    def add_smd_2pin(self, ref, x, y, net1, net2, rot=0, pkg="0201"):
        pitch = 0.3 if pkg == "0201" else (0.5 if pkg == "0402" else 0.2)
        fp = [f'  (footprint "SMD:{pkg}" (layer "F.Cu") (at {x:.3f} {y:.3f} {rot}) (attr smd)']
        fp.append(self.add_pad("1", -pitch, 0, 0.3, 0.4, net1))
        fp.append(self.add_pad("2", pitch, 0, 0.3, 0.4, net2))
        fp.append('  )')
        self.footprints.append('\n'.join(fp))

    def add_inductor(self, ref, x, y, net1, net2):
        fp = [f'  (footprint "Inductor:SMD" (layer "F.Cu") (at {x} {y} 0) (attr smd)']
        fp.append(self.add_pad("1", -3, 0, 3, 5, net1))
        fp.append(self.add_pad("2", 3, 0, 3, 5, net2))
        fp.append('  )')
        self.footprints.append('\n'.join(fp))

    def add_qfn(self, ref, x, y, pins, size, nets):
        fp = [f'  (footprint "Package:QFN-{pins}" (layer "F.Cu") (at {x} {y} 0) (attr smd)']
        for p in range(pins):
            ang = (p / pins) * 360
            px = (size/2) * math.cos(math.radians(ang))
            py = (size/2) * math.sin(math.radians(ang))
            net = nets[p % len(nets)] if nets else "GND"
            fp.append(self.add_pad(p+1, px, py, 0.2, 0.5, net))
        fp.append('  )')
        self.footprints.append('\n'.join(fp))

    def add_crystal(self, ref, x, y, n_in, n_out):
        fp = [f'  (footprint "Crystal:SMD" (layer "F.Cu") (at {x} {y} 0) (attr smd)']
        fp.append(self.add_pad(1, -1.2, -0.8, 1, 1, n_in))
        fp.append(self.add_pad(2, 1.2, -0.8, 1, 1, "GND"))
        fp.append(self.add_pad(3, 1.2, 0.8, 1, 1, n_out))
        fp.append(self.add_pad(4, -1.2, 0.8, 1, 1, "GND"))
        fp.append('  )')
        self.footprints.append('\n'.join(fp))

    def generate_board(self):
        # 1. GPU Core
        gpu_nets = ["GND", "VCC_GPU", "VCC_IO", "VCC_PLL"] * 600
        self.add_bga("U1_GPU", 140, 70, 50, 49, 49, gpu_nets)

        # 2. Memory
        for i in range(12):
            mx = 85 if i < 4 else (195 if i < 8 else 110 + (i-8)*20)
            my = 40 + (i%4)*20 if i < 8 else 110
            mem_nets = [f"MEM{i}_DQ{b}" for b in range(32)] + ["GND", "VCC_MEM"] * 50
            self.add_bga(f"U_MEM{i}", mx, my, 12, 14, 14, mem_nets)

        # 3. VRM
        for i in range(20):
            lx = 40 + i*12 if i < 10 else 260
            ly = 15 if i < 10 else 30 + (i-10)*10
            self.add_inductor(f"L{i}", lx, ly, "+12V", "VCC_PHASE")

        # 4. Decoupling (Extreme Density for 2000+ Components)
        for i in range(2400):
            r = random.uniform(5, 140)
            ang = random.uniform(0, 360)
            x = 150 + r * math.cos(math.radians(ang))
            y = 70 + r * math.sin(math.radians(ang))
            if 1 < x < 299 and 1 < y < 139:
                net = "VCC_GPU" if i % 4 == 0 else ("VCC_MEM" if i % 4 == 1 else ("VCC_PLL" if i % 4 == 2 else "GND"))
                pkg = random.choice(["0201", "0402"])
                self.add_smd_2pin(f"D_CAP_{i}", x, y, net, "GND", rot=random.choice([0, 90, 180, 270]), pkg=pkg)

        # 4a. Logic Buffer Array (Additional Complexity)
        for i in range(250):
            x, y = random.uniform(5, 295), random.uniform(5, 135)
            self.add_qfn(f"U_BUF{i}", x, y, 6, 1.5, ["GND", "VCC_IO", "BUF_IN", "BUF_OUT"])

        # 5. Crystals
        self.add_crystal("Y1", 100, 25, "Y1_IN", "Y1_OUT")
        self.add_crystal("Y2", 180, 25, "Y2_IN", "Y2_OUT")

        # 6. Control
        self.add_qfn("U_FMU", 50, 70, 32, 5, ["GND", "VCC_IO", "FMU_DATA", "FMU_CLK"])
        self.add_qfn("U_IMU", 230, 70, 32, 5, ["GND", "VCC_IO", "IMU_DATA", "IMU_CLK"])

        # 7. Beyond Binary Components (15-Layer Upgrade)
        # Memristive Synaptic Grid (Layer 4)
        for i in range(4):
            self.add_bga(f"U_MEMRISTOR_{i}", 110 + i*20, 90, 10, 10, 10, ["MEMR_A", "MEMR_B", "GND", "V_ANA"])
        
        # Ternary Logic Encoders (Layer 6)
        for i in range(8):
            self.add_qfn(f"U_TERNARY_{i}", 30 + i*30, 120, 48, 7, ["TRIT_P", "TRIT_N", "TRIT_0", "GND"])

        # Analog Wave Compute Modules (Layer 3)
        for i in range(2):
            self.add_bga(f"U_ANALOG_WAVE_{i}", 70 + i*140, 45, 15, 12, 12, ["WAVE_P", "WAVE_N", "GND"])

        # Board Outline (Graphics)
        w, h = 300, 140
        self.graphics.append(f'  (gr_line (start 0 0) (end {w} 0) (layer "Edge.Cuts") (width 0.15))')
        self.graphics.append(f'  (gr_line (start {w} 0) (end {w} {h}) (layer "Edge.Cuts") (width 0.15))')
        self.graphics.append(f'  (gr_line (start {w} {h}) (end 0 {h}) (layer "Edge.Cuts") (width 0.15))')
        self.graphics.append(f'  (gr_line (start 0 {h}) (end 0 0) (layer "Edge.Cuts") (width 0.15))')

    def write_files(self):
        pcb = [
            f'(kicad_pcb (version 20211014) (generator pcbnew) (host antigravity 1.0)',
            '  (general (thickness 1.6))',
            '  (paper "A2")',
            '  (layers',
            '    (0 "F.Cu" signal)',
            '    (1 "In1.Cu" signal)',
            '    (2 "In2.Cu" signal)',
            '    (3 "In3.Cu" signal)',
            '    (4 "In4.Cu" signal)',
            '    (5 "In5.Cu" signal)',
            '    (6 "In6.Cu" signal)',
            '    (7 "In7.Cu" signal)',
            '    (8 "In8.Cu" signal)',
            '    (9 "In9.Cu" signal)',
            '    (10 "In10.Cu" signal)',
            '    (11 "In11.Cu" signal)',
            '    (12 "In12.Cu" signal)',
            '    (13 "In13.Cu" signal)',
            '    (31 "B.Cu" signal)',
            '    (44 "Edge.Cuts" user "Edge.Cuts")',
            '  )',
            '  (setup',
            '    (stackup',
            '      (layer "F.Cu" (type "copper") (thickness 0.035))',
            '      (layer "dielectric 1" (type "prepreg") (thickness 0.1) (material "FR4"))',
            '      (layer "In1.Cu" (type "copper") (thickness 0.035))',
            '      (layer "dielectric 2" (type "core") (thickness 0.2) (material "FR4"))',
            '      (layer "In2.Cu" (type "copper") (thickness 0.035))',
            '      (layer "dielectric 3" (type "core") (thickness 0.2) (material "FR4"))',
            '      (layer "In3.Cu" (type "copper") (thickness 0.035))',
            '      (layer "dielectric 4" (type "core") (thickness 0.2) (material "FR4"))',
            '      (layer "In4.Cu" (type "copper") (thickness 0.035))',
            '      (layer "dielectric 5" (type "core") (thickness 0.2) (material "FR4"))',
            '      (layer "In5.Cu" (type "copper") (thickness 0.035))',
            '      (layer "dielectric 6" (type "core") (thickness 0.2) (material "FR4"))',
            '      (layer "In6.Cu" (type "copper") (thickness 0.035))',
            '      (layer "dielectric 7" (type "core") (thickness 0.2) (material "FR4"))',
            '      (layer "In7.Cu" (type "copper") (thickness 0.035))',
            '      (layer "dielectric 8" (type "core") (thickness 0.2) (material "FR4"))',
            '      (layer "In8.Cu" (type "copper") (thickness 0.035))',
            '      (layer "dielectric 9" (type "core") (thickness 0.2) (material "FR4"))',
            '      (layer "In9.Cu" (type "copper") (thickness 0.035))',
            '      (layer "dielectric 10" (type "core") (thickness 0.2) (material "FR4"))',
            '      (layer "In10.Cu" (type "copper") (thickness 0.035))',
            '      (layer "dielectric 11" (type "core") (thickness 0.2) (material "FR4"))',
            '      (layer "In11.Cu" (type "copper") (thickness 0.035))',
            '      (layer "dielectric 12" (type "core") (thickness 0.2) (material "FR4"))',
            '      (layer "In12.Cu" (type "copper") (thickness 0.035))',
            '      (layer "dielectric 13" (type "core") (thickness 0.2) (material "FR4"))',
            '      (layer "In13.Cu" (type "copper") (thickness 0.035))',
            '      (layer "dielectric 14" (type "core") (thickness 0.2) (material "FR4"))',
            '      (layer "B.Cu" (type "copper") (thickness 0.035))',
            '    )',
            '    (pad_to_mask_clearance 0.05)',
            '    (design_settings (defaults (track_width 0.15) (via_size 0.3) (via_drill 0.2)))',
            '  )'
        ]

        # Add Nets
        pcb.append('  (net 0 "")')
        sorted_nets = sorted(self.nets.items(), key=lambda x: x[1])
        for name, nid in sorted_nets:
            if name in self.used_nets:
                pcb.append(f'  (net {nid} "{name}")')

        # Add Footprints
        pcb.extend(self.footprints)

        # Add Graphics (Outline)
        pcb.extend(self.graphics)

        pcb.append(')')

        with open(f"{self.project_name}.kicad_pcb", 'w') as f:
            f.write('\n'.join(pcb))
        
        # Standard .kicad_pro
        pro = {
            "meta": {"version": 1, "filename": f"{self.project_name}.kicad_pro"},
            "board": {"design_settings": {"defaults": {"track_width": 0.15, "via_size": 0.3}}}
        }
        with open(f"{self.project_name}.kicad_pro", 'w') as f:
            json.dump(pro, f, indent=2)
            
        print(f"✅ Generated {self.project_name}.kicad_pcb with {len(self.footprints)} components and {len(self.used_nets)} used nets.")

if __name__ == "__main__":
    gen = LightRailKiCadGenerator()
    gen.generate_board()
    gen.write_files()
