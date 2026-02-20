"""
LightRail AI Pluggable Interconnect - 15-Layer KiCad Generator
Matches TDS: Rogers 4350B Hybrid Stack + PCIe Gen5 x16 + TFLN CPO
"""

import json
import os

class LightRailPluggableGenerator:
    def __init__(self, project_name="lightrail_pluggable"):
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
        self.add('(kicad_pcb (version 20211014) (generator lightrail_hd_gen)')
        self.add('  (general (thickness 1.6))')
        self.add('  (paper "A3")')
        self.add('  (layers')
        # 15-Layer Stackup
        self.add('    (0 "L1_Top_RF" signal)')
        self.add('    (1 "L2_GND_RF" power)')
        self.add('    (2 "L3_SerDes" signal)')
        self.add('    (3 "L4_GND_SerDes" power)')
        self.add('    (4 "L5_Control" signal)')
        self.add('    (5 "L6_Power_1V8" power)')
        self.add('    (6 "L7_GND_Dig" power)')
        self.add('    (7 "L8_NCE_Neuron" signal)')
        self.add('    (8 "L9_GND_Dig" power)')
        self.add('    (9 "L10_Power_3V3" power)')
        self.add('    (10 "L11_Fanout" signal)')
        self.add('    (11 "L12_GND_Analog" power)')
        self.add('    (12 "L13_Power_Bias" power)')
        self.add('    (13 "L14_GND_Bot" power)')
        self.add('    (31 "L15_Bot_Signal" signal)')
        # Standard mask/silk
        self.add('    (36 "B.SilkS" user)')
        self.add('    (37 "F.SilkS" user)')
        self.add('    (38 "B.Mask" user)')
        self.add('    (39 "F.Mask" user)')
        self.add('    (44 "Edge.Cuts" user)')
        self.add('  )')

    def generate_nets(self):
        self.add('  (net 0 "")')
        # Power Rails from TDS
        for net in ["GND", "VCC_3V3", "VCC_1V8", "VCC_12V", "VEE_n5V", "V_BIAS", "GND_ANALOG"]:
            nid = self.add_net(net)
            self.add(f'  (net {nid} "{net}")')
            
        # PCIe Gen5 x16 (64 signals)
        for lane in range(16):
            for sig in ["TX_P", "TX_N", "RX_P", "RX_N"]:
                net = f"PCIE{lane}_{sig}"
                nid = self.add_net(net)
                self.add(f'  (net {nid} "{net}")')
                
        # TFLN Modulator RF Drive (8 Channels)
        for ch in range(8):
            net = f"TFLN_RF_CH{ch}"
            nid = self.add_net(net)
            self.add(f'  (net {nid} "{net}")')

    def add_pad(self, num, x, y, w, h, net, shape="rect", layer="L1_Top_RF"):
        net_id = self.nets.get(net, 0)
        self.add(f'    (pad "{num}" smd {shape} (at {x:.2f} {y:.2f}) (size {w} {h}) (layers "{layer}" "F.Paste" "F.Mask") (net {net_id} "{net}"))')

    def add_tfln_modulator(self, cx, cy):
        """U1: TFLN-MZM-400G-C"""
        self.add(f'  (footprint "LightRail:TFLN_MZM_400G" (layer "L1_Top_RF")')
        self.add(f'    (at {cx} {cy})')
        self.add(f'    (fp_text reference "U1" (at 0 -8) (layer "F.SilkS") (effects (font (size 1.2 1.2) (thickness 0.15))))')
        # RF Pads (Differential Drive)
        for i in range(8):
            self.add_pad(f"RF_{i}", -10 + i*2.5, 5, 0.4, 1.5, f"TFLN_RF_CH{i}")
        # Thermal Pad
        self.add_pad("TH", 0, 0, 15, 12, "GND", "rect")
        self.add('  )')

    def add_serdes_retimer(self, cx, cy):
        """U9: BCM84881 Broadcom Retimer"""
        self.add(f'  (footprint "Broadcom:BCM84881_BGA" (layer "L1_Top_RF")')
        self.add(f'    (at {cx} {cy})')
        self.add(f'    (fp_text reference "U9" (at 0 -12) (layer "F.SilkS") (effects (font (size 1.5 1.5) (thickness 0.2))))')
        # Fake BGA array for placement
        for r in range(10):
            for c in range(10):
                px = -9 + c*2
                py = -9 + r*2
                self.add_pad(f"{r}_{c}", px, py, 0.5, 0.5, "GND", "circle")
        self.add('  )')

    def add_edge_connector(self, cx, cy):
        """J1: PCIe Gen5 x16 Edge"""
        self.add(f'  (footprint "TE:PCIe_Gen5_x16" (layer "L1_Top_RF")')
        self.add(f'    (at {cx} {cy})')
        self.add(f'    (fp_text reference "J1" (at 0 -5) (layer "F.SilkS") (effects (font (size 1.2 1.2) (thickness 0.15))))')
        pitch = 1.0
        for i in range(64):
            px = -31.5 + i*pitch
            lane = i // 4
            sig = ["TX_P", "TX_N", "RX_P", "RX_N"][i % 4]
            self.add_pad(f"{i+1}", px, 0, 0.6, 4, f"PCIE{lane}_{sig}")
        self.add('  )')

    def add_board_outline(self, w, h):
        self.add(f'  (gr_line (start 0 0) (end {w} 0) (layer "Edge.Cuts") (width 0.15))')
        self.add(f'  (gr_line (start {w} 0) (end {w} {h}) (layer "Edge.Cuts") (width 0.15))')
        self.add(f'  (gr_line (start {w} {h}) (end 0 {h}) (layer "Edge.Cuts") (width 0.15))')
        self.add(f'  (gr_line (start 0 {h}) (end 0 0) (layer "Edge.Cuts") (width 0.15))')

    def generate_layout(self):
        # 167mm x 111mm (Standard PCIe Half Length)
        self.add_board_outline(167, 111)
        # Components
        self.add_tfln_modulator(40, 40)
        self.add_serdes_retimer(80, 40)
        self.add_edge_connector(83.5, 107)

    def write_files(self):
        self.add(')')
        output_file = f"{self.project_name}.kicad_pcb"
        with open(output_file, 'w') as f:
            f.write('\n'.join(self.pcb_content))
        print(f"Generated {output_file}")

if __name__ == "__main__":
    gen = LightRailPluggableGenerator()
    gen.generate_header()
    gen.generate_nets()
    gen.generate_layout()
    gen.write_files()
