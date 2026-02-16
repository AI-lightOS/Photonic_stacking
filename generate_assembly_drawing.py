"""
LightRailAI CPO Interconnect - Assembly & Wire Bonding Drawing
Enhanced with technical characteristics and critical routing notes.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

def generate_assembly_drawing(output_file="LightRail_Assembly_Drawing.png"):
    print(f"Generating {output_file}...")
    
    fig, ax = plt.subplots(figsize=(18, 18))
    ax.set_facecolor('#fdfdfd')
    
    # Board Boundary
    width, height = 106.68, 111.15
    rect = patches.Rectangle((0, 0), width, height, linewidth=3, edgecolor='black', facecolor='#e6f3e6', alpha=0.3)
    ax.add_patch(rect)
    
    # --- COMPONENTS ---
    
    # J1: PCIe Gen5 x16 Edge Connector
    ax.add_patch(patches.Rectangle((10, -2), 80, 5, color='#ffd700', alpha=0.8, ec='black'))
    ax.text(50, 0.5, 'J1: PCIe Gen5 x16', ha='center', va='center', fontweight='bold', fontsize=10)
    
    # U1: TFLN Mach-Zehnder Modulator
    u1_w, u1_h = 25, 12
    u1_x, u1_y = 40, 60
    ax.add_patch(patches.Rectangle((u1_x, u1_y), u1_w, u1_h, color='#3498db', alpha=0.5, ec='black', linewidth=2))
    ax.text(u1_x + u1_w/2, u1_y + u1_h/2, 'U1: TFLN Modulator\n(DNP - Manual Align)', ha='center', va='center', fontweight='bold', fontsize=10)
    
    # U9: SerDes IC (Broadcom BCM84881)
    ax.add_patch(patches.Rectangle((42, 35), 20, 20, color='#e74c3c', alpha=0.4, ec='black'))
    ax.text(52, 45, 'U9: SerDes\nBCM84881', ha='center', va='center', fontweight='bold', fontsize=9)
    
    # U10: Precision Clock
    ax.add_patch(patches.Rectangle((75, 45), 8, 8, color='#9b59b6', alpha=0.4, ec='black'))
    ax.text(79, 49, 'U10\nSi5395A', ha='center', va='center', fontsize=8)

    # J4-J7: SMA Connectors
    sma_y = [20, 40, 60, 80]
    for i, y in enumerate(sma_y):
        ax.add_patch(patches.Circle((width + 2, y), 3, color='#f1c40f', ec='black'))
        ax.text(width + 2, y, f'J{i+4}', ha='center', va='center', fontweight='bold', fontsize=8)

    # OPT1: Fiber Couplers
    ax.add_patch(patches.Rectangle((35, 75), 5, 10, color='#1abc9c', alpha=0.6, ec='black'))
    ax.add_patch(patches.Rectangle((65, 75), 5, 10, color='#1abc9c', alpha=0.6, ec='black'))
    ax.text(37.5, 87, 'OPT1-In', ha='center', fontsize=8)
    ax.text(67.5, 87, 'OPT1-Out', ha='center', fontsize=8)

    # --- ROUTING VISUALIZATION ---
    # Critical RF Traces (L1)
    ax.plot([52, 106], [66, 60], color='red', linewidth=2, linestyle='-', alpha=0.8, label='RF (50 ohm)')
    ax.plot([52, 106], [66, 40], color='red', linewidth=2, linestyle='-', alpha=0.8)
    
    # SerDes Diff Pairs (L3 - shown as ghosted)
    ax.plot([52, 20], [45, 10], color='blue', linewidth=3, linestyle='--', alpha=0.3, label='SerDes (85 ohm Diff)')
    ax.plot([52, 80], [45, 10], color='blue', linewidth=3, linestyle='--', alpha=0.3)

    # --- TECHNICAL CHARACTERISTICS BOX ---
    char_box = patches.Rectangle((5, 115), 50, 25, facecolor='#f8f9fa', edgecolor='blue', linewidth=1)
    ax.add_patch(char_box)
    ax.text(7, 137, "TECHNICAL CHARACTERISTICS", fontweight='bold', fontsize=12, color='blue')
    ax.text(7, 133, "• Throughput: 3.2 Tbps (8x 400G Lanes)", fontsize=10)
    ax.text(7, 129, "• Power Envelope: <15W Total Module Power", fontsize=10)
    ax.text(7, 125, "• RF Bandwidth: 100 GHz per lane", fontsize=10)
    ax.text(7, 121, "• Optical Efficiency: <1 pJ/bit", fontsize=10)
    ax.text(7, 117, "• Material: Rogers 4350B Hybrid 15-Layer", fontsize=10)

    # --- WIRE BONDING DETAIL ---
    bond_box = patches.Rectangle((60, 115), 45, 25, facecolor='#fffde7', edgecolor='#fbc02d', linewidth=1)
    ax.add_patch(bond_box)
    ax.text(62, 137, "WIRE BONDING DETAIL (U1/U3)", fontweight='bold', fontsize=12, color='#f57f17')
    ax.text(62, 133, "• Type: Gold Wire, Wedge Bonding", fontsize=10)
    ax.text(62, 129, "• Wire Diameter: 25um (0.001 mil)", fontsize=10)
    ax.text(62, 125, "• Pad Finish: ENIG (Electroless Nickel/Gold)", fontsize=10)
    ax.text(62, 121, "• Critical Note: Do not bond until optical", fontsize=10)
    ax.text(62, 117, "  alignment is calibrated (>5dBm loopback)", fontsize=10)

    # --- ROUTING & IMPEDANCE TABLE ---
    ax.text(5, -15, "CRITICAL ROUTING NOTES:", fontweight='bold', fontsize=11)
    ax.text(5, -19, "1. L1 (Top): RF Modulator Drive - 50Ω ±2% Single-Ended. Rogers 4350B required.", fontsize=10)
    ax.text(5, -23, "2. L3 (Sig): SerDes Rx/Tx - 85Ω ±5% Differential Stripline. Rogers 4350B dielectric.", fontsize=10)
    ax.text(5, -27, "3. Vias: Blind (L1-L2) for RF GND; Buried (L3-L12) for internal signals.", fontsize=10)

    ax.set_xlim(-10, width + 15)
    ax.set_ylim(-30, 145)
    ax.set_aspect('equal')
    ax.set_title("LightRailAI CPO Interconnect - ASSEMBLY & WIRING DIAGRAM\nv3.0 Production Specification", fontsize=18, fontweight='bold', pad=20)
    
    plt.legend(loc='lower right', fontsize=10)
    plt.savefig(output_file, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"Generated enhanced assembly drawing with characteristics and wiring.")

if __name__ == "__main__":
    generate_assembly_drawing()
