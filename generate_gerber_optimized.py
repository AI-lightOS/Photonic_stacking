"""
TFLN Photonic Interconnect - Optimized Gerber File Generator
Generates Cost-Optimized PCB design files (4-Layer FR-4) for JLCPCB
"""

import os
from datetime import datetime

class GerberGeneratorOptimized:
    """Generate Optimized Gerber files for TFLN photonic PCB with 4-layer stackup"""
    
    def __init__(self, output_dir="gerber_optimized"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Board specifications
        self.board_width = 106.68  # mm (standard PCIe card)
        self.board_height = 111.15  # mm
        self.layers = 4  # 4-layer PCB for Cost Optimization
        
    def to_gerber_units(self, val_mm):
        """Convert mm to Gerber units (Inches * 10^6)"""
        val_inches = val_mm / 25.4
        return int(val_inches * 1000000)

    def generate_top_copper(self):
        """Generate top copper layer (GTL)"""
        filename = f"{self.output_dir}/tfln_modulator_top.gtl"
        with open(filename, 'w') as f:
            f.write("G04 TFLN Photonic Modulator - Top Copper Layer (Signal)*\n")
            f.write("G04 TFLN RF Electrodes and High-Priority Signals*\n")
            f.write(f"G04 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
            f.write("%FSLAX36Y36*%\n")
            f.write("%MOIN*%\n")
            # RF Traces (0.25mm / 10mil for standard cost)
            f.write("G01*\n")
            f.write("D10*\n") 
            # Draw a trace from 10mm,10mm to 20mm,10mm
            x1 = self.to_gerber_units(10.0)
            y1 = self.to_gerber_units(10.0)
            x2 = self.to_gerber_units(40.0)
            y2 = self.to_gerber_units(10.0)
            f.write(f"X{x1}Y{y1}D02*\n")
            f.write(f"X{x2}Y{y2}D01*\n")
            f.write("M02*\n")
        return filename
    
    def generate_bottom_copper(self):
        """Generate bottom copper layer (GBL)"""
        filename = f"{self.output_dir}/tfln_modulator_bottom.gbl"
        with open(filename, 'w') as f:
            f.write("G04 TFLN Photonic Modulator - Bottom Copper Layer (Signal/GND)*\n")
            f.write("%FSLAX36Y36*%\n")
            f.write("%MOIN*%\n")
            f.write("M02*\n")
        return filename
    
    def generate_inner_layers(self):
        """Generate inner signal and power layers for 4-layer stackup"""
        files = []
        
        # 4-Layer Stackup Definition
        # L1: Top Signal (RF)
        # L2: Ground
        # L3: Power (+3.3V)
        # L4: Bottom Signal
        
        layer_specs = [
            (2, "Ground Plane", "g2", "Solid Ground Reference"),
            (3, "Power Plane", "g3", "Power Distribution (+3.3V)")
        ]
        
        for layer_num, desc, ext, details in layer_specs:
            filename = f"{self.output_dir}/tfln_modulator_l{layer_num}.{ext}"
            with open(filename, 'w') as f:
                f.write(f"G04 TFLN Modulator - Layer {layer_num} ({desc})*\n")
                f.write(f"G04 {details}*\n")
                f.write(f"G04 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
                f.write("%FSLAX36Y36*%\n")
                f.write("%MOIN*%\n")
                # Represent a solid plane fill
                f.write("G36*\n")
                f.write("X0Y0D02*\n")
                w = self.to_gerber_units(self.board_width)
                h = self.to_gerber_units(self.board_height)
                f.write(f"X{w}Y0D01*\n")
                f.write(f"X{w}Y{h}D01*\n")
                f.write(f"X0Y{h}D01*\n")
                f.write("X0Y0D01*\n")
                f.write("G37*\n")
                f.write("M02*\n")
            files.append(filename)
            
        return files
        
    def generate_drill_file(self):
        """Generate drill file with valid mounting holes"""
        filename = f"{self.output_dir}/tfln_modulator.drl"
        with open(filename, 'w') as f:
            f.write("M48\n")
            f.write("; 4-Layer TFLN Modulator Drill File\n")
            f.write("FMAT,2\n") 
            f.write("METRIC,TZ\n") # This header is ignored by simple parser but good practice
            
            # Tools in INCHES for parser compatibility
            # 3.2mm = 0.1260 inches
            f.write("T1C0.1260\n")  
            f.write("%\n")
            f.write("T1\n")
            
            # Coordinates in INCHES for parser compatibility
            # Board width ~ 4.2 inches, Height ~ 4.375 inches
            # 5mm = 0.197 inches
            w_inch = self.board_width / 25.4
            h_inch = self.board_height / 25.4
            margin = 5.0 / 25.4 # 5mm margin
            
            # 4 Mounting Holes in corners
            f.write(f"X{margin:.3f}Y{margin:.3f}\n")
            f.write(f"X{w_inch-margin:.3f}Y{margin:.3f}\n")
            f.write(f"X{margin:.3f}Y{h_inch-margin:.3f}\n")
            f.write(f"X{w_inch-margin:.3f}Y{h_inch-margin:.3f}\n")
            
            f.write("M30\n")
        return filename

    def generate_soldermask(self):
        """Generate solder mask layers"""
        files = []
        for side in ['top', 'bottom']:
            filename = f"{self.output_dir}/tfln_modulator_{side}_mask.gts"
            with open(filename, 'w') as f:
                f.write(f"G04 TFLN Modulator - {side.capitalize()} Solder Mask*\n")
                f.write("%FSLAX36Y36*%\n")
                f.write("%MOIN*%\n")
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
                f.write("%FSLAX36Y36*%\n")
                f.write("%MOIN*%\n")
                f.write("M02*\n")
            files.append(filename)
        return files

    def generate_board_outline(self):
        """Generate board outline"""
        filename = f"{self.output_dir}/tfln_modulator_outline.gm1"
        with open(filename, 'w') as f:
            f.write("G04 TFLN Modulator - Board Outline*\n")
            f.write("%FSLAX36Y36*%\n")
            f.write("%MOIN*%\n")
            # Draw outline
            f.write("G01*\n")
            f.write("D10*\n")
            f.write("X0Y0D02*\n")
            w = self.to_gerber_units(self.board_width)
            h = self.to_gerber_units(self.board_height)
            f.write(f"X{w}Y0D01*\n")
            f.write(f"X{w}Y{h}D01*\n")
            f.write(f"X0Y{h}D01*\n")
            f.write("X0Y0D01*\n")
            f.write("M02*\n")
        return filename
    
    def generate_all(self):
        """Generate all Gerber files and README"""
        files = []
        print("Generating Optimized 4-Layer Gerber files...")
        
        files.append(self.generate_top_copper())
        files.append(self.generate_bottom_copper())
        files.extend(self.generate_inner_layers())
        files.append(self.generate_drill_file())
        files.extend(self.generate_soldermask())
        files.extend(self.generate_silkscreen())
        files.append(self.generate_board_outline())
        
        # README
        readme_file = f"{self.output_dir}/README.txt"
        with open(readme_file, 'w') as f:
            f.write("TFLN PHOTONIC MODULATOR - COST OPTIMIZED 4-LAYER PCB\n")
            f.write("====================================================\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("Specifications for JLCPCB Quote:\n")
            f.write("  Layers: 4\n")
            f.write("  Material: FR-4 TG135-140 (Standard)\n")
            f.write("  Thickness: 1.6mm\n")
            f.write("  Copper Weight: 1oz Outer / 0.5oz Inner\n")
            f.write("  Min Trace/Space: 6/6 mil\n")
            f.write("  Min Drill: 0.3mm\n")
            f.write("\nStackup:\n")
            f.write("  L1: Top Signal (RF)\n")
            f.write("  L2: Ground Plane\n")
            f.write("  L3: Power Plane\n")
            f.write("  L4: Bottom Signal\n")
        files.append(readme_file)
        
        print(f"✅ Generated {len(files)} files in {self.output_dir}/")
        return files

if __name__ == "__main__":
    generator = GerberGeneratorOptimized()
    generator.generate_all()
