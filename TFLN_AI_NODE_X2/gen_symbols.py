#!/usr/bin/env python3
"""Generate KiCad 8.0 symbol library for TFLN_AI_NODE_X2."""

import math

def pin_line(name, number, x, y, length=2.54, direction="R", etype="passive"):
    """Generate a KiCad symbol pin S-expression."""
    dir_map = {"R": 0, "L": 180, "U": 90, "D": 270}
    angle = dir_map.get(direction, 0)
    return f'    (pin {etype} line (at {x:.2f} {y:.2f} {angle}) (length {length:.2f}) (name "{name}" (effects (font (size 1.0 1.0)))) (number "{number}" (effects (font (size 1.0 1.0)))))\n'


def gen_ai_compute_unit():
    """AI Compute Unit with BGA pads - 256-pin simplified representation."""
    s = '  (symbol "AI_Compute_Unit" (in_bom yes) (on_board yes)\n'
    s += '    (property "Reference" "U" (at 0 52 0) (effects (font (size 1.27 1.27))))\n'
    s += '    (property "Value" "AI_Compute_Unit" (at 0 50 0) (effects (font (size 1.27 1.27))))\n'
    s += '    (property "Footprint" "TFLN_AI_NODE_X2:BGA256_0.8mm" (at 0 -52 0) (effects (font (size 1.27 1.27)) hide))\n'
    s += '    (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))\n'
    s += '    (property "Description" "AI Compute Unit with TFLN Photonic-Enabled BGA256" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))\n'
    s += '    (symbol "AI_Compute_Unit_0_0"\n'
    # Body rectangle
    s += '      (rectangle (start -30 48) (end 30 -48) (stroke (width 0.254) (type default)) (fill (type background)))\n'
    s += '      (text "AI COMPUTE\\nUNIT" (at 0 0 0) (effects (font (size 3 3) bold)))\n'

    pin_num = 1
    # Left side: SerDes TX (16 diff pairs = 32 pins)
    y = 44
    for i in range(16):
        s += pin_line(f"SERDES_TX{i}_P", str(pin_num), -32.54, y, direction="R", etype="output")
        pin_num += 1; y -= 2.54
        s += pin_line(f"SERDES_TX{i}_N", str(pin_num), -32.54, y, direction="R", etype="output")
        pin_num += 1; y -= 3.0

    # Right side: SerDes RX (16 diff pairs = 32 pins)
    y = 44
    for i in range(16):
        s += pin_line(f"SERDES_RX{i}_P", str(pin_num), 32.54, y, direction="L", etype="input")
        pin_num += 1; y -= 2.54
        s += pin_line(f"SERDES_RX{i}_N", str(pin_num), 32.54, y, direction="L", etype="input")
        pin_num += 1; y -= 3.0

    # Top: DDR5 interface (64 pins)
    x = -28
    for i in range(32):
        s += pin_line(f"DDR5_DQ{i}", str(pin_num), x, 50.54, direction="D", etype="bidirectional")
        pin_num += 1; x += 1.8

    x = -28
    for i in range(32):
        s += pin_line(f"DDR5_DQ{i+32}", str(pin_num), x, -50.54, direction="U", etype="bidirectional")
        pin_num += 1; x += 1.8

    # PCIe lanes (bottom, 32 pins)
    x = -20
    for i in range(16):
        s += pin_line(f"PCIE_TX{i}", str(pin_num), x, -50.54, direction="U", etype="output")
        pin_num += 1; x += 2.54

    # Power pins
    for i in range(16):
        s += pin_line(f"VCORE", str(pin_num), -32.54, -44 + i*2.54, direction="R", etype="power_in")
        pin_num += 1

    # Ground pins (central ball array)
    for i in range(48):
        s += pin_line(f"GND", str(pin_num), 32.54, -44 + i*1.8, direction="L", etype="power_in")
        pin_num += 1

    s += '    )\n'
    s += '  )\n'
    return s


def gen_tfln_photonic_engine():
    """TFLN Photonic Engine with RF and optical keep-out."""
    s = '  (symbol "TFLN_Photonic_Engine" (in_bom yes) (on_board yes)\n'
    s += '    (property "Reference" "U" (at 0 32 0) (effects (font (size 1.27 1.27))))\n'
    s += '    (property "Value" "TFLN_Photonic_Engine" (at 0 30 0) (effects (font (size 1.27 1.27))))\n'
    s += '    (property "Footprint" "TFLN_AI_NODE_X2:TFLN_Photonic_Hybrid" (at 0 -32 0) (effects (font (size 1.27 1.27)) hide))\n'
    s += '    (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))\n'
    s += '    (property "Description" "TFLN Photonic Engine with Integrated Optical Engine and Modulators" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))\n'
    s += '    (symbol "TFLN_Photonic_Engine_0_0"\n'
    s += '      (rectangle (start -25 28) (end 25 -28) (stroke (width 0.254) (type default)) (fill (type background)))\n'
    s += '      (text "TFLN PHOTONIC\\nENGINE" (at 0 5 0) (effects (font (size 2.5 2.5) bold)))\n'
    s += '      (text "Integrated Optical\\nEngine" (at 0 -5 0) (effects (font (size 1.5 1.5))))\n'
    s += '      (text "TFLN Modulators" (at 0 -12 0) (effects (font (size 1.5 1.5))))\n'

    pin_num = 1
    # Left: RF inputs (differential, 8 pairs)
    y = 24
    for i in range(8):
        s += pin_line(f"RF_IN{i}_P", str(pin_num), -27.54, y, direction="R", etype="input")
        pin_num += 1; y -= 2.54
        s += pin_line(f"RF_IN{i}_N", str(pin_num), -27.54, y, direction="R", etype="input")
        pin_num += 1; y -= 3.5

    # Right: RF outputs (differential, 8 pairs)
    y = 24
    for i in range(8):
        s += pin_line(f"RF_OUT{i}_P", str(pin_num), 27.54, y, direction="L", etype="output")
        pin_num += 1; y -= 2.54
        s += pin_line(f"RF_OUT{i}_N", str(pin_num), 27.54, y, direction="L", etype="output")
        pin_num += 1; y -= 3.5

    # Top: control & bias
    x = -20
    for i in range(8):
        s += pin_line(f"BIAS{i}", str(pin_num), x, 30.54, direction="D", etype="input")
        pin_num += 1; x += 5.08

    # Bottom: power & ground
    x = -15
    for i in range(4):
        s += pin_line(f"VCC_TFLN", str(pin_num), x, -30.54, direction="U", etype="power_in")
        pin_num += 1; x += 5.08
    x = -15
    for i in range(4):
        s += pin_line(f"GND", str(pin_num), x + 2.54, -30.54, direction="U", etype="power_in")
        pin_num += 1; x += 5.08

    # Optical interface marker (no electrical pin, just annotation)
    s += '      (text "OPTICAL FAU\\nINTERFACE" (at 0 -22 0) (effects (font (size 1.2 1.2) italic)))\n'

    s += '    )\n'
    s += '  )\n'
    return s


def gen_vrm_drmos():
    """VRM DrMOS array (24-phase)."""
    s = '  (symbol "VRM_DrMOS_24Phase" (in_bom yes) (on_board yes)\n'
    s += '    (property "Reference" "U" (at 0 22 0) (effects (font (size 1.27 1.27))))\n'
    s += '    (property "Value" "VRM_DrMOS_24Phase" (at 0 20 0) (effects (font (size 1.27 1.27))))\n'
    s += '    (property "Footprint" "TFLN_AI_NODE_X2:VRM_DrMOS_Array" (at 0 -22 0) (effects (font (size 1.27 1.27)) hide))\n'
    s += '    (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))\n'
    s += '    (property "Description" "24-Phase VRM DrMOS Array for V_core 0.8V / 1000A+" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))\n'
    s += '    (symbol "VRM_DrMOS_24Phase_0_0"\n'
    s += '      (rectangle (start -20 18) (end 20 -18) (stroke (width 0.254) (type default)) (fill (type background)))\n'
    s += '      (text "VRM ARRAY\\n24-Phase DrMOS\\n0.8V / 1000A+" (at 0 0 0) (effects (font (size 2 2) bold)))\n'

    pin_num = 1
    # VIN (12V input)
    y = 14
    for i in range(6):
        s += pin_line(f"VIN_12V", str(pin_num), -22.54, y, direction="R", etype="power_in")
        pin_num += 1; y -= 5.08

    # VOUT (0.8V output phases)
    y = 14
    for i in range(24):
        s += pin_line(f"VOUT_PH{i}", str(pin_num), 22.54, y - (i % 12) * 2.54, direction="L", etype="power_out")
        pin_num += 1

    # PWM inputs
    x = -15
    for i in range(12):
        s += pin_line(f"PWM{i}", str(pin_num), x, 20.54, direction="D", etype="input")
        pin_num += 1; x += 2.54

    # GND
    x = -15
    for i in range(8):
        s += pin_line(f"GND", str(pin_num), x, -20.54, direction="U", etype="power_in")
        pin_num += 1; x += 3.81

    s += '    )\n'
    s += '  )\n'
    return s


def gen_ddr5_dimm():
    """DDR5 DIMM 288-pin connector."""
    s = '  (symbol "DDR5_DIMM_288" (in_bom yes) (on_board yes)\n'
    s += '    (property "Reference" "J" (at 0 78 0) (effects (font (size 1.27 1.27))))\n'
    s += '    (property "Value" "DDR5_DIMM_288" (at 0 76 0) (effects (font (size 1.27 1.27))))\n'
    s += '    (property "Footprint" "TFLN_AI_NODE_X2:DDR5_DIMM_288pin" (at 0 -78 0) (effects (font (size 1.27 1.27)) hide))\n'
    s += '    (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))\n'
    s += '    (property "Description" "DDR5 288-pin Vertical DIMM Socket" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))\n'
    s += '    (symbol "DDR5_DIMM_288_0_0"\n'
    s += '      (rectangle (start -8 74) (end 8 -74) (stroke (width 0.254) (type default)) (fill (type background)))\n'
    s += '      (text "DDR5\\nDIMM\\n288-pin" (at 0 0 0) (effects (font (size 2 2) bold)))\n'

    # Generate 144 pins on each side
    pin_num = 1
    y = 72
    for i in range(144):
        s += pin_line(f"P{pin_num}", str(pin_num), -10.54, y, direction="R", etype="passive")
        pin_num += 1
        y -= 1.0

    y = 72
    for i in range(144):
        s += pin_line(f"P{pin_num}", str(pin_num), 10.54, y, direction="L", etype="passive")
        pin_num += 1
        y -= 1.0

    s += '    )\n'
    s += '  )\n'
    return s


def gen_pcie_x16_slot():
    """PCIe Gen6 x16 slot."""
    s = '  (symbol "PCIe_x16_Gen6" (in_bom yes) (on_board yes)\n'
    s += '    (property "Reference" "J" (at 0 52 0) (effects (font (size 1.27 1.27))))\n'
    s += '    (property "Value" "PCIe_x16_Gen6" (at 0 50 0) (effects (font (size 1.27 1.27))))\n'
    s += '    (property "Footprint" "TFLN_AI_NODE_X2:PCIe_x16_Slot" (at 0 -52 0) (effects (font (size 1.27 1.27)) hide))\n'
    s += '    (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))\n'
    s += '    (property "Description" "PCIe Gen6 x16 Card Edge Expansion Slot" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))\n'
    s += '    (symbol "PCIe_x16_Gen6_0_0"\n'
    s += '      (rectangle (start -12 48) (end 12 -48) (stroke (width 0.254) (type default)) (fill (type background)))\n'
    s += '      (text "PCIe Gen6\\nx16 Slot" (at 0 0 0) (effects (font (size 2 2) bold)))\n'

    pin_num = 1
    # 82-pin connector A side
    y = 46
    for i in range(41):
        nm = f"A{i+1}"
        s += pin_line(nm, str(pin_num), -14.54, y, direction="R", etype="passive")
        pin_num += 1; y -= 2.3

    # 82-pin connector B side
    y = 46
    for i in range(41):
        nm = f"B{i+1}"
        s += pin_line(nm, str(pin_num), 14.54, y, direction="L", etype="passive")
        pin_num += 1; y -= 2.3

    s += '    )\n'
    s += '  )\n'
    return s


def gen_nvme_m2():
    """NVMe M.2 connector."""
    s = '  (symbol "NVMe_M2_Connector" (in_bom yes) (on_board yes)\n'
    s += '    (property "Reference" "J" (at 0 22 0) (effects (font (size 1.27 1.27))))\n'
    s += '    (property "Value" "NVMe_M2_Connector" (at 0 20 0) (effects (font (size 1.27 1.27))))\n'
    s += '    (property "Footprint" "TFLN_AI_NODE_X2:NVMe_M2_Socket" (at 0 -22 0) (effects (font (size 1.27 1.27)) hide))\n'
    s += '    (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))\n'
    s += '    (property "Description" "NVMe M.2 2280 Key-M Socket for 4x M.2 U.3 Storage" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))\n'
    s += '    (symbol "NVMe_M2_Connector_0_0"\n'
    s += '      (rectangle (start -8 18) (end 8 -18) (stroke (width 0.254) (type default)) (fill (type background)))\n'
    s += '      (text "NVMe\\nM.2" (at 0 0 0) (effects (font (size 2 2) bold)))\n'

    pin_num = 1
    y = 16
    for i in range(34):
        s += pin_line(f"M{i+1}", str(pin_num), -10.54, y, direction="R", etype="passive")
        pin_num += 1; y -= 1.0

    y = 16
    for i in range(33):
        s += pin_line(f"M{i+35}", str(pin_num), 10.54, y, direction="L", etype="passive")
        pin_num += 1; y -= 1.0

    s += '    )\n'
    s += '  )\n'
    return s


def gen_power_connector():
    """High-current power input connector."""
    s = '  (symbol "Power_Input_Connector" (in_bom yes) (on_board yes)\n'
    s += '    (property "Reference" "J" (at 0 12 0) (effects (font (size 1.27 1.27))))\n'
    s += '    (property "Value" "Power_Input_12V" (at 0 10 0) (effects (font (size 1.27 1.27))))\n'
    s += '    (property "Footprint" "TFLN_AI_NODE_X2:Power_Input_Connector" (at 0 -12 0) (effects (font (size 1.27 1.27)) hide))\n'
    s += '    (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))\n'
    s += '    (property "Description" "12V High-Current Power Input (1000A+ capable)" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))\n'
    s += '    (symbol "Power_Input_Connector_0_0"\n'
    s += '      (rectangle (start -6 8) (end 6 -8) (stroke (width 0.254) (type default)) (fill (type background)))\n'
    s += '      (text "12V\\nPOWER" (at 0 0 0) (effects (font (size 2 2) bold)))\n'

    pin_num = 1
    for i in range(8):
        s += pin_line(f"VIN_12V", str(pin_num), -8.54, 6 - i * 1.5, direction="R", etype="power_in")
        pin_num += 1
    for i in range(8):
        s += pin_line(f"GND", str(pin_num), 8.54, 6 - i * 1.5, direction="L", etype="power_in")
        pin_num += 1

    s += '    )\n'
    s += '  )\n'
    return s


def gen_bypass_cap():
    """Bypass/Decoupling capacitor."""
    s = '  (symbol "Bypass_Cap_Array" (in_bom yes) (on_board yes)\n'
    s += '    (property "Reference" "C" (at 0 5 0) (effects (font (size 1.27 1.27))))\n'
    s += '    (property "Value" "100nF/10uF" (at 0 -5 0) (effects (font (size 1.27 1.27))))\n'
    s += '    (property "Footprint" "Capacitor_SMD:C_0402_1005Metric" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))\n'
    s += '    (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))\n'
    s += '    (property "Description" "Bypass/Decoupling Capacitor Array" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))\n'
    s += '    (symbol "Bypass_Cap_Array_0_0"\n'
    s += '      (polyline (pts (xy -1 1) (xy 1 1)) (stroke (width 0.254) (type default)) (fill (type none)))\n'
    s += '      (polyline (pts (xy -1 -0.5) (xy 1 -0.5)) (stroke (width 0.254) (type default)) (fill (type none)))\n'
    s += pin_line("VCC", "1", 0, 3.81, direction="D", etype="passive")
    s += pin_line("GND", "2", 0, -3.81, direction="U", etype="passive")
    s += '    )\n'
    s += '  )\n'
    return s


def main():
    header = '(kicad_symbol_lib\n  (version 20231120)\n  (generator "TFLN_AI_NODE_X2_gen")\n  (generator_version "8.0")\n'
    footer = ')\n'

    symbols = header
    symbols += gen_ai_compute_unit()
    symbols += gen_tfln_photonic_engine()
    symbols += gen_vrm_drmos()
    symbols += gen_ddr5_dimm()
    symbols += gen_pcie_x16_slot()
    symbols += gen_nvme_m2()
    symbols += gen_power_connector()
    symbols += gen_bypass_cap()
    symbols += footer

    with open("symbols/TFLN_AI_NODE_X2.kicad_sym", "w") as f:
        f.write(symbols)
    print("Symbol library generated: symbols/TFLN_AI_NODE_X2.kicad_sym")


if __name__ == "__main__":
    main()
