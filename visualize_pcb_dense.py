import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import numpy as np

def render_high_density_pcb(output_file="pcb_populated_green_dense.png"):
    # Setup Green PCB Background
    fig, ax = plt.subplots(figsize=(16, 16))
    ax.set_facecolor('#004400') 
    fig.patch.set_facecolor('#111111') 

    # --- 1. Background Pattern (Subtle Weave/Traces) ---
    # Create thousands of background traces for texture
    for _ in range(300):
        x1, y1 = random.uniform(0, 4), random.uniform(0, 4)
        length = random.uniform(0.1, 0.5)
        if random.random() > 0.5: # Horizontal
            ax.plot([x1, x1+length], [y1, y1], color='#006600', linewidth=0.5, alpha=0.3)
        else: # Vertical
            ax.plot([x1, x1], [y1, y1+length], color='#006600', linewidth=0.5, alpha=0.3)

    # --- 2. Central Processor (The "Brain") ---
    cx, cy = 2.0, 2.0
    # Substrate
    ax.add_patch(patches.Rectangle((cx-0.75, cy-0.75), 1.5, 1.5, color='#005500', ec='#00AA00', linewidth=1))
    # Die
    ax.add_patch(patches.Rectangle((cx-0.4, cy-0.4), 0.8, 0.8, color='#111111', ec='#444444', linewidth=1, zorder=20))
    # Die Label
    ax.text(cx, cy, "TFLN-AI\nCORE", color='#AAAAAA', ha='center', va='center', fontsize=10, fontweight='bold', zorder=21)
    # Corner Glue
    for dx in [-0.4, 0.4]:
        for dy in [-0.4, 0.4]:
            ax.add_patch(patches.Circle((cx+dx, cy+dy), 0.05, color='#222222', zorder=20))

    # --- 3. Memory Banks (HBM Style) ---
    # 4 HBM stacks around the die
    hbm_locs = [
        (cx-0.9, cy-0.2, 0.3, 0.4), (cx+0.6, cy-0.2, 0.3, 0.4), # Left/Right
        (cx-0.2, cy+0.6, 0.4, 0.3), (cx-0.2, cy-0.9, 0.4, 0.3)  # Top/Bottom
    ]
    for x, y, w, h in hbm_locs:
         ax.add_patch(patches.Rectangle((x, y), w, h, color='#222222', ec='#555555', zorder=15))
         # Add slight texture to HBM
         ax.add_patch(patches.Rectangle((x+0.02, y+0.02), w-0.04, h-0.04, color='#111111', zorder=16))

    # --- 4. Capacitor Arrays (Decoupling) ---
    # Creating density by surrounding the core with MLCCs
    
    def add_cap_array(start_x, start_y, count, dx=0.08, dy=0.0, label=None):
        for i in range(count):
            px, py = start_x + (i*dx), start_y + (i*dy)
            # Body
            ax.add_patch(patches.Rectangle((px, py), 0.04, 0.06, color='#8B4513', zorder=10))
            # End caps (Silver)
            ax.add_patch(patches.Rectangle((px, py), 0.04, 0.015, color='#CCCCCC', zorder=11))
            ax.add_patch(patches.Rectangle((px, py+0.045), 0.04, 0.015, color='#CCCCCC', zorder=11))

    # Top/Bottom Arrays
    add_cap_array(cx-0.8, cy+1.0, 20, dx=0.08)
    add_cap_array(cx-0.8, cy-1.1, 20, dx=0.08)
    # Left/Right Arrays (rotated visually just by switching w/h logic in mind)
    # Actually let's just use Rectangles with swapped dims for side arrays
    for i in range(15):
        px, py = cx-1.1, cy-0.6 + (i*0.08)
        ax.add_patch(patches.Rectangle((px, py), 0.06, 0.04, color='#8B4513', zorder=10)) # Rotated
        ax.add_patch(patches.Rectangle((px, py), 0.015, 0.04, color='#CCCCCC', zorder=11))
        ax.add_patch(patches.Rectangle((px+0.045, py), 0.015, 0.04, color='#CCCCCC', zorder=11))
        
    for i in range(15):
        px, py = cx+1.05, cy-0.6 + (i*0.08)
        ax.add_patch(patches.Rectangle((px, py), 0.06, 0.04, color='#8B4513', zorder=10)) # Rotated
        ax.add_patch(patches.Rectangle((px, py), 0.015, 0.04, color='#CCCCCC', zorder=11))
        ax.add_patch(patches.Rectangle((px+0.045, py), 0.015, 0.04, color='#CCCCCC', zorder=11))

    # --- 5. VRM / Power Stages (Inductors + MOSFETs) ---
    # Left side power delivery
    for i in range(8):
        y_pos = 0.5 + i*0.45
        # Inductor (Grey Box)
        ax.add_patch(patches.Rectangle((0.4, y_pos), 0.4, 0.35, color='#555555', ec='#333333', zorder=10))
        ax.text(0.6, y_pos+0.175, "R47", color='white', ha='center', va='center', fontsize=6, zorder=11)
        # MOSFET (Black small box)
        ax.add_patch(patches.Rectangle((0.15, y_pos), 0.2, 0.35, color='#111111', zorder=10))

    # --- 6. Dense Signal Routing (Bus lines) ---
    # From HBM to Core
    # Left HBM
    x_start = cx-0.6; x_end = cx-0.4
    for i in range(50):
        y = cy - 0.2 + (i * 0.4/50)
        ax.plot([x_start, x_end], [y, y], color='#44AA44', linewidth=0.5, alpha=0.6)
    
    # Right HBM
    x_start = cx+0.4; x_end = cx+0.6
    for i in range(50):
        y = cy - 0.2 + (i * 0.4/50)
        ax.plot([x_start, x_end], [y, y], color='#44AA44', linewidth=0.5, alpha=0.6)

    # --- 7. PCIe Edge Connector ---
    for i in range(50):
        x = 0.5 + i*0.06
        ax.add_patch(patches.Rectangle((x, 0.02), 0.04, 0.25, color='#FFD700', zorder=5))

    # --- 8. Miscellaneous Components scattered for "Populated" look ---
    for _ in range(100):
        x = random.uniform(0.2, 3.8)
        y = random.uniform(0.5, 3.8)
        # Avoid clear zones (CPU center)
        if 1.2 < x < 2.8 and 1.2 < y < 2.8: continue
        
        # Random small resistors
        ax.add_patch(patches.Rectangle((x, y), 0.03, 0.015, color='#111111', zorder=5))
        ax.add_patch(patches.Rectangle((x-0.005, y), 0.01, 0.015, color='#BBBBBB', zorder=6)) # pads
        ax.add_patch(patches.Rectangle((x+0.03, y), 0.01, 0.015, color='#BBBBBB', zorder=6))

    # Board Outline
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    ax.axis('off') # Hide axes completely for clean look

    plt.savefig(output_file, dpi=200, bbox_inches='tight', facecolor='#111111')
    print(f"Rendered to {output_file}")

if __name__ == "__main__":
    render_high_density_pcb()
