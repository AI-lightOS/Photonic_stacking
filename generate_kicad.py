import os
import datetime

class KiCadGenerator:
    def __init__(self, filename="tfln_modulator.kicad_pcb"):
        self.filename = filename
        self.content = []

    def add(self, line):
        self.content.append(line)

    def generate_header(self):
        self.add('(kicad_pcb (version 20211014) (generator pcbnew)')
        self.add('  (general')
        self.add(f'    (thickness 1.6)')
        self.add('  )')
        self.add('  (paper "A3")')
        self.add('  (layers')
        self.add('    (0 "F.Cu" signal)')
        self.add('    (1 "In1.Cu" power)')
        self.add('    (2 "In2.Cu" signal)')
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
        self.add('    (stackup')
        self.add('      (layer "F.Cu" (type "signal") (thickness 0.035))')
        self.add('      (layer "In1.Cu" (type "power_plane") (thickness 0.035))')
        self.add('      (layer "In2.Cu" (type "signal") (thickness 0.035))')
        self.add('      (layer "B.Cu" (type "signal") (thickness 0.035))')
        self.add('      (layer "F.Mask" (type "solder_mask") (thickness 0.01))')
        self.add('      (layer "B.Mask" (type "solder_mask") (thickness 0.01))')
        self.add('    )')
        self.add('  )')

    def add_net(self, code, name):
        self.add(f'  (net {code} "{name}")')

    def add_footprint_rect(self, ref, x, y, w, h, layer="F.Cu"):
        # Simplified footprint generation
        self.add(f'  (footprint "ManualPkg:{ref}" (layer "{layer}")')
        self.add(f'    (at {x} {y})')
        self.add(f'    (attr smd)')
        self.add(f'    (fp_text reference "{ref}" (at 0 -{h/2 + 1}) (layer "F.SilkS")')
        self.add(f'      (effects (font (size 1 1) (thickness 0.15)))')
        self.add('    )')
        # Pad 1
        self.add(f'    (pad "1" smd rect (at -{w/3} 0) (size {w/4} {h/2}) (layers "{layer}" "F.Paste" "F.Mask"))')
        # Pad 2
        self.add(f'    (pad "2" smd rect (at {w/3} 0) (size {w/4} {h/2}) (layers "{layer}" "F.Paste" "F.Mask"))')
        self.add('  )')

    def add_trace(self, x1, y1, x2, y2, width=0.2, layer="F.Cu", net=0):
        self.add(f'  (segment (start {x1} {y1}) (end {x2} {y2}) (width {width}) (layer "{layer}") (net {net}))')

    def generate_components(self):
        # Add core processor
        self.add_footprint_rect("U1", 100, 100, 20, 20) # Center board approx 100,100 mm in KiCad space
        
        # Add basic traces
        # PCIe Bus traces
        for i in range(16):
            y_off = i * 0.5
            self.add_trace(50, 100+y_off, 90, 100+y_off)

    def write_file(self):
        self.add(')') # Close kicad_pcb
        with open(self.filename, 'w') as f:
            f.write('\n'.join(self.content))
        print(f"Generated {self.filename}")

if __name__ == "__main__":
    gen = KiCadGenerator()
    gen.generate_header()
    gen.generate_setup()
    
    # Nets
    gen.add_net(0, "")
    gen.add_net(1, "GND")
    gen.add_net(2, "+3V3")
    gen.add_net(3, "PCIE_TX")
    
    gen.generate_components()
    gen.write_file()
