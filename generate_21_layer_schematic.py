import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os

def generate_improved_architecture_diagram(output_file="static/advanced_21_layer_architecture.jpg"):
    """
    Generates a high-fidelity 2D schematic of the 21-layer Photonic Multi-Stack.
    Grouped by logical 'tiers' for clarity.
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(14, 18), facecolor='#0a0e27')
    ax.set_facecolor('#0a0e27')
    
    # Define Tiers and Layers
    # Each entry: (Layer#, Name, Category, Description)
    layers = [
        (21, "Active Liquid Cooling Manifold", "cooling", "Top-level pumped microfluidic cooling"),
        (20, "Vapor Chamber & TIM", "cooling", "High-K thermal interface material"),
        (19, "Top AI Compute Core (L3)", "logic", "7nm FinFET AI Acceleration cluster"),
        (18, "DSP & Control Logic (L2)", "logic", "Sub-system management and control"),
        (17, "SRAM / HBM Memory Layer (L1)", "memory", "High-density stacked memory"),
        (16, "Hybrid Bonding Interface", "bond", "Cu-Cu Pitch bonding layer"),
        (15, "Photonic Routing - Multiplexers", "photonics", "WDM mux/demux grid"),
        (14, "Photonic Routing - Ring Resonators", "photonics", "Dynamic filtering/modulation"),
        (13, "Photonic Routing - TFLN Modulators", "photonics", "Thin-Film Lithium Niobate EO core"),
        (12, "Photonic Routing - Passive & I/O", "photonics", "Edge coupling and alignment"),
        (11, "Silicon Interposer Top Metal (RDL)", "interposer", "Redistribution routing"),
        (10, "High-Aspect Ratio TSV Core", "interposer", "Vertical electrical connectivity"),
        (9,  "Silicon Interposer Base Metal (RDL)", "interposer", "Bottom redistribution layer"),
        (8,  "Ultra-Shielded RF Signal (TX)", "rf", "High-speed transmission signal"),
        (7,  "RF Ground Plane (TX Shield)", "gnd", "Isolation shield"),
        (6,  "Ultra-Shielded RF Signal (RX)", "rf", "High-speed receive signal"),
        (5,  "RF Ground Plane (RX Shield)", "gnd", "Isolation shield"),
        (4,  "Power Delivery Network (PDN) L2", "pwr", "Stable DC distribution"),
        (3,  "Integrated Decoupling Capacitors", "passive", "High-density MIM decoupling"),
        (2,  "Power Delivery Network (PDN) L1", "pwr", "Primary power intake"),
        (1,  "Advanced BGA System Interface", "base", "High-density ball grid array (>2000 pins)"),
    ]
    
    colors = {
        "cooling": "#add8e6", # Light blue
        "logic": "#ff9999", # Soft red
        "memory": "#ffcc99", # Light orange
        "bond": "#e6e6fa", # Lavender
        "photonics": "#90ee90", # Light green
        "interposer": "#d3d3d3", # Light gray
        "rf": "#ffb6c1", # Pinkish
        "gnd": "#a9a9a9", # Dark gray
        "pwr": "#ffff99", # Light yellow
        "passive": "#dda0dd", # Plum
        "base": "#8fbc8f", # Dark sea green
    }
    
    # Draw Layers from bottom to top
    y_start = 1.0
    layer_height = 0.6
    spacing = 0.15
    
    for i, (lnum, name, cat, desc) in enumerate(reversed(layers)):
        y = y_start + i * (layer_height + spacing)
        
        # Draw Layer Rectangle
        rect = Rectangle((2.5, y), 8, layer_height, facecolor=colors[cat], edgecolor='white', alpha=0.9, linewidth=1.5)
        ax.add_patch(rect)
        
        # Layer Number Label
        ax.text(1.5, y + layer_height/2, f"L{lnum:02d}", color='white', ha='center', va='center', fontsize=14, fontweight='bold')
        
        # Information Label (inside/next to)
        ax.text(6.5, y + layer_height/2, name, color='#0a0e27', ha='center', va='center', fontsize=13, fontweight='bold')
        
        # Description (side)
        ax.text(10.7, y + layer_height/2, f"← {desc}", color='cyan', ha='left', va='center', fontsize=11, fontstyle='italic')
        
        # Vertical TSV lines (visual cue for connectivity)
        if lnum > 1:
            ax.plot([3.5, 3.5], [y - spacing, y], color='white', alpha=0.3, linewidth=2, linestyle='--')
            ax.plot([9.5, 9.5], [y - spacing, y], color='white', alpha=0.3, linewidth=2, linestyle='--')

    # Legend for Categories
    legend_y = y_start + len(layers) * (layer_height + spacing) + 0.5
    cat_keys = list(colors.keys())
    for idx, cat in enumerate(cat_keys):
        row = idx // 4
        col = idx % 4
        ax.add_patch(Rectangle((col * 3.5, legend_y - row * 0.8), 0.5, 0.4, facecolor=colors[cat], edgecolor='white'))
        ax.text(col * 3.5 + 0.6, legend_y - row * 0.8 + 0.2, cat.upper(), color='white', fontsize=10, va='center')

    # Title & Overall Design
    plt.title("Advanced 21-Layer Photonic Multi-Stack Architecture", color='#00d4ff', fontsize=24, fontweight='bold', pad=40)
    
    # Add some 'features' annotations
    ax.text(7, legend_y + 1, "INTEGRATED COOLING • PHOTONIC LOGIC • RF INTERPOSER", 
            color='#00ff88', fontsize=16, fontweight='bold', ha='center', bbox=dict(facecolor='black', alpha=0.5, edgecolor='#00ff88'))

    ax.set_xlim(0, 16)
    ax.set_ylim(0, legend_y + 2)
    ax.set_axis_off()
    
    # Save to static directory for app use
    plt.savefig(output_file, format='jpg', dpi=300, bbox_inches='tight', facecolor='#0a0e27')
    print(f"✅ Enhanced Architecture Diagram saved to {output_file}")
    plt.close()

if __name__ == "__main__":
    generate_improved_architecture_diagram()
