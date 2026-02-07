import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import numpy as np

def render_ultra_dense_pcb(output_file="pcb_populated_green_dense.png"):
    # Setup Dark Green/Black Professional PCB Background
    fig, ax = plt.subplots(figsize=(24, 12))
    ax.set_facecolor('#002200') # Very dark green
    fig.patch.set_facecolor('#080808') # Outer background

    # --- 1. Texture & Ground Plane Pattern ---
    # Dense grid of via-like dots for "Full Density" look
    for _ in range(2000):
        x = random.uniform(0, 40)
        y = random.uniform(0, 20)
        ax.add_patch(patches.Circle((x, y), 0.015, color='#004400', alpha=0.5, zorder=1))

    # --- 2. Central AI Computing Core ---
    cx, cy = 20, 10
    # Large BGA Substrate
    ax.add_patch(patches.Rectangle((cx-4, cy-4), 8, 8, color='#003300', ec='#00AA00', linewidth=1.5, zorder=5))
    # Die (Silicon)
    ax.add_patch(patches.Rectangle((cx-2.5, cy-2.5), 5, 5, color='#111111', ec='#555555', linewidth=1, zorder=20))
    # Label
    ax.text(cx, cy, "TFLN-AI\nLIGHT RAIL", color='#FFFFFF', ha='center', va='center', fontsize=14, fontweight='bold', zorder=21)
    
    # --- 3. GDDR6X Memory Surround (12 chips) ---
    mem_color = '#111111'
    mem_ec = '#444444'
    mem_locs = []
    for i in range(4): mem_locs.append((cx-6, cy-3 + i*2)) # Left
    for i in range(4): mem_locs.append((cx+4.5, cy-3 + i*2)) # Right
    for i in range(4): mem_locs.append((cx-3 + i*2, cy-6)) # Bottom

    for x, y in mem_locs:
        ax.add_patch(patches.Rectangle((x, y), 1.5, 1.5, color=mem_color, ec=mem_ec, zorder=15))
        # Internal traces to GPU
        ax.plot([x+0.75, cx], [y+0.75, cy], color='#FFD700', linewidth=0.2, alpha=0.15, zorder=10)

    # --- 4. 20-Phase VRM (High Density) ---
    vrm_x_start = 2
    for i in range(20):
        # Inductor (R47)
        bx = vrm_x_start + i*0.85
        by = 16
        ax.add_patch(patches.Rectangle((bx, by), 0.6, 1.8, color='#444444', ec='#222222', zorder=10))
        ax.text(bx+0.3, by+0.9, "R47", color='white', ha='center', va='center', fontsize=6, rotation=90, zorder=11)
        # PowerStage (MOSFET)
        ax.add_patch(patches.Rectangle((bx, by-1.2), 0.6, 0.8, color='#000000', zorder=10))

    # --- 5. Massive MLCC Decoupling (Full Density) ---
    def add_mlcc_block(x_range, y_range, density=200):
        for _ in range(density):
            px = random.uniform(x_range[0], x_range[1])
            py = random.uniform(y_range[0], y_range[1])
            # Avoid core/mem directly for "populated" look
            ax.add_patch(patches.Rectangle((px, py), 0.1, 0.06, color='#8B4513', zorder=12)) # MLCC Body
            ax.add_patch(patches.Rectangle((px, py), 0.02, 0.06, color='#CCCCCC', zorder=13)) # Caps
            ax.add_patch(patches.Rectangle((px+0.08, py), 0.02, 0.06, color='#CCCCCC', zorder=13))

    # Decoupling around GPU
    add_mlcc_block((15, 25), (5, 15), 300)
    # Decoupling around VRM
    add_mlcc_block((2, 19), (14, 15), 100)
    # Scattered everywhere else
    add_mlcc_block((0.5, 39.5), (0.5, 19.5), 500)

    # --- 6. Photonic / Fiber Interconnects (As per uploaded image) ---
    # Silver cooling/optical blocks on the right
    ax.add_patch(patches.Rectangle((32, 4), 6, 12, color='#CCCCCC', ec='#AAAAAA', zorder=30))
    ax.text(35, 10, "OPTICAL\nCOUPLER\nARRAY", color='#333333', ha='center', va='center', fontsize=12, fontweight='bold', zorder=31)
    
    # "Fibers" coming out
    for i in range(16):
        fy = 5 + i * 0.6
        ax.plot([38, 41], [fy, fy], color='#FFFFFF', linewidth=1.5, alpha=0.8, zorder=29)
        ax.add_patch(patches.Circle((41, fy), 0.1, color='#FF4444', zorder=30)) # Laser emitters?

    # --- 7. PCIe Gen5 Edge Connector ---
    for i in range(164): # Standard PCIe-x16 pin count ish
        px = 10 + i * 0.12
        ax.add_patch(patches.Rectangle((px, 0.1), 0.08, 1.2, color='#FFD700', zorder=5))

    # Board Limits
    ax.set_xlim(0, 42)
    ax.set_ylim(0, 20)
    ax.axis('off')

    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='#080808')
    print(f"Rendered High-Density AI Accelerator Class PCB to {output_file}")

if __name__ == "__main__":
    render_ultra_dense_pcb()
