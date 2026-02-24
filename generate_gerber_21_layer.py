import os
from datetime import datetime

class GerberGenerator21Layer:
    """Generate Gerber files for the 21-layer Advanced Photonic 3D Stack Architecture"""
    
    def __init__(self, output_dir="gerber_21_layer"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # 21-Layer Stackup Definition
        self.layers = [
            (21, "Active Liquid Cooling Manifold", "cooling", "g21"),
            (20, "Vapor Chamber & TIM", "cooling", "g20"),
            (19, "Top AI Compute Core (L3)", "logic", "g19"),
            (18, "DSP & Control Logic (L2)", "logic", "g18"),
            (17, "SRAM / HBM Memory Layer (L1)", "memory", "g17"),
            (16, "Hybrid Bonding Interface", "bond", "g16"),
            (15, "Photonic Routing - Multiplexers", "photonics", "g15"),
            (14, "Photonic Routing - Ring Resonators", "photonics", "g14"),
            (13, "Photonic Routing - TFLN Modulators", "photonics", "g13"),
            (12, "Photonic Routing - Passive & I/O", "photonics", "g12"),
            (11, "Silicon Interposer Top Metal (RDL)", "interposer", "g11"),
            (10, "High-Aspect Ratio TSV Core", "interposer", "g10"),
            (9,  "Silicon Interposer Base Metal (RDL)", "interposer", "g9"),
            (8,  "Ultra-Shielded RF Signal (TX)", "rf", "g8"),
            (7,  "RF Ground Plane (TX Shield)", "gnd", "g7"),
            (6,  "Ultra-Shielded RF Signal (RX)", "rf", "g6"),
            (5,  "RF Ground Plane (RX Shield)", "gnd", "g5"),
            (4,  "Power Delivery Network (PDN) L2", "pwr", "g4"),
            (3,  "Integrated Decoupling Capacitors", "passive", "g3"),
            (2,  "Power Delivery Network (PDN) L1", "pwr", "g2"),
            (1,  "Advanced BGA System Interface", "base", "g1"),
        ]
        
    def generate_layer_file(self, layer_num, name, category, ext):
        """Generate a Gerber file with realistic patterns for a specific layer"""
        filename = f"{self.output_dir}/advanced_stack_l{layer_num:02d}.{ext}"
        with open(filename, 'w') as f:
            f.write(f"G04 Advanced 21-Layer Photonic Stack - Layer {layer_num} ({name})*\n")
            f.write(f"G04 Category: {category}*\n")
            f.write(f"G04 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
            f.write("%FSLAX36Y36*%\n")
            f.write("%MOIN*%\n")
            
            # Aperture Definitions
            f.write("%ADD10C,0.010*%G04 Standard Trace-0.010in*\n")
            f.write("%ADD11C,0.050*%G04 BGA Pad-0.050in*\n")
            f.write("%ADD12C,0.005*%G04 Fine Photonic-0.005in*\n")
            f.write("%ADD13C,0.080*%G04 Thermal Via-0.080in*\n")
            
            f.write("G01*\n")
            
            # Board Outline (on every layer for reference)
            f.write("D10*\n")
            f.write("X0Y0D02*\n")
            f.write("X4000000Y0D01*\n")
            f.write("X4000000Y4000000D01*\n")
            f.write("X0Y4000000D01*\n")
            f.write("X0Y0D01*\n")

            if category == "base":
                self._generate_bga_grid(f)
            elif category == "photonics":
                self._generate_photonic_patterns(f, layer_num)
            elif category == "logic" or category == "memory":
                self._generate_logic_interconnects(f)
            elif category == "cooling":
                self._generate_cooling_channels(f)
            elif category == "rf":
                self._generate_rf_transmission_lines(f)
            else:
                self._generate_generic_ground_plane(f)

            f.write("M02*\n")
        return filename

    def _generate_bga_grid(self, f):
        """Generate a BGA ball grid array pattern"""
        f.write("G04 BGA Grid Generation*\n")
        f.write("D11*\n") # 50mil pads
        for x in range(500000, 3600000, 200000):
            for y in range(500000, 3600000, 200000):
                f.write(f"X{x}Y{y}D03*\n")

    def _generate_photonic_patterns(self, f, layer_num):
        """Generate realistic photonic patterns like waveguides and rings"""
        f.write("G04 Photonic Waveguide and Resonator Patterns*\n")
        f.write("D12*\n") # Fine 5mil traces
        
        # Draw some "rings" using segmented lines (approximating circles)
        import math
        for center_y in range(1000000, 3500000, 800000):
            center_x = 2000000
            radius = 300000
            # Draw ring
            f.write(f"G04 Ring Resonator at {center_x},{center_y}*\n")
            for angle in range(0, 370, 10):
                rad = math.radians(angle)
                x = int(center_x + radius * math.cos(rad))
                y = int(center_y + radius * math.sin(rad))
                f.write(f"X{x}Y{y}{'D02' if angle == 0 else 'D01'}*\n")
        
        # Bus waveguides
        f.write("G04 Bus Waveguides*\n")
        f.write("X500000Y500000D02*\n")
        f.write("X3500000Y500000D01*\n")
        f.write("X500000Y3500000D02*\n")
        f.write("X3500000Y3500000D01*\n")

    def _generate_cooling_channels(self, f):
        """Generate microfluidic cooling channel outlines"""
        f.write("G04 Microfluidic Cooling Channels*\n")
        f.write("D13*\n") # 80mil channels
        for x in range(1000000, 3500000, 1000000):
            f.write(f"X{x}Y500000D02*\n")
            f.write(f"X{x}Y3500000D01*\n")
            # Connect headers
            if x < 3000000:
                f.write(f"X{x}Y3500000D02*\n")
                f.write(f"X{x+1000000}Y3500000D01*\n")

    def _generate_logic_interconnects(self, f):
        """Generate high-density logic breakout patterns"""
        f.write("G04 High Density Interconnects*\n")
        f.write("D10*\n")
        for i in range(20):
            offset = 200000 + i * 150000
            f.write(f"X{offset}Y500000D02*\n")
            f.write(f"X{offset}Y3500000D01*\n")

    def _generate_rf_transmission_lines(self, f):
        """Generate differential RF transmission lines"""
        f.write("G04 RF Differential Pairs*\n")
        f.write("D10*\n")
        # Pair 1
        f.write("X1000000Y1000000D02*\n")
        f.write("X3000000Y1000000D01*\n")
        f.write("X1000000Y1050000D02*\n")
        f.write("X3000000Y1050000D01*\n")
        # Pair 2
        f.write("X1000000Y3000000D02*\n")
        f.write("X3000000Y3000000D01*\n")
        f.write("X1000000Y3050000D02*\n")
        f.write("X3000000Y3050000D01*\n")

    def _generate_generic_ground_plane(self, f):
        """Generate a cross-hatched ground plane"""
        f.write("G04 Cross-Hatched Ground Plane*\n")
        f.write("D10*\n")
        for i in range(0, 4000000, 500000):
            f.write(f"X{i}Y0D02*\n")
            f.write(f"X{i}Y4000000D01*\n")
            f.write(f"X0Y{i}D02*\n")
            f.write(f"X4000000Y{i}D01*\n")

    def generate_all(self):
        print(f"Generating 21-Layer Advanced Gerber files in {self.output_dir}...")
        generated_files = []
        for layer_num, name, category, ext in self.layers:
            generated_files.append(self.generate_layer_file(layer_num, name, category, ext))
            
        # Also generate a drill file
        drill_file = self._generate_drill_file()
        generated_files.append(drill_file)
        
        # README
        readme_path = os.path.join(self.output_dir, "README.txt")
        with open(readme_path, 'w') as f:
            f.write("ADVANCED 21-LAYER PHOTONIC ARCHITECTURE\n")
            f.write("========================================\n")
            for layer_num, name, category, ext in reversed(self.layers):
                f.write(f"L{layer_num:02d}: {name} ({category})\n")
        generated_files.append(readme_path)
        
        print(f"✅ Successfully generated {len(generated_files)} files.")
        return generated_files

    def _generate_drill_file(self):
        """Generate an Excellon drill file for TSVs and Vias"""
        filename = f"{self.output_dir}/advanced_stack.drl"
        with open(filename, 'w') as f:
            f.write("M48\n")
            f.write("METRIC,LZ\n")
            f.write("T1C0.2\n") # 0.2mm vias
            f.write("T2C0.5\n") # 0.5mm BGA interface
            f.write("%\n")
            f.write("G05\n")
            f.write("T1\n")
            for x in range(1000, 3900, 500):
                for y in range(1000, 3900, 500):
                    f.write(f"X{x}Y{y}\n")
            f.write("T2\n")
            for x in range(500, 3600, 400):
                f.write(f"X{x}Y500\n")
            f.write("M30\n")
        return filename

if __name__ == "__main__":
    generator = GerberGenerator21Layer()
    generator.generate_all()
