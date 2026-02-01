"""
Fixed KiCad PCB Generator for DeepPCB
- Proper net assignments to pins
- Non-overlapping pad positions
- Actual routing connections needed
"""

import json

class FixedKiCadGenerator:
    def __init__(self, project_name="tfln_modulator"):
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
        self.add('(kicad_pcb (version 20211014) (generator fixed_generator)')
        self.add('  (general')
        self.add('    (thickness 1.6)')
        self.add('  )')
        self.add('  (paper "A3")')
        
        # 4-layer stackup (simpler for routing)
        self.add('  (layers')
        self.add('    (0 "F.Cu" signal)')
        self.add('    (1 "In1.Cu" power)')
        self.add('    (2 "In2.Cu" power)')
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
        # Pre-define all nets
        self.add('  (net 0 "")')
        
        # Power nets
        for net_name in ["GND", "VCC", "+3V3", "+1V8"]:
            nid = self.add_net(net_name)
            self.add(f'  (net {nid} "{net_name}")')
        
        # Signal nets for routing
        for i in range(1, 21):
            net_name = f"SIG{i}"
            nid = self.add_net(net_name)
            self.add(f'  (net {nid} "{net_name}")')

    def add_chip(self, ref, x, y, size, pin_nets):
        """Add a chip with BGA-style pads and net assignments"""
        num_pins = len(pin_nets)
        grid = int(num_pins ** 0.5)
        if grid * grid < num_pins:
            grid += 1
        pitch = size / (grid + 1)
        
        self.add(f'  (footprint "Custom:{ref}" (layer "F.Cu")')
        self.add(f'    (at {x} {y})')
        self.add(f'    (attr smd)')
        self.add(f'    (fp_text reference "{ref}" (at 0 {-size/2 - 2}) (layer "F.SilkS")')
        self.add(f'      (effects (font (size 1 1) (thickness 0.15)))')
        self.add('    )')
        
        pad_num = 1
        for row in range(grid):
            for col in range(grid):
                if pad_num > num_pins:
                    break
                px = -size/2 + pitch * (col + 1)
                py = -size/2 + pitch * (row + 1)
                net_name = pin_nets[pad_num - 1] if pad_num <= len(pin_nets) else ""
                net_id = self.nets.get(net_name, 0)
                self.add(f'    (pad "{pad_num}" smd circle (at {px:.3f} {py:.3f}) (size 0.5 0.5) (layers "F.Cu" "F.Paste" "F.Mask") (net {net_id} "{net_name}"))')
                pad_num += 1
        
        self.add('  )')

    def add_two_pin_component(self, ref, x, y, net1, net2, rotation=0):
        """Add a simple 2-pin component (capacitor/resistor)"""
        net1_id = self.nets.get(net1, 0)
        net2_id = self.nets.get(net2, 0)
        
        self.add(f'  (footprint "Capacitor_SMD:C_0603" (layer "F.Cu")')
        self.add(f'    (at {x} {y} {rotation})')
        self.add(f'    (attr smd)')
        self.add(f'    (fp_text reference "{ref}" (at 0 -1.5) (layer "F.SilkS")')
        self.add(f'      (effects (font (size 0.8 0.8) (thickness 0.12)))')
        self.add('    )')
        # Pads spaced 1.6mm apart (standard 0603)
        self.add(f'    (pad "1" smd rect (at -0.8 0) (size 0.8 0.9) (layers "F.Cu" "F.Paste" "F.Mask") (net {net1_id} "{net1}"))')
        self.add(f'    (pad "2" smd rect (at 0.8 0) (size 0.8 0.9) (layers "F.Cu" "F.Paste" "F.Mask") (net {net2_id} "{net2}"))')
        self.add('  )')

    def add_board_outline(self):
        """Add board edge cuts - 60mm x 40mm"""
        self.add('  (gr_line (start 0 0) (end 60 0) (layer "Edge.Cuts") (width 0.15))')
        self.add('  (gr_line (start 60 0) (end 60 40) (layer "Edge.Cuts") (width 0.15))')
        self.add('  (gr_line (start 60 40) (end 0 40) (layer "Edge.Cuts") (width 0.15))')
        self.add('  (gr_line (start 0 40) (end 0 0) (layer "Edge.Cuts") (width 0.15))')

    def generate_design(self):
        """Generate a simple but routable design"""
        
        # Board outline
        self.add_board_outline()
        
        # Main processor U1 - center of board
        # 16-pin chip with mix of power and signal
        u1_nets = ["VCC", "GND", "SIG1", "SIG2", "SIG3", "SIG4", 
                   "SIG5", "SIG6", "SIG7", "SIG8", "GND", "VCC",
                   "SIG9", "SIG10", "+3V3", "GND"]
        self.add_chip("U1", 30, 20, 10, u1_nets)
        
        # Secondary chip U2 - left side
        u2_nets = ["VCC", "GND", "SIG1", "SIG11", "SIG12", "SIG13",
                   "+3V3", "GND", "SIG14"]
        self.add_chip("U2", 12, 20, 6, u2_nets)
        
        # Connector J1 - right side
        j1_nets = ["SIG2", "SIG3", "SIG4", "SIG5", "GND", "VCC",
                   "SIG15", "SIG16", "SIG17"]
        self.add_chip("J1", 50, 20, 6, j1_nets)
        
        # Decoupling capacitors - properly spaced
        # C1: VCC to GND near U1
        self.add_two_pin_component("C1", 25, 12, "VCC", "GND", 0)
        
        # C2: +3V3 to GND near U1
        self.add_two_pin_component("C2", 35, 12, "+3V3", "GND", 0)
        
        # C3: VCC to GND near U2
        self.add_two_pin_component("C3", 12, 12, "VCC", "GND", 0)
        
        # C4: VCC to GND near J1
        self.add_two_pin_component("C4", 50, 12, "VCC", "GND", 0)
        
        # Additional signal routing caps
        self.add_two_pin_component("C5", 25, 28, "SIG6", "GND", 0)
        self.add_two_pin_component("C6", 35, 28, "SIG7", "GND", 0)

    def write_files(self):
        self.add(')')
        
        # Write PCB file
        pcb_file = f"{self.project_name}.kicad_pcb"
        with open(pcb_file, 'w') as f:
            f.write('\n'.join(self.pcb_content))
        print(f"Generated {pcb_file}")
        
        # Write project file
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
                    "track_widths": [0.2, 0.3, 0.5],
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
                    "track_width": 0.25,
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
        print(f"Generated {pro_file}")
        
        # Print routing summary
        print(f"\n✅ Design ready for DeepPCB!")
        print(f"   - {len(self.nets)} nets defined")
        print(f"   - Nets need routing: SIG1-SIG17, VCC, GND, +3V3")


if __name__ == "__main__":
    gen = FixedKiCadGenerator()
    gen.generate_header()
    gen.generate_setup()
    gen.generate_nets()
    gen.generate_design()
    gen.write_files()
