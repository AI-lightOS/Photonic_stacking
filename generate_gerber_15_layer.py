
import os
from datetime import datetime

class GerberGenerator15Layer:
    """Generate Gerber files for the 15-layer Photonic 3D Stack Architecture"""
    
    def __init__(self, output_dir="gerber_files_2"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # 15-Layer Stackup Definition (from Bottom to Top as per schematic numbering)
        # Layer 1 is Bottom (BGA), Layer 15 is Top (Heat Sink)
        self.layers = [
            (15, "Heat Sink / Cooling Plate", "Top cooling assembly", "g15"),
            (14, "Thermal Interface Material (TIM)", "Thermal coupling", "g14"),
            (13, "Integrated Heat Spreader (IHS)", "Heat spreading layer", "g13"),
            (12, "Top Logic Die (Compute Core)", "Active silicon logic", "g12"),
            (11, "3D Bonding Interface (Hybrid Bond)", "Face-to-face interconnect", "g11"),
            (10, "Bottom Logic Die / SRAM", "Memory and logic", "g10"),
            (9,  "Silicon Interposer Top Metal", "RDL / Interconnect", "g9"),
            (8,  "TFLN Photonic Layer (Waveguides)", "Optical routing", "g8"),
            (7,  "Through-Silicon Vias (TSV)", "Vertical interconnects", "g7"),
            (6,  "Silicon Interposer Base", "Silicon substrate", "g6"),
            (5,  "Interposer Bottom Bump (C4)", "Flip-chip bumps", "g5"),
            (4,  "Package Substrate Top Metal", "Substrate routing", "g4"),
            (3,  "Organic Package Substrate (Core)", "Package core", "g3"),
            (2,  "Package Substrate Bottom Metal", "Substrate routing", "g2"),
            (1,  "BGA Ball Grid Array", "System interface", "g1"),
        ]
        
    def generate_layer_file(self, layer_num, name, description, ext):
        """Generate a Gerber file for a specific layer"""
        filename = f"{self.output_dir}/tfln_stack_l{layer_num:02d}.{ext}"
        with open(filename, 'w') as f:
            f.write(f"G04 TFLN Photonic Stack - Layer {layer_num} ({name})*\n")
            f.write(f"G04 {description}*\n")
            f.write(f"G04 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
            f.write("%FSLAX36Y36*%\n")
            f.write("%MOIN*%\n")
            
            # Add some dummy content to simulate design data
            f.write("G01*\n")
            # Draw a box representing the layer extent
            f.write(f"G04 Layer {layer_num} Content*\n")
            f.write("D10*\n")
            f.write("X0Y0D02*\n")
            f.write("X4000000Y0D01*\n")
            f.write("X4000000Y4000000D01*\n")
            f.write("X0Y4000000D01*\n")
            f.write("X0Y0D01*\n")
            
            if "Photonic" in name:
                f.write("G04 Waveguide Structures*\n")
                f.write("X1000000Y2000000D02*\n")
                f.write("X3000000Y2000000D01*\n")
            
            if "BGA" in name or "Bump" in name:
                 f.write("G04 Pad Array*\n")
                 # Simulate some pads
                 for x in range(500000, 3500000, 1000000):
                     for y in range(500000, 3500000, 1000000):
                         f.write(f"X{x}Y{y}D03*\n")

            f.write("M02*\n")
        return filename

    def generate_drill_file(self):
        """Generate drill file for TSVs and Vias"""
        filename = f"{self.output_dir}/tfln_stack.drl"
        with open(filename, 'w') as f:
            f.write("M48\n")
            f.write("; 15-Layer TFLN Stack Drill File (TSV/Thru-Hole)\n")
            f.write("FMAT,2\n")
            f.write("METRIC,TZ\n")
            f.write("T1C0.050\n") 
            f.write("%\n")
            f.write("T1\n")
            f.write("X1500Y1500\n")
            f.write("X2500Y2500\n")
            f.write("M30\n")
        return filename

    def generate_readme(self):
        """Generate README defining the stackup"""
        filename = f"{self.output_dir}/README.txt"
        with open(filename, 'w') as f:
            f.write("TFLN PHOTONIC 3D STACK - 15-LAYER ARCHITECTURE GERBER FILES\n")
            f.write("=========================================================\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("Stackup Configuration (Top to Bottom):\n")
            f.write("-" * 60 + "\n")
            for layer_num, name, desc, ext in self.layers:
                f.write(f"Layer {layer_num:02d}: {name:<40} [{desc}]\n")
            f.write("-" * 60 + "\n")
            f.write("\nNote: These files represent the vertical integration layers of the \n")
            f.write("3D photonic computing stack, from the BGA substrate up to the heat sink.\n")
        return filename

    def generate_all(self):
        print(f"Generating 15-Layer Gerber files in {self.output_dir}...")
        generated_files = []
        
        # Generate layer files
        for layer_num, name, desc, ext in self.layers:
            generated_files.append(self.generate_layer_file(layer_num, name, desc, ext))
            
        # Generate drill file
        generated_files.append(self.generate_drill_file())
        
        # Generate README
        generated_files.append(self.generate_readme())
        
        print(f"✅ Successfully generated {len(generated_files)} files.")
        return generated_files

if __name__ == "__main__":
    generator = GerberGenerator15Layer()
    generator.generate_all()
