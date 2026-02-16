"""
TFLN Photonic Interconnect - Gerber File Generator
Generates PCB design files for 12-layer TFLN modulator integration
"""

import os
from datetime import datetime

class GerberGenerator:
    """Generate Gerber files for TFLN photonic PCB with 12-layer stackup"""
    
    def __init__(self, output_dir="gerber_files"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Antigravity Specifications
        self.board_width = 106.68  # mm (Standard Half Length)
        self.board_height = 111.15  # mm (Standard Height)
        self.layers = 15
        self.material_rf = "Rogers 4350B"
        self.material_digital = "High-Tg FR4"
        
    def generate_top_copper(self):
        """Generate top copper layer (GTL)"""
        filename = f"{self.output_dir}/Antigravity_L1_Top_Cu.gtl"
        with open(filename, 'w') as f:
            f.write("G04 TFLN Photonic Modulator - Top Copper Layer (Signal)*\n")
            f.write("G04 TFLN RF Electrodes and High-Priority Signals*\n")
            f.write(f"G04 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
            f.write("%FSLAX36Y36*%\n")
            f.write("%MOIN*%\n")
            # RF Traces
            f.write("G01*\n")
            f.write("D10*\n")
            f.write("X1000000Y1000000D02*\n")
            f.write("X2000000Y1000000D01*\n")
            f.write("M02*\n")
        return filename
    
    def generate_bottom_copper(self):
        """Generate bottom copper layer (GBL)"""
        filename = f"{self.output_dir}/Antigravity_L15_Bottom_Cu.gbl"
        with open(filename, 'w') as f:
            f.write("G04 TFLN Photonic Modulator - Bottom Copper Layer (Signal/GND)*\n")
            f.write("%FSLAX36Y36*%\n")
            f.write("%MOIN*%\n")
            f.write("G01*\n")
            f.write("D10*\n")
            # Draw a simple cross for visualization
            f.write(f"X0Y0D02*\n")
            f.write(f"X{int(self.board_width*1000000)}Y{int(self.board_height*1000000)}D01*\n")
            f.write(f"X0Y{int(self.board_height*1000000)}D02*\n")
            f.write(f"X{int(self.board_width*1000000)}Y0D01*\n")
            f.write("M02*\n")
        return filename
    
    def generate_inner_layers(self):
        """Generate inner signal and power layers for Antigravity 15-layer stackup"""
        files = []
        
        # Antigravity 15-Layer Stackup Definition
        layer_specs = [
            (2, "Ground", "g2", "RF Reference Plane (Rogers 4350B)"),
            (3, "Signal", "g3", "High-Speed SerDes (Rx/Tx) (Rogers 4350B)"),
            (4, "Ground", "g4", "SerDes Reference (Copper)"),
            (5, "Signal", "g5", "Low-Speed Control (I2C, SPI, GPIO) (FR4)"),
            (6, "Power", "g6", "1.8V Rail (LDO Output) (FR4)"),
            (7, "Ground", "g7", "Digital Ground (Copper)"),
            (8, "Signal", "g8", "NCE Neuron Interconnects (FR4)"),
            (9, "Ground", "g9", "Digital Ground (Copper)"),
            (10, "Power", "g10", "3.3V Rail (Main Power) (FR4)"),
            (11, "Signal", "g11", "FPGA/Controller Fanout (FR4)"),
            (12, "Ground", "g12", "Analog Ground (Copper)"),
            (13, "Power", "g13", "-5V / 12V (Bias/TEC) (FR4)"),
            (14, "Ground", "g14", "Bottom Reference (Copper)")
        ]
        
        for layer_num, desc, ext, details in layer_specs:
            filename = f"{self.output_dir}/LightRailAI_L{layer_num}_{desc.replace(' ', '_')}.{ext}"
            with open(filename, 'w') as f:
                f.write(f"G04 TFLN Modulator - Layer {layer_num} ({desc})*\n")
                f.write(f"G04 {details}*\n")
                f.write(f"G04 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
                f.write("%FSLAX36Y36*%\n")
                f.write("%MOIN*%\n")
                f.write("G01*\n")
                f.write("D10*\n")
                # Draw a simple cross for visualization
                f.write(f"X0Y0D02*\n")
                f.write(f"X{int(self.board_width*1000000)}Y{int(self.board_height*1000000)}D01*\n")
                f.write(f"X0Y{int(self.board_height*1000000)}D02*\n")
                f.write(f"X{int(self.board_width*1000000)}Y0D01*\n")
                f.write("M02*\n")
            files.append(filename)
            
        return files
    
    def generate_drill_file(self):
        """Generate drill file"""
        filename = f"{self.output_dir}/tfln_modulator.drl"
        with open(filename, 'w') as f:
            f.write("M48\n")
            f.write("; 15-Layer TFLN Modulator Drill File\n")
            f.write("M30\n")
        return filename

    def generate_soldermask(self):
        """Generate solder mask layers"""
        files = []
        for side in ['top', 'bottom']:
            filename = f"{self.output_dir}/tfln_modulator_{side}_mask.gts"
            with open(filename, 'w') as f:
                f.write(f"G04 TFLN Modulator - {side.capitalize()} Solder Mask*\n")
                f.write("M02*\n")
            files.append(filename)
        return files
    
    def generate_silkscreen(self):
        """Generate silkscreen layers"""
        files = []
        for side in ['top', 'bottom']:
            filename = f"{self.output_dir}/tfln_modulator_{side}_silk.gto"
            with open(filename, 'w') as f:
                f.write(f"G04 TFLN Modulator - {side.capitalize()} Silkscreen*\n")
                f.write("M02*\n")
            files.append(filename)
        return files

    def generate_board_outline(self):
        """Generate board outline"""
        filename = f"{self.output_dir}/Antigravity_Outline.gm1"
        with open(filename, 'w') as f:
            f.write("G04 TFLN Modulator - Board Outline*\n")
            f.write("M02*\n")
        return filename
    
    def generate_all(self):
        """Generate all Gerber files and README"""
        files = []
        print("Generating 15-Layer Gerber files...")
        
        files.append(self.generate_top_copper())
        files.append(self.generate_bottom_copper())
        files.extend(self.generate_inner_layers())
        files.append(self.generate_drill_file())
        files.extend(self.generate_soldermask())
        files.extend(self.generate_silkscreen())
        files.append(self.generate_board_outline())
        
        # README
        readme_file = f"{self.output_dir}/README.txt"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write("LIGHTRAILAI CPO INTERCONNECT - 15-LAYER HYBRID STACK PCB\n")
            f.write("====================================================\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("Stackup Configuration:\n")
            f.write("  L1: Top Signal (Rogers 4350B, 50 ohm SE)\n")
            f.write("  L2: Ground (Copper)\n")
            f.write("  L3: Signal (Rogers 4350B, 85 ohm Diff)\n")
            f.write("  L4: Ground (Copper)\n")
            f.write("  L5: Low-Speed Control (FR4)\n")
            f.write("  L6: 1.8V Rail (FR4)\n")
            f.write("  L7: Digital Ground (Copper)\n")
            f.write("  L8: NCE Neuron Interconnects (FR4)\n")
            f.write("  L9: Digital Ground (Copper)\n")
            f.write("  L10: 3.3V Rail (FR4)\n")
            f.write("  L11: FPGA/Controller Fanout (FR4)\n")
            f.write("  L12: Analog Ground (Copper)\n")
            f.write("  L13: -5V / 12V (Bias/TEC) (FR4)\n")
            f.write("  L14: Ground (Copper)\n")
            f.write("  L15: Bottom Signal (FR4)\n")
        files.append(readme_file)
        
        print(f"DONE: Generated {len(files)} files in {self.output_dir}/")
        return files

if __name__ == "__main__":
    generator = GerberGenerator()
    generator.generate_all()
