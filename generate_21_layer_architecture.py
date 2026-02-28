import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def generate_improved_architecture_diagram(output_file="advanced_21_layer_architecture.jpg"):
    fig, ax = plt.subplots(figsize=(14, 16))
    
    # Define the 21-layer architecture
    # Format: (Layer Num, Name, Category/Color, Description)
    layers = [
        (21, "Active Liquid Cooling Manifold", "cooling", "Top-level pumped microfluidic cooling"),
        (20, "Vapor Chamber & TIM", "cooling", "High-efficiency heat spreading"),
        (19, "Top AI Compute Core (L3)", "logic", "Neural processing & orchestration"),
        (18, "DSP & Control Logic (L2)", "logic", "Signal processing & error correction"),
        (17, "SRAM / HBM Memory Layer (L1)", "memory", "High-bandwidth local memory cache"),
        (16, "Hybrid Bonding Interface", "bond", "Cu-Cu face-to-face logic-to-photonics bond"),
        (15, "Photonic Routing - Multiplexers", "photonics", "WDM/AWG frequency multiplexing"),
        (14, "Photonic Routing - Ring Resonators", "photonics", "Dense comb generation & filtering"),
        (13, "Photonic Routing - TFLN Modulators", "photonics", "Ultra-high speed electro-optic modulation"),
        (12, "Photonic Routing - Passive & I/O", "photonics", "Low-loss waveguides & fiber coupling"),
        (11, "Silicon Interposer Top Metal (RDL)", "interposer", "High-density fan-out routing"),
        (10, "High-Aspect Ratio TSV Core", "interposer", "Through-silicon vias for vertical power/signal"),
        (9,  "Silicon Interposer Base Metal (RDL)", "interposer", "Signal spreading to package substrate"),
        (8,  "Ultra-Shielded RF Signal (TX)", "rf", "Differential high-speed RF transmit (<0.1dB/cm)"),
        (7,  "RF Ground Plane (TX Shield)", "gnd", "Crosstalk isolation for TX"),
        (6,  "Ultra-Shielded RF Signal (RX)", "rf", "Differential high-speed RF receive"),
        (5,  "RF Ground Plane (RX Shield)", "gnd", "Crosstalk isolation for RX"),
        (4,  "Power Delivery Network (PDN) L2", "pwr", "Clean analog power rails for modulators"),
        (3,  "Integrated Decoupling Capacitors", "passive", "Embedded deep-trench capacitors for PDN"),
        (2,  "Power Delivery Network (PDN) L1", "pwr", "Main digital power distribution"),
        (1,  "Advanced BGA System Interface", "base", "High-density ball grid array (>2000 pins)"),
    ]
    
    # Color scheme
    colors = {
        "cooling": "#add8e6", # Light blue
        "logic": "#ff9999",   # Light red/pink
        "memory": "#ffcc99",  # Light orange
        "bond": "#e6e6fa",    # Lavender
        "photonics": "#90ee90", # Light green
        "interposer": "#d3d3d3", # Light gray
        "rf": "#ffb6c1",      # Light pink
        "gnd": "#a9a9a9",     # Dark gray
        "pwr": "#ffff99",     # Light yellow
        "passive": "#dda0dd", # Plum
        "base": "#8fbc8f"     # Dark sea green
    }
    
    box_width = 10
    box_height = 0.8
    y_gap = 0.2
    start_y = 0
    
    # Draw from bottom (layer 1) to top (layer 21)
    for idx, (num, name, cat, desc) in enumerate(reversed(layers)):
        y_pos = start_y + idx * (box_height + y_gap)
        
        # Draw layer box
        rect = patches.Rectangle((0, y_pos), box_width, box_height, 
                               linewidth=1.5, edgecolor='black', facecolor=colors[cat])
        ax.add_patch(rect)
        
        # Add text (Layer Number and Name)
        plt.text(box_width/2, y_pos + box_height/2 + 0.1, 
                 f"Layer {num}: {name}", 
                 horizontalalignment='center', verticalalignment='center',
                 fontsize=12, fontweight='bold', color='black')
                 
        # Add description below name
        plt.text(box_width/2, y_pos + box_height/2 - 0.2, 
                 desc, 
                 horizontalalignment='center', verticalalignment='center',
                 fontsize=9, fontstyle='italic', color='#333333')

    # Add TSV vertical connections through interposer (Layers 9,10,11)
    # y positions for layers 9, 10, 11
    interposer_y_start = start_y + 8 * (box_height + y_gap)
    interposer_y_end = start_y + 11 * (box_height + y_gap)
    for x_pos in [2, 4, 6, 8]:
        plt.plot([x_pos, x_pos], [interposer_y_start, interposer_y_end], 
                color='gold', linewidth=3, linestyle='--', zorder=0)

    # Styling
    ax.set_xlim(-1, box_width + 5)
    ax.set_ylim(-1, start_y + 21 * (box_height + y_gap) + 2)
    ax.axis('off')
    
    # Add Legend
    legend_elements = [patches.Patch(facecolor=color, edgecolor='black', label=cat.capitalize()) 
                      for cat, color in colors.items()]
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1), 
              title="Layer Tiers", fontsize=10, title_fontsize=12)
    
    # Title and Metadata
    plt.title("Advanced 21-Layer Photonic 3D Multi-Stack Architecture", fontsize=16, fontweight='bold', y=0.98)
    plt.text(-0.5, ax.get_ylim()[1] - 1.5, "Optimized for:\n- Extreme Bandwidth Density\n- Ultra-Low Latency (<1ns)\n- Superior Crosstalk Isolation\n- Elite Thermal Dissipation", 
             fontsize=12, bbox=dict(facecolor='white', alpha=0.8, edgecolor='black'))
             
    plt.tight_layout()
    plt.savefig(output_file, format='jpg', dpi=300, bbox_inches='tight')
    print(f"✅ Successfully generated advanced architecture diagram: {output_file}")

if __name__ == "__main__":
    generate_improved_architecture_diagram()
