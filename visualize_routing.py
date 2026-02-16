"""
LightRailAI CPO Interconnect - Routing Visualization
Focusing on L1 (RF) and L3 (SerDes) critical paths.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def visualize_routing(output_file="LightRailAI_Routing_View.png"):
    print(f"Generating {output_file}...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    
    width, height = 106.68, 111.15
    
    # --- LAYER 1: RF MODULATOR DRIVE (50Ω) ---
    ax1.set_facecolor('#0a0e27')
    ax1.add_patch(patches.Rectangle((0, 0), width, height, color='#1c2331', alpha=0.5))
    
    # U1 Modulator Die
    u1_w, u1_h = 25, 12
    u1_x, u1_y = 40, 60
    ax1.add_patch(patches.Rectangle((u1_x, u1_y), u1_w, u1_h, color='#3498db', ec='white', alpha=0.3))
    ax1.text(u1_x+u1_w/2, u1_y+u1_h/2, "U1\nTFLN Die", color='white', ha='center', va='center', fontsize=12)
    
    # RF Traces (L1 Top)
    rf_y_offsets = [-4, -2, 2, 4]
    for y_off in rf_y_offsets:
        ax1.plot([u1_x+u1_w, width], [u1_y+u1_h/2+y_off, u1_y+u1_h/2+y_off*10], color='#ff4757', linewidth=2, label='50Ω RF' if y_off == -4 else "")
    
    ax1.set_title("LAYER 1: RF MODULATOR DRIVE (50Ω SE)\nMaterial: Rogers 4350B", color='white', fontsize=14)
    ax1.set_aspect('equal')
    ax1.axis('off')

    # --- LAYER 3: SerDes HIGH-SPEED (85Ω DIFF) ---
    ax2.set_facecolor('#0a0e27')
    ax2.add_patch(patches.Rectangle((0, 0), width, height, color='#1c2331', alpha=0.5))
    
    # U9 SerDes BGA
    u9_w, u9_h = 20, 20
    u9_x, u9_y = 42, 35
    ax2.add_patch(patches.Rectangle((u9_x, u9_y), u9_w, u9_h, color='#e74c3c', ec='white', alpha=0.3))
    ax2.text(u9_x+u9_w/2, u9_y+u9_h/2, "U9\nBCM84881", color='white', ha='center', va='center', fontsize=12)
    
    # SerDes Differential Pairs (L3 Signal)
    for i in range(8):
        y_start = u9_y + 2 + i*2
        ax2.plot([u9_x, 10], [y_start, 5+i], color='#1e90ff', linewidth=1.5, alpha=0.8, label='85Ω Diff' if i == 0 else "")
        ax2.plot([u9_x+u9_w, 90], [y_start, 5+i], color='#1e90ff', linewidth=1.5, alpha=0.8)

    ax2.set_title("LAYER 3: SerDes TX/RX (85Ω DIFF)\nMaterial: Rogers 4350B", color='white', fontsize=14)
    ax2.set_aspect('equal')
    ax2.axis('off')

    plt.suptitle("LIGHTRAILAI CPO INTERCONNECT - CRITICAL ROUTING TOPOLOGY", color='cyan', fontsize=20, fontweight='bold', y=0.95)
    plt.tight_layout(rect=[0, 0.03, 1, 0.9])
    plt.savefig(output_file, dpi=200, facecolor='#0a0e27')
    plt.close()
    print(f"Generated LightRailAI routing visualization: {output_file}")

if __name__ == "__main__":
    visualize_routing()
