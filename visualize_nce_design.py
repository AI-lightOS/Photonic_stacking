import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon, PathPatch
from matplotlib.path import Path
import numpy as np

def render_nce_module(output_file=r"C:\Users\bolao\Downloads\LightRail_NCE_1_Render.png"):
    """
    Render the High-Fidelity LightRail NCE-1 PCIe Module.
    """
    # 1. Setup Canvas
    fig, ax = plt.subplots(figsize=(20, 12))
    ax.set_facecolor('#0a0a0a') # Deep black background
    fig.patch.set_facecolor('#0a0a0a')

    # --- Dimensions (mm) ---
    # Standard PCIe Height: ~111mm. Length: ~312mm (Full Length)
    # This design is "Wafer Scale", so it dominates the board.
    pcb_w, pcb_h = 300, 111 
    center_x, center_y = pcb_w / 2, pcb_h / 2

    # --- 2. Thermal Alignment Frame (The "Gunmetal" Carrier) ---
    # Sits behind everything.
    frame_w, frame_h = pcb_w + 10, pcb_h + 10
    frame = FancyBboxPatch((center_x - frame_w/2, center_y - frame_h/2), 
                          frame_w, frame_h,
                          boxstyle="round,pad=0,rounding_size=4",
                          facecolor='#2c3e50', edgecolor='#34495e', linewidth=2, alpha=1.0)
    ax.add_patch(frame)
    
    # Add "Precision Grooves" texture to frame
    for i in range(0, int(frame_w), 10):
        groove_x = center_x - frame_w/2 + i
        ax.plot([groove_x, groove_x], [center_y - frame_h/2, center_y + frame_h/2],
               color='#34495e', linewidth=0.5, alpha=0.3)

    # --- 3. Unified Memory Complex (SUBSTRATE) ---
    # Two green strips flanking the center
    sub_h = 30
    sub_w = 220
    
    # Top Substrate
    sub_top_y = center_y + 15
    rect_sub_top = Rectangle((center_x - sub_w/2, sub_top_y), sub_w, sub_h,
                            facecolor='#1e8449', edgecolor='#145a32', linewidth=1) # Dark PCB Green
    ax.add_patch(rect_sub_top)
    
    # Bottom Substrate
    sub_bot_y = center_y - 15 - sub_h
    rect_sub_bot = Rectangle((center_x - sub_w/2, sub_bot_y), sub_w, sub_h,
                            facecolor='#1e8449', edgecolor='#145a32', linewidth=1)
    ax.add_patch(rect_sub_bot)

    # --- 4. HBM3e Chiplets (Black Rectangles on Substrate) ---
    hbm_w, hbm_h = 12, 12
    hbm_spacing = 20
    num_hbm = 8
    
    start_x = center_x - ((num_hbm * hbm_spacing) / 2) + hbm_spacing/2
    
    for i in range(num_hbm):
        # Top Row HBM
        hx = start_x + i * hbm_spacing - hbm_w/2
        hy_top = sub_top_y + (sub_h - hbm_h)/2
        hbm_top = Rectangle((hx, hy_top), hbm_w, hbm_h, color='black', alpha=0.9)
        ax.add_patch(hbm_top)
        
        # Bottom Row HBM
        hy_bot = sub_bot_y + (sub_h - hbm_h)/2
        hbm_bot = Rectangle((hx, hy_bot), hbm_w, hbm_h, color='black', alpha=0.9)
        ax.add_patch(hbm_bot)
        
        # BGA Dots visualization (tiny dots around HBM)
        ax.scatter([hx, hx+hbm_w], [hy_top, hy_top], color='#cdcdcd', s=1, alpha=0.5)

    # --- 5. The NCE Core (Wafer-Scale Die) ---
    # Center massive die.
    die_w, die_h = 240, 80 # huge
    die_x = center_x - die_w/2
    die_y = center_y - die_h/2
    
    # Gradient effect simulation for "Spectral Colors"
    # Matplotlib gradient is tricky, using stripes for diffraction grating look
    die_bg = Rectangle((die_x, die_y), die_w, die_h, facecolor='#101010', edgecolor='#00d4ff', linewidth=1.5)
    ax.add_patch(die_bg)
    
    # Diffractive Grid Texture (Cyan/Magenta shimmering lines)
    for i in range(0, int(die_w), 2):
        line_x = die_x + i
        color = '#00ffff' if i % 4 == 0 else '#ff00ff'
        alpha = 0.15 + (np.sin(i/10) * 0.1) # Shimmer effect
        ax.plot([line_x, line_x], [die_y, die_y + die_h], color=color, linewidth=0.5, alpha=alpha)

    # Text Label on Die
    ax.text(center_x, center_y, "LightRail NCE-1\nWafer-Scale Engine", 
            ha='center', va='center', color='white', fontsize=14, fontweight='bold', alpha=0.8)

    # --- 6. Optical Socket Interfaces (Ribbons) ---
    # 4 Top, 4 Bottom extending from wafer edge
    ribbon_w = 15
    ribbon_len = 40
    
    # Ribbon Positions (align with gaps in HBM maybe? or just evenly spaced)
    ribbon_spacing = die_w / 5
    
    for i in range(4):
        # Calculate X position
        rx = (die_x + ribbon_spacing) + i * ribbon_spacing - ribbon_w/2
        
        # --- Top Ribbons ---
        # Start at wafer edge (die_y + die_h) go UP
        # Draw Ribbon
        r_top_poly = Polygon([
            [rx, die_y + die_h], 
            [rx + ribbon_w, die_y + die_h],
            [rx + ribbon_w, die_y + die_h + ribbon_len],
            [rx, die_y + die_h + ribbon_len]
        ], closed=True, facecolor='#aaddff', alpha=0.4, edgecolor='none') # Translucent Blue/Cyan
        ax.add_patch(r_top_poly)
        
        # Draw "Blind-Mate Ferrule" (Black Block at end)
        ferrule_top = Rectangle((rx - 2, die_y + die_h + ribbon_len - 5), ribbon_w + 4, 12, color='black')
        ax.add_patch(ferrule_top)
        
        # --- Bottom Ribbons ---
        # Start at wafer edge (die_y) go DOWN
        r_bot_poly = Polygon([
            [rx, die_y], 
            [rx + ribbon_w, die_y],
            [rx + ribbon_w, die_y - ribbon_len],
            [rx, die_y - ribbon_len]
        ], closed=True, facecolor='#aaddff', alpha=0.4, edgecolor='none')
        ax.add_patch(r_bot_poly)
        
        # Ferrule
        ferrule_bot = Rectangle((rx - 2, die_y - ribbon_len - 7), ribbon_w + 4, 12, color='black')
        ax.add_patch(ferrule_bot)

    # --- 7. PCIe Edge Connector (Bottom Edge) ---
    # Only for power. Standard x16.
    conn_w = 80
    conn_h = 8
    conn_x = 20 # Offset to left usually
    conn_y = center_y - frame_h/2 - conn_h
    
    # Gold Fingers
    fingers = Rectangle((conn_x, conn_y), conn_w, conn_h, facecolor='#d4af37', edgecolor='none')
    ax.add_patch(fingers)
    ax.text(conn_x + conn_w/2, conn_y - 5, "PCIe Gen5 Power/Control", ha='center', color='#888', fontsize=8)

    # --- Branding & Info ---
    ax.text(20, pcb_h + 30, "LightRail AI", color='white', fontsize=24, fontweight='bold')
    ax.text(20, pcb_h + 15, "NCE-1 Wafer-Scale Module", color='#00d4ff', fontsize=14)
    ax.text(250, -40, "800G Optical Ribbons x8", color='#aaddff', fontsize=10)

    # --- Cleanup ---
    ax.set_xlim(-20, 350)
    ax.set_ylim(-60, 150)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='#0a0a0a')
    print(f"Rendered NCE-1 design to {output_file}")

if __name__ == "__main__":
    render_nce_module()
