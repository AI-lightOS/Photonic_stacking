import os
from datetime import datetime

class GerberGeneratorOrchestrated:
    """Generate Gerber files for the 18-layer Orchestrated Photonic 3D Stack Architecture"""
    
    def __init__(self, output_dir="gerber_orchestrated"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # 18-Layer Stackup Definition (from Bottom to Top)
        self.layers = [
            (18, "Micro-Fluidic Cooling Plate", "Advanced thermal dissipation", "g18"),
            (17, "Thermal Interface Material (TIM)", "Thermal coupling", "g17"),
            (16, "Top Logic Sub-Die (Control/AI)", "High-level orchestration logic", "g16"),
            (15, "Bottom Logic Sub-Die (DSP/SRAM)", "Signal processing & memory", "g15"),
            (14, "Hybrid Bonding Interface", "Logic to Photonic face-to-face", "g14"),
            (13, "Photonic Routing (Ring Resonators)", "Dense wavelength division multiplexing", "g13"),
            (12, "Photonic Routing (TFLN Modulators)", "High-speed electro-optic modulation", "g12"),
            (11, "Photonic Routing (Passive WG)", "Interconnects and splitters", "g11"),
            (10, "Silicon Interposer Top Metal", "RDL for photonics to TSVs", "g10"),
            (9,  "Dense TSV Interposer Core", "Vertical via arrays", "g9"),
            (8,  "Silicon Interposer Base Metal", "RDL spreading for base substrate", "g8"),
            (7,  "High-Speed RF Signal Layer 1", "Modulator RF drivers", "g7"),
            (6,  "RF Ground Plane 1", "Impedance control", "g6"),
            (5,  "High-Speed RF Signal Layer 2", "Secondary RF routing", "g5"),
            (4,  "RF Ground Plane 2", "Shielding and return paths", "g4"),
            (3,  "Power Delivery Network (PDN) Top", "Clean power rails", "g3"),
            (2,  "Power Delivery Network (PDN) Bot", "Power and ground", "g2"),
            (1,  "BGA System Interface", "External connection", "g1"),
        ]
        
    def generate_layer_file(self, layer_num, name, description, ext):
        """Generate a Gerber file for a specific layer"""
        filename = f"{self.output_dir}/orchestrated_stack_l{layer_num:02d}.{ext}"
        with open(filename, 'w') as f:
            f.write(f"G04 Orchestrated Photonic Stack - Layer {layer_num} ({name})*\n")
            f.write(f"G04 {description}*\n")
            f.write(f"G04 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
            f.write("%FSLAX36Y36*%\n")
            f.write("%MOIN*%\n")
            
            f.write("G01*\n")
            f.write(f"G04 Layer {layer_num} Elements*\n")
            f.write("D10*\n")
            f.write("X0Y0D02*\n")
            f.write("X5000000Y0D01*\n")
            f.write("X5000000Y5000000D01*\n")
            f.write("X0Y5000000D01*\n")
            f.write("X0Y0D01*\n")
            
            if "Photonic" in name:
                f.write("G04 Waveguide / Resonator Structures*\n")
                f.write("X1000000Y2000000D02*\n")
                f.write("X4000000Y2000000D01*\n")
                f.write("X4000000Y3000000D01*\n")
                f.write("X1000000Y3000000D01*\n")
                
            if "RF" in name:
                f.write("G04 High Speed RF Transmission Lines*\n")
                f.write("X500000Y500000D02*\n")
                f.write("X4500000Y4500000D01*\n")
                
            if "BGA" in name or "Power" in name:
                 f.write("G04 Array Pads*\n")
                 for x in range(500000, 4500000, 1000000):
                     for y in range(500000, 4500000, 1000000):
                         f.write(f"X{x}Y{y}D03*\n")

            f.write("M02*\n")
        return filename

    def generate_drill_file(self):
        """Generate drill file for TSVs and Vias"""
        filename = f"{self.output_dir}/orchestrated_stack.drl"
        with open(filename, 'w') as f:
            f.write("M48\n")
            f.write("; 18-Layer Orchestrated Stack Drill File\n")
            f.write("FMAT,2\n")
            f.write("METRIC,TZ\n")
            f.write("T1C0.030\n") 
            f.write("%\n")
            f.write("T1\n")
            for x in range(1500, 3500, 500):
                f.write(f"X{x}Y{x}\n")
            f.write("M30\n")
        return filename

    def generate_readme(self):
        """Generate README defining the stackup"""
        filename = f"{self.output_dir}/README.txt"
        with open(filename, 'w') as f:
            f.write("ORCHESTRATED PHOTONIC MULTI-STACK - 18-LAYER ARCHITECTURE\n")
            f.write("=========================================================\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("Stackup Configuration (Top to Bottom):\n")
            f.write("-" * 65 + "\n")
            for layer_num, name, desc, ext in reversed(self.layers):
                f.write(f"Layer {layer_num:02d}: {name:<35} [{desc}]\n")
            f.write("-" * 65 + "\n")
        return filename

    def generate_all(self):
        print(f"Generating 18-Layer Orchestrated Gerber files in {self.output_dir}...")
        generated_files = []
        for layer_num, name, desc, ext in self.layers:
            generated_files.append(self.generate_layer_file(layer_num, name, desc, ext))
        generated_files.append(self.generate_drill_file())
        generated_files.append(self.generate_readme())
        print(f"✅ Successfully generated {len(generated_files)} files.")
        return generated_files

if __name__ == "__main__":
    generator = GerberGeneratorOrchestrated()
    generator.generate_all()
