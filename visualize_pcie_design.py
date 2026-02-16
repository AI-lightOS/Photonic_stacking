import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon, FancyArrowPatch

def render_pcie_card(output_file=r"C:\Users\bolao\Downloads\LightRail_AI_PCIe_Design.png"):
    """
    Render the LightRail AI board in a standard PCIe form factor.
    """
    # Create figure with dark background
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.set_facecolor('#1a1a1a')
    fig.patch.set_facecolor('#1a1a1a')
    
    # --- PCB Dimensions (Standard PCIe Half-Length) ---
    pcb_width = 167.65  # mm (approx 6.6 inches)
    pcb_height = 111.15 # mm (standard height)
    
    # Draw PCB Substrate (Black/Dark Grey)
    pcb = FancyBboxPatch((0, 0), pcb_width, pcb_height,
                        boxstyle="round,pad=0,rounding_size=2",
                        facecolor='#252525', edgecolor='#333333', linewidth=2)
    ax.add_patch(pcb)
    
    # --- PCIe Edge Connector (Gold Fingers) ---
    connector_width = 80.0 # x16 length approx
    connector_height = 8.0
    connector_x = 10.0
    connector_y = -connector_height
    
    # Connector simplified visual
    connector = Rectangle((connector_x, connector_y), connector_width, connector_height,
                         facecolor='#2a2a2a', edgecolor='none')
    ax.add_patch(connector)
    
    # Gold Fingers
    finger_width = 1.0
    finger_gap = 0.8
    num_fingers = int(connector_width / (finger_width + finger_gap))
    
    for i in range(num_fingers):
        fx = connector_x + i * (finger_width + finger_gap) + 2
        finger = Rectangle((fx, connector_y), finger_width, connector_height,
                          facecolor='#d4af37') # Gold color
        ax.add_patch(finger)
        
    # --- PCIe Bracket (Metal) ---
    bracket_width = 20.0
    bracket_height = pcb_height + 20
    bracket_x = -bracket_width
    bracket_y = -10
    
    bracket = Rectangle((bracket_x, bracket_y), bracket_width, bracket_height,
                       facecolor='#b0b0b0', edgecolor='#808080', linewidth=1)
    ax.add_patch(bracket)
    
    # Bracket "Tab" (Top)
    tab_w = 10
    tab_h = 10
    tab = Rectangle((bracket_x, bracket_y + bracket_height), bracket_width + tab_w, 2,
                   facecolor='#b0b0b0')
    ax.add_patch(tab)
    
    # Ports on Bracket (USB-C / QSFP-DD cues)
    port1 = Rectangle((bracket_x + 5, 20), 10, 20, facecolor='#1a1a1a', edgecolor='black')
    ax.add_patch(port1)
    port2 = Rectangle((bracket_x + 5, 60), 10, 20, facecolor='#1a1a1a', edgecolor='black')
    ax.add_patch(port2)

    # --- Key Components ---
    
    # 1. TFLN Modulator (The Star Show)
    mod_w, mod_h = 60, 30
    mod_x, mod_y = 50, 60
    
    # Package body
    modulator = Rectangle((mod_x, mod_y), mod_w, mod_h,
                         facecolor='#e0e0e0', edgecolor='#00d4ff', linewidth=2)
    ax.add_patch(modulator)
    
    ax.text(mod_x + mod_w/2, mod_y + mod_h/2, "TFLN Modulator\n(Gen 3)", 
            ha='center', va='center', color='black', fontsize=10, fontweight='bold')
            
    # Fiber Inputs/Outputs (Blue strands)
    ax.plot([mod_x - 30, mod_x], [mod_y + 10, mod_y + 10], color='#00d4ff', linewidth=2)
    ax.plot([mod_x - 30, mod_x], [mod_y + 20, mod_y + 20], color='#00d4ff', linewidth=2)
    
    # 2. Control ASIC / FPGA (Main Processor)
    asic_w, asic_h = 35, 35
    asic_x, asic_y = 50, 15
    
    asic = Rectangle((asic_x, asic_y), asic_w, asic_h,
                    facecolor='#111111', edgecolor='#444444', linewidth=1)
    ax.add_patch(asic)
    
    ax.text(asic_x + asic_w/2, asic_y + asic_h/2, "LightRail AI\nControl Chip",
            ha='center', va='center', color='white', fontsize=8)

    # 3. Heatsink (Finned Look)
    hs_x, hs_y = 100, 20
    hs_w, hs_h = 50, 70
    
    heatsink_base = Rectangle((hs_x, hs_y), hs_w, hs_h,
                             facecolor='#404040', alpha=0.9)
    ax.add_patch(heatsink_base)
    
    # Fins
    for i in range(10):
        fin_x = hs_x + i * (hs_w / 10)
        ax.plot([fin_x, fin_x], [hs_y, hs_y + hs_h], color='#606060', linewidth=1)

    # Airflow Arrows
    arrow_props = dict(facecolor='#00ff88', edgecolor='none', alpha=0.6)
    
    # Front-to-Back Airflow cues
    ax.add_patch(FancyArrowPatch((160, 50), (120, 50), 
                                arrowstyle='->', mutation_scale=20, color='#00ff88', alpha=0.5))

    # --- Branding ---
    ax.text(120, 100, "LightRail AI", color='white', fontsize=16, fontweight='bold', fontname='Arial')
    ax.text(120, 95, "x16 PCIe Gen5", color='#aaaaaa', fontsize=10)

    # --- Setup Plot Limits ---
    ax.set_xlim(-30, 180)
    ax.set_ylim(-20, 130)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='#1a1a1a')
    print(f"Rendered PCIe design to {output_file}")

if __name__ == "__main__":
    render_pcie_card()
