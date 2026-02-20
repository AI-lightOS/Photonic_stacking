import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection
import re

class RealisticGerberParser:
    def __init__(self):
        self.elements = [] # list of (type, shape, coords, size)
        self.apertures = {} # code -> (shape, size)
        
    def parse(self, filepath):
        self.elements = []
        self.apertures = {}
        scale = 1.0 # default
        
        with open(filepath, 'r') as f:
            content = f.read()
            
            # Check units
            if '%MOIN*%' in content:
                scale = 1.0 # We'll work in inches since matplotlib doesn't care about units, but inches keeps numbers small
            
            # Parse Apertures
            # %ADD10C,0.010*% -> Circle diameter 0.010
            # %ADD12R,0.050X0.050*% -> Rect 0.050x0.050
            aperture_pattern = r'%ADD(\d+)([CR]),([0-9.]+)(?:X([0-9.]+))?\*%'
            for match in re.finditer(aperture_pattern, content):
                code = int(match.group(1))
                shape = match.group(2)
                size1 = float(match.group(3))
                size2 = float(match.group(4)) if match.group(4) else size1
                self.apertures[code] = (shape, (size1, size2))
            
            # Parse Commands
            current_x, current_y = 0.0, 0.0
            current_d = None
            current_aperture = None
            
            lines = content.splitlines()
            for line in lines:
                line = line.strip()
                
                # Aperture Selection D10-D99
                if line.startswith('D') and line.endswith('*') and len(line) > 3:
                     # e.g. D11*
                     try:
                        code = int(line[1:-1])
                        if code >= 10:
                            current_aperture = code
                     except: pass

                # Coords
                # X...Y...D...
                match = re.search(r'X(\d+)Y(\d+)D(\d+)', line)
                if match:
                    # Parse coords (assuming 3.6 format from generator: 1000000 = 1.0)
                    x = float(match.group(1)) / 1000000.0
                    y = float(match.group(2)) / 1000000.0
                    d_code = match.group(3)
                    
                    if d_code == '01': # Line to
                        if current_aperture in self.apertures:
                             width = self.apertures[current_aperture][1][0]
                             self.elements.append(('line', (current_x, current_y), (x, y), width))
                    elif d_code == '02': # Move to
                        pass
                    elif d_code == '03': # Flash
                        if current_aperture in self.apertures:
                            shape, size = self.apertures[current_aperture]
                            self.elements.append(('flash', shape, (x, y), size))
                            
                    current_x, current_y = x, y

        return self.elements

def render_realistic(gerber_dir="gerber_files", output_file="pcb_realistic_render.png"):
    parser = RealisticGerberParser()
    
    # Setup plot - Dark Background
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_facecolor('#050505') # Very dark grey/black
    fig.patch.set_facecolor('#050505')
    
    # Defined Layers to Render
    # Order matters: Bottom -> Top
    layers_to_render = [
        {'file': 'tfln_modulator_bottom.gbl', 'color': '#003300', 'alpha': 0.8}, # Bottom (Dark Green)
        {'file': 'tfln_modulator_l2.g2', 'color': '#004400', 'alpha': 0.4},      # Inner Plane (Faint Green)
        {'file': 'tfln_modulator_top.gtl', 'color': '#cc0000', 'alpha': 0.9, 'pad_color': '#FFD700'},    # Top (Red), Pads (Gold)
    ]
    
    for layer in layers_to_render:
        filepath = os.path.join(gerber_dir, layer['file'])
        if not os.path.exists(filepath):
            continue
            
        elements = parser.parse(filepath)
        
        lines = []
        pads = []
        
        pad_color = layer.get('pad_color', layer['color'])
        
        for elem in elements:
            if elem[0] == 'line':
                # Line segment
                start, end, width = elem[1], elem[2], elem[3]
                # Matplotlib plot is easiest for lines, but can use patches for thick lines if needed. 
                # For high fidelity, simple plot with linewidth is okay but strictly ends are rounded in plot vs square/round in gerber.
                # Let's use simple plot for traces
                ax.plot([start[0], end[0]], [start[1], end[1]], 
                        color=layer['color'], linewidth=width*72, # linewidth in points, approx conversion 
                        alpha=layer['alpha'], solid_capstyle='round')
                        
            elif elem[0] == 'flash':
                shape, center, size = elem[1], elem[2], elem[3]
                if shape == 'C':
                    # Circle
                    radius = size[0] / 2
                    circle = patches.Circle(center, radius, color=pad_color, alpha=1.0)
                    ax.add_patch(circle)
                elif shape == 'R':
                    # Rect (centered)
                    w, h = size
                    xy = (center[0] - w/2, center[1] - h/2)
                    rect = patches.Rectangle(xy, w, h, color=pad_color, alpha=1.0)
                    ax.add_patch(rect)

    # Board Outline (Yellow-ish)
    outline_file = os.path.join(gerber_dir, "tfln_modulator_outline.gm1")
    if os.path.exists(outline_file):
         # Just simplistic rendering of outline if it has lines
         pass 

    ax.axis('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Limits - hardcoded based on known board size (roughly 0-4 inches)
    ax.set_xlim(-0.2, 4.2)
    ax.set_ylim(-0.2, 4.5)
    
    # Remove spines
    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.savefig(output_file, dpi=150, bbox_inches='tight', facecolor='#050505')
    print(f"Rendered to {output_file}")

if __name__ == "__main__":
    render_realistic()
