#!/usr/bin/env python3
"""Generate KiCad 8.0 schematic for TFLN_AI_NODE_X2.

Board layout (from image reference):
- 2x AI Compute Units (TFLN Photonic Enabled) - center
- 2x Integrated Optical Engines - center  
- 2x TFLN Modulators - center
- 4x VRM Arrays (24-Phase DrMOS) - corners around compute units
- 8x PCIe Gen6 x16 Expansion Slots - top and sides
- 4x DDR5 DIMM slots
- 4x NVMe M.2 U.3 Storage - left and right edges
- Power delivery system (V_core 0.8V, 1000A+)
- Bypass/decoupling capacitor arrays
"""

import uuid

def uid():
    return str(uuid.uuid4())

def symbol_instance(ref, value, lib_symbol, x, y, unit=1, mirror=False):
    """Generate a symbol instance in schematic."""
    mir = ' (mirror y)' if mirror else ''
    s = f'  (symbol\n'
    s += f'    (lib_id "TFLN_AI_NODE_X2:{lib_symbol}")\n'
    s += f'    (at {x} {y} 0)\n'
    s += f'    (unit {unit})\n'
    s += f'    (exclude_from_sim no)\n'
    s += f'    (in_bom yes)\n'
    s += f'    (on_board yes)\n'
    s += f'    (dnp no)\n'
    s += f'    (uuid "{uid()}")\n'
    s += f'    (property "Reference" "{ref}" (at {x} {y-4} 0) (effects (font (size 1.27 1.27))))\n'
    s += f'    (property "Value" "{value}" (at {x} {y-6} 0) (effects (font (size 1.27 1.27))))\n'
    s += f'    (property "Footprint" "TFLN_AI_NODE_X2:{lib_symbol.replace("AI_Compute_Unit","BGA256_0.8mm").replace("TFLN_Photonic_Engine","TFLN_Photonic_Hybrid").replace("VRM_DrMOS_24Phase","VRM_DrMOS_Array").replace("DDR5_DIMM_288","DDR5_DIMM_288pin").replace("PCIe_x16_Gen6","PCIe_x16_Slot").replace("NVMe_M2_Connector","NVMe_M2_Socket").replace("Power_Input_Connector","Power_Input_Connector").replace("Bypass_Cap_Array","")}" (at {x} {y-8} 0) (effects (font (size 1.27 1.27)) hide))\n'
    s += f'    (property "Datasheet" "" (at {x} {y} 0) (effects (font (size 1.27 1.27)) hide))\n'
    s += f'  )\n'
    return s

def wire(x1, y1, x2, y2):
    return f'  (wire (pts (xy {x1} {y1}) (xy {x2} {y2})) (stroke (width 0) (type default)) (uuid "{uid()}"))\n'

def bus(x1, y1, x2, y2):
    return f'  (bus (pts (xy {x1} {y1}) (xy {x2} {y2})) (stroke (width 0) (type default)) (uuid "{uid()}"))\n'

def net_label(name, x, y, angle=0):
    return f'  (label "{name}" (at {x} {y} {angle}) (effects (font (size 1.27 1.27))) (uuid "{uid()}"))\n'

def global_label(name, x, y, angle=0, shape="bidirectional"):
    return f'  (global_label "{name}" (shape {shape}) (at {x} {y} {angle}) (effects (font (size 1.27 1.27))) (uuid "{uid()}"))\n'

def power_port(name, x, y, ptype="power_in"):
    return f'  (power_port "{name}" (at {x} {y} 0) (effects (font (size 1.27 1.27))) (uuid "{uid()}"))\n'

def text_note(text, x, y, size=2.0):
    return f'  (text "{text}" (at {x} {y} 0) (effects (font (size {size} {size})) (justify left)) (uuid "{uid()}"))\n'

def main():
    sch = '(kicad_sch\n'
    sch += '  (version 20231120)\n'
    sch += '  (generator "TFLN_AI_NODE_X2_gen")\n'
    sch += '  (generator_version "8.0")\n'
    sch += '  (uuid "2bfb8e5e-91ef-4c9c-b4fa-e7a1bb0c3608")\n'
    sch += '  (paper "A0")\n'
    sch += '  (title_block\n'
    sch += '    (title "TFLN_AI_NODE_X2 - Photonic-Integrated AI Compute Node")\n'
    sch += '    (date "2026-04-12")\n'
    sch += '    (rev "1.0")\n'
    sch += '    (company "LightRail AI / LightOS")\n'
    sch += '    (comment 1 "SCHEMATIC: TFLN Photonic-Integrated AI Compute Node")\n'
    sch += '    (comment 2 "Based on MidBoard - with 8x PCIe 5.0 Slots")\n'
    sch += '    (comment 3 "22-Layer PCB with DDR5, PCIe Gen6, TFLN RF")\n'
    sch += '  )\n\n'

    # Library symbols reference
    sch += '  (lib_symbols\n'
    # Read the generated symbol library and embed it
    with open("symbols/TFLN_AI_NODE_X2.kicad_sym", "r") as f:
        content = f.read()
    # Extract individual symbols from library
    import re
    # Find all top-level symbol definitions
    symbols = re.findall(r'  \(symbol "([^"]+)".*?\n  \)', content, re.DOTALL)
    symbol_blocks = re.findall(r'(  \(symbol "[^"]+?".*?\n  \))', content, re.DOTALL)
    for block in symbol_blocks:
        sch += '  ' + block + '\n'
    sch += '  )\n\n'

    # ==========================================
    # TITLE AND SECTION ANNOTATIONS
    # ==========================================
    sch += text_note("TFLN_AI_NODE_X2 - Photonic-Integrated AI Compute Node", 20, 20, 4)
    sch += text_note("AI Compute Section", 40, 60, 3)
    sch += text_note("Power Delivery Section", 40, 300, 3)
    sch += text_note("PCIe Expansion Section", 400, 60, 3)
    sch += text_note("Memory Section (DDR5)", 40, 500, 3)
    sch += text_note("Storage Section (NVMe)", 400, 500, 3)

    # ==========================================
    # AI COMPUTE UNITS (x2)
    # ==========================================
    sch += symbol_instance("U1", "AI_Compute_Unit_1", "AI_Compute_Unit", 120, 150)
    sch += symbol_instance("U2", "AI_Compute_Unit_2", "AI_Compute_Unit", 280, 150)

    # ==========================================
    # TFLN PHOTONIC ENGINES (x2)
    # ==========================================
    sch += symbol_instance("U3", "TFLN_Photonic_Engine_1", "TFLN_Photonic_Engine", 120, 250)
    sch += symbol_instance("U4", "TFLN_Photonic_Engine_2", "TFLN_Photonic_Engine", 280, 250)

    # ==========================================
    # VRM ARRAYS (x4) - 24-Phase DrMOS each
    # ==========================================
    sch += symbol_instance("U5", "VRM_Array_Top_Left", "VRM_DrMOS_24Phase", 60, 340)
    sch += symbol_instance("U6", "VRM_Array_Top_Right", "VRM_DrMOS_24Phase", 200, 340)
    sch += symbol_instance("U7", "VRM_Array_Bot_Left", "VRM_DrMOS_24Phase", 340, 340)
    sch += symbol_instance("U8", "VRM_Array_Bot_Right", "VRM_DrMOS_24Phase", 480, 340)

    # ==========================================
    # PCIe Gen6 x16 EXPANSION SLOTS (x8)
    # ==========================================
    for i in range(4):
        sch += symbol_instance(f"J{i+1}", f"PCIe_Slot_Top_{i+1}", "PCIe_x16_Gen6", 420 + i * 60, 120)
    for i in range(4):
        sch += symbol_instance(f"J{i+5}", f"PCIe_Slot_Bot_{i+1}", "PCIe_x16_Gen6", 420 + i * 60, 250)

    # ==========================================
    # DDR5 DIMM SLOTS (x4)
    # ==========================================
    for i in range(4):
        sch += symbol_instance(f"J{i+9}", f"DDR5_DIMM_{i+1}", "DDR5_DIMM_288", 80 + i * 80, 550)

    # ==========================================
    # NVMe M.2 STORAGE (x4)
    # ==========================================
    for i in range(2):
        sch += symbol_instance(f"J{i+13}", f"NVMe_Storage_Left_{i+1}", "NVMe_M2_Connector", 440, 550 + i * 60)
    for i in range(2):
        sch += symbol_instance(f"J{i+15}", f"NVMe_Storage_Right_{i+1}", "NVMe_M2_Connector", 560, 550 + i * 60)

    # ==========================================
    # POWER INPUT CONNECTORS (x2)
    # ==========================================
    sch += symbol_instance("J17", "Power_Input_1", "Power_Input_Connector", 60, 420)
    sch += symbol_instance("J18", "Power_Input_2", "Power_Input_Connector", 200, 420)

    # ==========================================
    # BYPASS CAPACITOR ARRAYS (x16)
    # ==========================================
    cap_positions = [
        (100, 100), (140, 100), (260, 100), (300, 100),  # Near AI units
        (100, 200), (140, 200), (260, 200), (300, 200),  # Near TFLN
        (40, 320), (80, 320), (180, 320), (220, 320),    # Near VRM
        (320, 320), (360, 320), (460, 320), (500, 320),  # Near VRM
    ]
    for idx, (cx, cy) in enumerate(cap_positions):
        sch += symbol_instance(f"C{idx+1}", f"100nF/10uF", "Bypass_Cap_Array", cx, cy)

    # ==========================================
    # GLOBAL NET LABELS - Power Rails
    # ==========================================
    power_labels = [
        ("V_CORE_0V8", 60, 360, 0),
        ("V_CORE_0V8", 200, 360, 0),
        ("V_CORE_0V8", 340, 360, 0),
        ("V_CORE_0V8", 480, 360, 0),
        ("VIN_12V", 60, 400, 0),
        ("VIN_12V", 200, 400, 0),
        ("GND", 60, 440, 0),
        ("GND", 200, 440, 0),
    ]
    for name, x, y, angle in power_labels:
        sch += global_label(name, x, y, angle, "power_in" if "VIN" in name or "GND" in name else "bidirectional")

    # ==========================================
    # GLOBAL NET LABELS - High-Speed Signals  
    # ==========================================
    # SerDes connections between AI Units and TFLN
    for i in range(16):
        sch += global_label(f"SERDES_U1_TX{i}_P", 88, 150 - 44 + i * 5.54, 180)
        sch += global_label(f"SERDES_U1_TX{i}_N", 88, 150 - 44 + i * 5.54 + 2.54, 180)

    # PCIe lanes
    for i in range(8):
        sch += global_label(f"PCIE_LANE{i}_TX_P", 420, 100 + i * 5, 180)
        sch += global_label(f"PCIE_LANE{i}_TX_N", 420, 100 + i * 5 + 2, 180)

    # DDR5 bus
    for i in range(4):
        sch += global_label(f"DDR5_CH{i}_DQ[0:63]", 80 + i * 80, 530, 90)

    # TFLN RF differential pairs
    for i in range(8):
        sch += global_label(f"TFLN_RF{i}_P", 93, 250 - 24 + i * 6.04, 180)
        sch += global_label(f"TFLN_RF{i}_N", 93, 250 - 24 + i * 6.04 + 2.54, 180)

    # ==========================================
    # WIRES - Power distribution
    # ==========================================
    # VRM to AI Unit power connections
    sch += wire(82, 340, 100, 340)  # VRM1 -> U1 VCORE
    sch += wire(222, 340, 240, 340)  # VRM2 -> U2 VCORE
    # Power input to VRM
    sch += wire(60, 420, 60, 360)   # Power1 -> VRM1
    sch += wire(200, 420, 200, 360) # Power2 -> VRM2

    # SerDes connections AI <-> TFLN
    for i in range(8):
        y1 = 150 - 44 + i * 5.54
        y2 = 250 - 24 + i * 6.04
        sch += wire(152, y1, 152, y2)  # U1 SerDes -> TFLN1

    sch += '\n'
    sch += ')\n'

    with open("TFLN_AI_NODE_X2.kicad_sch", "w") as f:
        f.write(sch)
    print("Schematic generated: TFLN_AI_NODE_X2.kicad_sch")


if __name__ == "__main__":
    main()
