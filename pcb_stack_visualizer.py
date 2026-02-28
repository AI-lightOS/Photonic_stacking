import os
import matplotlib.pyplot as plt
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
                    # simplistic parse: assuming format FSLAX36Y36
                    x = float(match.group(1)) / 1000000.0 * scale
                    y = float(match.group(2)) / 1000000.0 * scale
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
        ('tfln_modulator_top.gtl', 12, 'L1 (Top)'),
        ('tfln_modulator_l2.g2', 11, 'L2 (GND)'),
        ('tfln_modulator_l3.g3', 10, 'L3 (Signal)'),
        ('tfln_modulator_l4.g4', 9, 'L4 (GND)'),
        ('tfln_modulator_l5.g5', 8, 'L5 (Signal)'),
        ('tfln_modulator_l6.g6', 7, 'L6 (GND)'),
        ('tfln_modulator_l7.g7', 6, 'L7 (Pwr)'),
        ('tfln_modulator_l8.g8', 5, 'L8 (GND)'),
        ('tfln_modulator_l9.g9', 4, 'L9 (Pwr)'),
        ('tfln_modulator_l10.g10', 3, 'L10 (Sig)'),
        ('tfln_modulator_l11.g11', 2, 'L11 (GND)'),
        ('tfln_modulator_bottom.gbl', 1, 'L12 (Bot)'),
    ]
    
    colors = ['red', 'green', 'blue', 'green', 'purple', 'green', 'orange', 'green', 'orange', 'cyan', 'green', 'blue']
    
    for i, (filename, z_height, label) in enumerate(layers):
        filepath = os.path.join(gerber_dir, filename)
        if os.path.exists(filepath):
            lines = parser.parse(filepath)
            print(f"Layer {label}: {len(lines)} segments")
            
            # Subsample lines if too many to keep rendering fast
            if len(lines) > 500:
                lines = lines[::2]
                
            for start, end in lines:
                ax.plot([start[0], end[0]], [start[1], end[1]], [z_height, z_height], 
                        color=colors[i], alpha=0.6, linewidth=1)
                        
            # Add label at a corner
            ax.text(0, 0, z_height, label, fontsize=8)

    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Layer Stack')
    ax.set_title('12-Layer TFLN PCB Stack Visualization')
    
    # Set reasonable bounds
    ax.set_xlim(0, 80) # Approx based on generate_gerber coords
    ax.set_ylim(0, 80)
    ax.set_zlim(0, 13)
    
    plt.savefig(output_file, dpi=150)
    print(f"Saved visualization to {output_file}")

if __name__ == "__main__":
    visualize_stack()
