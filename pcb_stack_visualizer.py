import os
import matplotlib.pyplot as plt
plt.switch_backend('Agg')
from mpl_toolkits.mplot3d import Axes3D
import glob
import re

# Use gerber_viewer logic partially, but simplified for 3D
class SimpleGerberParser:
    def __init__(self):
        self.lines = []
        
    def parse(self, filepath):
        self.lines = []
        scale = 1.0
        with open(filepath, 'r') as f:
            content = f.read()
            if '%MOIN*%' in content:
                scale = 25.4 # inches to mm
            
            current_x, current_y = 0.0, 0.0
            
            # Simple line parser
            for line in content.splitlines():
                line = line.strip()
                match = re.search(r'X(\d+)Y(\d+)D(\d+)', line)
                if match:
                    # simplistic parse: assuming format FSLAX36Y36 for mm or FSLAX25Y25 for inch
                    # We divide by 1e6 for mm (3.6) and usually 1e5 for inch (2.5)
                    divisor = 1000000.0
                    if '%MOIN*%' in content:
                        divisor = 100000.0
                    
                    x = float(match.group(1)) / divisor * scale
                    y = float(match.group(2)) / divisor * scale
                    d = match.group(3)
                    
                    if d == '01': # Draw
                        self.lines.append(((current_x, current_y), (x, y)))
                    
                    current_x, current_y = x, y
        return self.lines

def visualize_stack(gerber_dir="gerber_files", output_file="pcb_stack_3d.png"):
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    parser = SimpleGerberParser()
    
    # Layer definitions and Z-heights (exaggerated for visibility)
    # Mapping based on generate_gerber.py
    # L1 (Top) is highest Z.
    
    layers = [
        ('LightRailAI_L1_Top_Cu.gtl', 15, 'L1 (Top, Rogers)'),
        ('LightRailAI_L2_Ground.g2', 14, 'L2 (GND)'),
        ('LightRailAI_L3_Signal.g3', 13, 'L3 (SerDes, Rogers)'),
        ('LightRailAI_L4_Ground.g4', 12, 'L4 (GND)'),
        ('LightRailAI_L5_Signal.g5', 11, 'L5 (Ctrl, FR4)'),
        ('LightRailAI_L6_Power.g6', 10, 'L6 (1.8V, FR4)'),
        ('LightRailAI_L7_Ground.g7', 9, 'L7 (GND)'),
        ('LightRailAI_L8_Signal.g8', 8, 'L8 (NCE, FR4)'),
        ('LightRailAI_L9_Ground.g9', 7, 'L9 (GND)'),
        ('LightRailAI_L10_Power.g10', 6, 'L10 (3.3V, FR4)'),
        ('LightRailAI_L11_Signal.g11', 5, 'L11 (FPGA, FR4)'),
        ('LightRailAI_L12_Ground.g12', 4, 'L12 (GND)'),
        ('LightRailAI_L13_Power.g13', 3, 'L13 (Bias, FR4)'),
        ('LightRailAI_L14_Ground.g14', 2, 'L14 (GND)'),
        ('LightRailAI_L15_Bottom_Cu.gbl', 1, 'L15 (Bot, FR4)'),
        ('vlsi_photonics.gbr', 15.5, 'VLSI Photonics (Top Layer)'),
        ('vlsi_fpga_logic.gbr', 15.6, 'VLSI FPGA Logic'),
    ]
    
    colors = ['red', 'green', 'blue', 'green', 'purple', 'green', 'orange', 'green', 'gray', 'orange', 'cyan', 'green', 'yellow', 'green', 'blue', 'pink', 'magenta']
    
    for i, (filename, z_height, label) in enumerate(layers):
        filepath = os.path.join(gerber_dir, filename)
        if os.path.exists(filepath):
            print(f"Processing Layer {label} ({filename})...")
            lines = parser.parse(filepath)
            print(f"  -> {len(lines)} segments found.")
            
            # Subsample lines if too many to keep rendering fast
            if len(lines) > 500:
                lines = lines[::2]
                
            for start, end in lines:
                ax.plot([start[0], end[0]], [start[1], end[1]], [z_height, z_height], 
                        color=colors[i % len(colors)], alpha=0.6, linewidth=1)
                        
            # Add label at a corner
            ax.text(0, 0, z_height, label, fontsize=8)

    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Layer Stack')
    ax.set_title('Aligned 15-Layer TFLN PCB Stack Visualization')
    
    # Set reasonable bounds
    ax.set_xlim(0, 80) # Approx based on generate_gerber coords
    ax.set_ylim(0, 80)
    ax.set_zlim(0, 16)
    
    plt.savefig(output_file, dpi=150)
    print(f"Saved visualization to {output_file}")

if __name__ == "__main__":
    visualize_stack()
