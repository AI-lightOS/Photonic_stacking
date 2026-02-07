
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from io import BytesIO

def generate_tfln_circuit_schematic():
    """Generate SVG schematic for TFLN modulator circuit"""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_axis_off()
    
    # Define colors
    c_optical = '#00d4ff'
    c_elec = '#ffd700'
    c_gnd = '#000000'
    c_res = '#ffffff'
    
    # ---------------------------------------------------------
    # 1. OPTICAL PATH (TFLN MZM)
    # ---------------------------------------------------------
    # Input Waveguide
    ax.plot([0, 2], [5, 5], color=c_optical, linewidth=3)
    ax.text(0.5, 5.2, 'Optical In\n(1550 nm)', fontsize=10, ha='center', color='blue')

    # Y-Splitter
    ax.plot([2, 4], [5, 6.5], color=c_optical, linewidth=3)
    ax.plot([2, 4], [5, 3.5], color=c_optical, linewidth=3)

    # MZM Arms (Interaction Region)
    ax.plot([4, 12], [6.5, 6.5], color=c_optical, linewidth=3) # Top Arm
    ax.plot([4, 12], [3.5, 3.5], color=c_optical, linewidth=3) # Bottom Arm

    # Y-Combiner
    ax.plot([12, 14], [6.5, 5], color=c_optical, linewidth=3)
    ax.plot([12, 14], [3.5, 5], color=c_optical, linewidth=3)

    # Output Waveguide
    ax.plot([14, 16], [5, 5], color=c_optical, linewidth=3)
    ax.text(15.5, 5.2, 'Modulated Out\n(400G PAM4)', fontsize=10, ha='center', color='blue')

    # ---------------------------------------------------------
    # 2. RF ELECTRODES (Ground-Signal-Ground-Signal-Ground)
    # ---------------------------------------------------------
    # Signal Electrodes (Traveling Wave)
    # Top Arm Signal
    rect_sig_top = patches.Rectangle((4.5, 6.7), 7, 0.4, linewidth=1, edgecolor=c_elec, facecolor=c_elec, alpha=0.6)
    ax.add_patch(rect_sig_top)
    ax.text(8, 7.3, 'Signal Electrode (+)', fontsize=9, ha='center')

    # Bottom Arm Signal (Push-Pull)
    rect_sig_bot = patches.Rectangle((4.5, 2.9), 7, 0.4, linewidth=1, edgecolor=c_elec, facecolor=c_elec, alpha=0.6)
    ax.add_patch(rect_sig_bot)
    ax.text(8, 2.7, 'Signal Electrode (-)', fontsize=9, ha='center')

    # Ground Electrodes
    rect_gnd_mid = patches.Rectangle((4.5, 4.8), 7, 0.4, linewidth=1, edgecolor='gray', facecolor='#dddddd', alpha=0.6)
    ax.add_patch(rect_gnd_mid)
    ax.text(8, 5.0, 'Common Ground', fontsize=9, ha='center')

    # ---------------------------------------------------------
    # 3. TERMINATION CIRCUIT
    # ---------------------------------------------------------
    # Top Termination
    ax.plot([11.5, 11.5], [6.9, 7.5], 'k-', linewidth=1) # Trace to Resistor
    res_top = patches.Rectangle((11.3, 7.5), 0.4, 0.8, linewidth=1, edgecolor='black', facecolor=c_res)
    ax.add_patch(res_top)
    ax.text(12.0, 7.9, '50Ω', fontsize=9)
    ax.plot([11.5, 11.5], [8.3, 8.5], 'k-', linewidth=1) # To Ground
    # Ground Symbol
    ax.plot([11.2, 11.8], [8.5, 8.5], 'k-', linewidth=1)
    ax.plot([11.35, 11.65], [8.6, 8.6], 'k-', linewidth=1)
    ax.plot([11.45, 11.55], [8.7, 8.7], 'k-', linewidth=1)

    # Bottom Termination
    ax.plot([11.5, 11.5], [3.1, 2.5], 'k-', linewidth=1) # Trace to Resistor
    res_bot = patches.Rectangle((11.3, 1.7), 0.4, 0.8, linewidth=1, edgecolor='black', facecolor=c_res)
    ax.add_patch(res_bot)
    ax.text(12.0, 2.1, '50Ω', fontsize=9)
    ax.plot([11.5, 11.5], [1.7, 1.5], 'k-', linewidth=1) # To Ground
    # Ground Symbol
    ax.plot([11.2, 11.8], [1.5, 1.5], 'k-', linewidth=1)
    ax.plot([11.35, 11.65], [1.6, 1.6], 'k-', linewidth=1)
    ax.plot([11.45, 11.55], [1.7, 1.7], 'k-', linewidth=1)

    # ---------------------------------------------------------
    # 4. DIFFERENTIAL DRIVER STAGE
    # ---------------------------------------------------------
    # Driver Box
    driver_box = patches.Rectangle((-3, 2), 2.5, 6, linewidth=2, edgecolor='black', facecolor='#f0f0f0')
    ax.add_patch(driver_box)
    ax.text(-1.75, 7.5, 'Differential\nDriver IC', fontsize=11, ha='center', weight='bold')

    # Driver Outputs
    ax.plot([-0.5, 4.5], [6.9, 6.9], 'k-', linewidth=1.5) # Top Drive
    ax.plot([-0.5, 4.5], [3.1, 3.1], 'k-', linewidth=1.5) # Bottom Drive

    # AC Coupling Caps
    cap_top_1 = patches.Rectangle((1.5, 6.7), 0.2, 0.4, linewidth=1, edgecolor='black', facecolor='white')
    cap_top_2 = patches.Rectangle((1.9, 6.7), 0.2, 0.4, linewidth=1, edgecolor='black', facecolor='white')
    ax.add_patch(cap_top_1)
    ax.add_patch(cap_top_2)

    cap_bot_1 = patches.Rectangle((1.5, 2.9), 0.2, 0.4, linewidth=1, edgecolor='black', facecolor='white')
    cap_bot_2 = patches.Rectangle((1.9, 2.9), 0.2, 0.4, linewidth=1, edgecolor='black', facecolor='white')
    ax.add_patch(cap_bot_1)
    ax.add_patch(cap_bot_2)
    
    ax.text(1.8, 7.2, '100nF', fontsize=8, ha='center')
    ax.text(1.8, 2.6, '100nF', fontsize=8, ha='center')

    # Bias Tee Inductors (Conceptual)
    # Top Bias
    ax.plot([3.0, 3.0], [6.9, 8.0], 'k-', linewidth=1)
    # Coil
    x_coil = np.linspace(2.8, 3.2, 20)
    y_coil = np.linspace(8.0, 9.0, 20)
    ax.plot(x_coil, y_coil, 'k-', linewidth=1) # Simplified coil
    ax.text(3.3, 8.5, 'Bias T', fontsize=8)
    ax.text(3.0, 9.2, 'V_bias1', fontsize=9, ha='center')

    # Bottom Bias
    ax.plot([3.0, 3.0], [3.1, 2.0], 'k-', linewidth=1)
    # Coil
    x_coil = np.linspace(2.8, 3.2, 20)
    y_coil = np.linspace(2.0, 1.0, 20)
    ax.plot(x_coil, y_coil, 'k-', linewidth=1) # Simplified coil
    ax.text(3.3, 1.5, 'Bias T', fontsize=8)
    ax.text(3.0, 0.8, 'V_bias2', fontsize=9, ha='center')

    # ---------------------------------------------------------
    # 5. LABELS AND TITLE
    # ---------------------------------------------------------
    ax.set_title('Densified Optimal TFLN Modulator Schematic\n(Differential Drive, 50Ω Terminated)', fontsize=16, weight='bold', pad=20)
    
    # Legend
    ax.text(0, 0, 'Design Parameters:\n- Vπ: 1.85V\n- Bandwidth: 100GHz\n- Impedance: 50Ω Diff\n- Stackup: 12-Layer', 
            fontsize=10, bbox=dict(facecolor='white', alpha=0.8))

    # Save to SVG string
    buf = BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    plt.close(fig)
    return buf.getvalue().decode('utf-8')

def generate_power_distribution_schematic():
    """Generate SVG schematic for power distribution"""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_axis_off()
    
    # Main Power Rail
    ax.plot([1, 13], [6, 6], 'r-', linewidth=3)
    ax.text(0.5, 6, '12V Bus', fontsize=12, va='center', weight='bold')
    
    # Regulators (Buck Converters)
    # 3.3V
    reg1 = patches.Rectangle((2, 3), 2, 2, linewidth=2, edgecolor='blue', facecolor='#E6E6FF')
    ax.add_patch(reg1)
    ax.text(3, 4, 'Buck\n3.3V', fontsize=10, ha='center', va='center')
    
    # 1.8V
    reg2 = patches.Rectangle((6, 3), 2, 2, linewidth=2, edgecolor='blue', facecolor='#E6E6FF')
    ax.add_patch(reg2)
    ax.text(7, 4, 'Buck\n1.8V', fontsize=10, ha='center', va='center')
    
    # 1.0V
    reg3 = patches.Rectangle((10, 3), 2, 2, linewidth=2, edgecolor='blue', facecolor='#E6E6FF')
    ax.add_patch(reg3)
    ax.text(11, 4, 'Buck\n1.0V', fontsize=10, ha='center', va='center')
    
    # Connections from 12V
    ax.plot([3, 3], [6, 5], 'k-', linewidth=1)
    ax.plot([7, 7], [6, 5], 'k-', linewidth=1)
    ax.plot([11, 11], [6, 5], 'k-', linewidth=1)
    
    # Outputs lines
    ax.plot([3, 3], [3, 1], 'g-', linewidth=2)
    ax.plot([7, 7], [3, 1], 'g-', linewidth=2)
    ax.plot([11, 11], [3, 1], 'g-', linewidth=2)
    
    # Filters (LDOs inline for clean power)
    ldo1 = patches.Rectangle((2.5, 1.5), 1, 1, linewidth=1, edgecolor='green', facecolor='#ccffcc')
    ax.add_patch(ldo1)
    ax.text(3, 2, 'LDO\nLow Noise', fontsize=7, ha='center', va='center')
    
    ldo2 = patches.Rectangle((6.5, 1.5), 1, 1, linewidth=1, edgecolor='green', facecolor='#ccffcc')
    ax.add_patch(ldo2)
    ax.text(7, 2, 'LDO\nLow Noise', fontsize=7, ha='center', va='center')

    # Loads
    load1 = patches.Rectangle((2, -1), 2, 1.5, linewidth=1, edgecolor='black', facecolor='#EEEEEE')
    ax.add_patch(load1)
    ax.text(3, -0.25, 'Analog\n(Drivers)', fontsize=9, ha='center')
    
    load2 = patches.Rectangle((6, -1), 2, 1.5, linewidth=1, edgecolor='black', facecolor='#EEEEEE')
    ax.add_patch(load2)
    ax.text(7, -0.25, 'Digital I/O\n(SerDes)', fontsize=9, ha='center')
    
    load3 = patches.Rectangle((10, -1), 2, 1.5, linewidth=1, edgecolor='black', facecolor='#EEEEEE')
    ax.add_patch(load3)
    ax.text(11, -0.25, 'Core Logic\n(FPGA/DSP)', fontsize=9, ha='center')

    # Decoupling Caps (Symbolic)
    for x in [3.5, 7.5, 11.5]:
        ax.plot([x, x], [0.8, 0.2], 'k-', linewidth=1)
        ax.plot([x-0.2, x+0.2], [0.2, 0.2], 'k-', linewidth=1)
        ax.plot([x-0.2, x+0.2], [0.1, 0.1], 'k-', linewidth=1)
        ax.text(x+0.3, 0.15, '10μF', fontsize=7)

    ax.set_title('Densified Power Distribution Network (PDN)', fontsize=16, weight='bold', pad=20)
    
    # Save to SVG string
    buf = BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    plt.close(fig)
    return buf.getvalue().decode('utf-8')
