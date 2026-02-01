import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection
import re

class RealisticGerberParser:
    def __init__(self):
        self.elements = []
        self.apertures = {}
        
    def parse(self, filepath):
        self.elements = []
        self.apertures = {}
        scale = 1.0
        
        with open(filepath, 'r') as f:
            content = f.read()
            if '%MOIN*%' in content:
                scale = 1.0 
            
            # Parse Apertures
            aperture_pattern = r'%ADD(\d+)([CR]),([0-9.]+)(?:X([0-9.]+))?\*%'
            for match in re.finditer(aperture_pattern, content):
                code = int(match.group(1))
                shape = match.group(2)
                size1 = float(match.group(3))
                size2 = float(match.group(4)) if match.group(4) else size1
                self.apertures[code] = (shape, (size1, size2))
            
            # Parse Commands
            current_x, current_y = 0.0, 0.0
            current_aperture = None
            
            lines = content.splitlines()
            for line in lines:
                line = line.strip()
                if line.startswith('D') and line.endswith('*') and len(line) > 3:
                     try:
                        code = int(line[1:-1])
                        if code >= 10: current_aperture = code
                     except: pass

                match = re.search(r'X(\d+)Y(\d+)D(\d+)', line)
                if match:
                    x = float(match.group(1)) / 1000000.0
                    y = float(match.group(2)) / 1000000.0
                    d_code = match.group(3)
                    
                    if d_code == '01':
                        if current_aperture in self.apertures:
                             width = self.apertures[current_aperture][1][0]
                             self.elements.append(('line', (current_x, current_y), (x, y), width))
                    elif d_code == '03':
                        if current_aperture in self.apertures:
                            shape, size = self.apertures[current_aperture]
                            self.elements.append(('flash', shape, (x, y), size))
                            
                    current_x, current_y = x, y
        return self.elements

def render_populated_green_pcb(gerber_dir="gerber_files", output_file="pcb_populated_green.png"):
    parser = RealisticGerberParser()
    
    # 1. Setup Green PCB Background
    fig, ax = plt.subplots(figsize=(12, 12))
    # Standard PCB Green: #006600, usually a bit translucent over darker substrate
    ax.set_facecolor('#004400') 
    fig.patch.set_facecolor('#111111') # Dark background for the image file
    
    # 2. Render Layers
    # Inner layers (lighter green veins)
    inner_layers = ['tfln_modulator_l2.g2', 'tfln_modulator_l3.g3']
    for lname in inner_layers:
        filepath = os.path.join(gerber_dir, lname)
        if os.path.exists(filepath):
            elements = parser.parse(filepath)
            for elem in elements:
                if elem[0] == 'line':
                    ax.plot([elem[1][0], elem[2][0]], [elem[1][1], elem[2][1]], 
                            color='#00AA00', linewidth=elem[3]*40, alpha=0.3)

    # Top Copper (Bright Green/Gold for pads)
    top_file = os.path.join(gerber_dir, 'tfln_modulator_top.gtl')
    if os.path.exists(top_file):
        elements = parser.parse(top_file)
        for elem in elements:
            if elem[0] == 'line':
                # Traces under soldermask look lighter green
                ax.plot([elem[1][0], elem[2][0]], [elem[1][1], elem[2][1]], 
                        color='#33DD33', linewidth=elem[3]*72, alpha=0.8)
            elif elem[0] == 'flash':
                # Pads are Gold (ENIG)
                shape, center, size = elem[1], elem[2], elem[3]
                if shape == 'C':
                    ax.add_patch(patches.Circle(center, size[0]/2, color='#FFD700', alpha=1.0))
                elif shape == 'R':
                    w, h = size
                    xy = (center[0] - w/2, center[1] - h/2)
                    ax.add_patch(patches.Rectangle(xy, w, h, color='#FFD700', alpha=1.0))

    # 3. Render Components (Populated)
    # Hardcoded visualization of components based on known design locations
    # (In a real pipeline, this would come from a centroid/pick-and-place file)
    
    components = [
        # Chip U1 (Center) - Black package
        {'shape': 'rect', 'xy': (1.0, 1.0), 'w': 2.0, 'h': 1.0, 'color': '#111111', 'label': 'TFLN MZM\nPROCESSOR'},
        # Connectors
        {'shape': 'rect', 'xy': (0.2, 0.2), 'w': 0.6, 'h': 0.6, 'color': '#CCCCCC', 'label': 'PCIe'}, # Simulated
        {'shape': 'rect', 'xy': (3.2, 3.2), 'w': 0.6, 'h': 0.6, 'color': '#CCCCCC', 'label': 'OPT'},
        # Decoupling Caps (Small jagged browns)
        {'shape': 'rect', 'xy': (1.1, 2.1), 'w': 0.1, 'h': 0.05, 'color': '#8B4513'},
        {'shape': 'rect', 'xy': (1.2, 2.1), 'w': 0.1, 'h': 0.05, 'color': '#8B4513'},
        {'shape': 'rect', 'xy': (1.3, 2.1), 'w': 0.1, 'h': 0.05, 'color': '#8B4513'},
    ]
    
    for comp in components:
        if comp['shape'] == 'rect':
            rect = patches.Rectangle(comp['xy'], comp['w'], comp['h'], 
                                   color=comp['color'], ec='black', linewidth=1, zorder=10)
            ax.add_patch(rect)
            if 'label' in comp:
                cx = comp['xy'][0] + comp['w']/2
                cy = comp['xy'][1] + comp['h']/2
                ax.text(cx, cy, comp['label'], color='white', ha='center', va='center', 
                        fontsize=8, fontweight='bold', zorder=11)

    # Board Outline (Cutout)
    # Simple rounded rect approximation for the substrate shape
    # We already painted the background, but let's assume the axes limits define the view

    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(-0.2, 4.2)
    ax.set_ylim(-0.2, 4.2)
    
    # Remove spines
    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.savefig(output_file, dpi=150, bbox_inches='tight', facecolor='#111111')
    print(f"Rendered to {output_file}")

if __name__ == "__main__":
    render_populated_green_pcb()
