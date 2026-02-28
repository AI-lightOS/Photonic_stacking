
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors

def generate_15_layer_schematic(output_file="static/15_layer_schematic.svg"):
    """
    Generates a schematic visualization of a 15-layer photonic 3D stack.
    Based on standard advanced packaging architectures (CoWoS / 3D-IC).
    """
    fig, ax = plt.subplots(figsize=(12, 16))
    ax.set_facecolor('#0f1629')
    fig.patch.set_facecolor('#0f1629')
    
    # Layer definitions (Name, Color, Thickness/Height, Width modifier)
    layers = [
        ("Layer 15: Heat Sink / Cooling Plate", "#4a90e2", 1.5, 1.0),
        ("Layer 14: Thermal Interface Material (TIM)", "#d0d0d0", 0.3, 0.9),
        ("Layer 13: Integrated Heat Spreader (IHS)", "#b0b0b0", 1.0, 0.95),
        ("Layer 12: Top Logic Die (Compute Core)", "#ff6b6b", 0.8, 0.6),
        ("Layer 11: 3D Bonding Interface (Hybrid Bond)", "#ffd93d", 0.2, 0.6),
        ("Layer 10: Bottom Logic Die / SRAM", "#ff8c42", 0.8, 0.6),
        ("Layer 9:  Silicon Interposer Top Metal", "#a0aec0", 0.4, 0.8),
        ("Layer 8:  TFLN Photonic Layer (Waveguides)", "#00d4ff", 0.6, 0.75),
        ("Layer 7:  Through-Silicon Vias (TSV)", "#718096", 1.2, 0.75),
        ("Layer 6:  Silicon Interposer Base", "#4a5568", 0.8, 0.8),
        ("Layer 5:  Interposer Bottom Bump (C4)", "#cbd5e0", 0.3, 0.8),
        ("Layer 4:  Package Substrate Top Metal", "#f6e05e", 0.2, 1.0),
        ("Layer 3:  Organic Package Substrate (Core)", "#2d3748", 2.0, 1.0),
        ("Layer 2:  Package Substrate Bottom Metal", "#f6e05e", 0.2, 1.0),
        ("Layer 1:  BGA Ball Grid Array", "#e2e8f0", 0.5, 1.0),
    ]

    current_y = 1.0
    center_x = 5.0
    
    # Draw from bottom up
    for i, (name, color, height, width_mod) in enumerate(reversed(layers)):
        layer_idx = len(layers) - i - 1
        width = 8.0 * width_mod
        x = center_x - (width / 2.0)
        y = current_y
        
        # Draw the main layer rectangle
        rect = patches.Rectangle((x, y), width, height, 
                               fc=color, ec='white', linewidth=1.0, alpha=0.9,
                               zorder=10)
        ax.add_patch(rect)
        
        # Highlight/Texture for specific layers
        if "Logic" in name:
            # Add "circuit" texture
            for _ in range(10):
                import random
                lx = x + random.random() * width * 0.9
                ly = y + random.random() * height * 0.9
                w = random.random() * width * 0.1
                h = random.random() * height * 0.1
                ax.add_patch(patches.Rectangle((lx, ly), w, h, fc='white', alpha=0.2, zorder=11))
        
        if "TFLN" in name:
             # Add waveguides
             ax.plot([x, x+width], [y+height/2, y+height/2], color='white', linewidth=2, linestyle='--', zorder=12, alpha=0.7)
             ax.text(center_x, y+height/2, "~~~ Photon Path ~~~", color='white', ha='center', va='center', fontsize=8, fontweight='bold', zorder=13)

        if "BGA" in name or "Bump" in name:
            # Draw balls instead of solid block? 
            # Let's just overlay circles to represent balls
            num_balls = int(width * 2)
            ball_spacing = width / num_balls
            for b in range(num_balls):
                bx = x + b * ball_spacing + ball_spacing/2
                by = y + height/2
                radius = min(height, ball_spacing) / 2.5
                circle = patches.Circle((bx, by), radius, fc='#888888', ec='black', zorder=12)
                ax.add_patch(circle)

        # Add Label Line
        # Line from right side of layer to label
        label_x_start = x + width
        label_x_end = 10.0
        label_y = y + height / 2.0
        
        ax.plot([label_x_start, label_x_end], [label_y, label_y], color='white', linewidth=0.5, linestyle=':', alpha=0.5)
        
        # Add Label Text
        ax.text(label_x_end + 0.2, label_y, name, 
                color='#e0e6ed', fontsize=10, va='center', fontweight='bold')

        current_y += height + 0.1 # Gap

    # Set limits and clean up
    ax.set_xlim(0, 16)
    ax.set_ylim(0, current_y + 1)
    ax.axis('off')
    
    # Title
    ax.text(8, current_y + 0.5, "15-Layer 3D Photonic Stack Architecture", 
            color='#00d4ff', fontsize=16, ha='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_file, format='svg', facecolor='#0f1629')
    print(f"Generated schematic at {output_file}")

if __name__ == "__main__":
    generate_15_layer_schematic()
