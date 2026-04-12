#!/usr/bin/env python3
"""Generate KiCad 8.0 footprint library for TFLN_AI_NODE_X2."""

import math
import os

OUTDIR = "footprints.pretty"


def bga256_08mm():
    """BGA256 with 0.8mm pitch - AI Compute Unit.
    Central pins -> GND plane, outer pins -> V_core and high-speed SerDes."""
    pitch = 0.8
    rows = 16
    cols = 16
    pad_dia = 0.4
    mask_dia = 0.45
    paste_dia = 0.35

    row_letters = "ABCDEFGHJKLMNPRT"  # Skip I, O, Q, S per BGA convention

    s = f'(footprint "BGA256_0.8mm"\n'
    s += '  (version 20240108)\n'
    s += '  (generator "TFLN_gen")\n'
    s += '  (generator_version "8.0")\n'
    s += '  (layer "F.Cu")\n'
    s += '  (descr "BGA-256, 0.8mm pitch, 16x16 array, AI Compute Unit")\n'
    s += '  (tags "BGA 256 0.8mm AI")\n'
    s += f'  (attr smd)\n'

    # Courtyard
    half = (rows * pitch) / 2 + 1.0
    s += f'  (fp_rect (start {-half:.3f} {-half:.3f}) (end {half:.3f} {half:.3f}) (stroke (width 0.05) (type default)) (layer "F.CrtYd"))\n'

    # Silkscreen outline
    silk_half = half - 0.2
    s += f'  (fp_rect (start {-silk_half:.3f} {-silk_half:.3f}) (end {silk_half:.3f} {silk_half:.3f}) (stroke (width 0.12) (type default)) (layer "F.SilkS"))\n'

    # Pin 1 marker
    s += f'  (fp_circle (center {-(rows-1)*pitch/2 - 0.6:.3f} {-(cols-1)*pitch/2 - 0.6:.3f}) (end {-(rows-1)*pitch/2 - 0.3:.3f} {-(cols-1)*pitch/2 - 0.6:.3f}) (stroke (width 0.1) (type solid)) (fill solid) (layer "F.SilkS"))\n'

    # Fab layer text
    s += f'  (fp_text reference "REF**" (at 0 {-half - 1:.3f}) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))\n'
    s += f'  (fp_text value "BGA256_0.8mm" (at 0 {half + 1:.3f}) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))\n'
    s += f'  (fp_text user "${{REFERENCE}}" (at 0 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))\n'

    # Generate pads
    pad_num = 0
    for r in range(rows):
        for c in range(cols):
            pad_num += 1
            x = (c - (cols - 1) / 2.0) * pitch
            y = (r - (rows - 1) / 2.0) * pitch
            name = f"{row_letters[r]}{c+1}"

            # Central 8x8 = GND, next ring = V_core, outer = signal
            is_center = (4 <= r <= 11) and (4 <= c <= 11)
            is_mid = (2 <= r <= 13) and (2 <= c <= 13) and not is_center

            s += f'  (pad "{name}" smd circle (at {x:.3f} {y:.3f}) (size {pad_dia} {pad_dia}) '
            s += f'(layers "F.Cu" "F.Paste" "F.Mask") '
            s += f'(solder_mask_margin 0.05) (solder_paste_margin -0.025) '

            if is_center:
                s += f'(net 0 "") '  # GND - assigned in PCB
            s += f'(zone_connect 1))\n'

    s += ')\n'

    with open(os.path.join(OUTDIR, "BGA256_0.8mm.kicad_mod"), "w") as f:
        f.write(s)
    print(f"  BGA256_0.8mm.kicad_mod")


def tfln_photonic_hybrid():
    """TFLN Photonic Engine hybrid footprint with RF SMT pads and optical keep-out."""
    s = '(footprint "TFLN_Photonic_Hybrid"\n'
    s += '  (version 20240108)\n'
    s += '  (generator "TFLN_gen")\n'
    s += '  (generator_version "8.0")\n'
    s += '  (layer "F.Cu")\n'
    s += '  (descr "TFLN Photonic Engine - Hybrid footprint with RF pads and optical fiber array keep-out")\n'
    s += '  (tags "TFLN photonic optical hybrid RF")\n'
    s += '  (attr smd)\n'

    # Overall courtyard: 30mm x 20mm
    s += '  (fp_rect (start -16 -11) (end 16 11) (stroke (width 0.05) (type default)) (layer "F.CrtYd"))\n'
    s += '  (fp_rect (start -15.5 -10.5) (end 15.5 10.5) (stroke (width 0.12) (type default)) (layer "F.SilkS"))\n'

    # Optical FAU keep-out area (silkscreen rectangle with hatching)
    s += '  (fp_rect (start -8 6) (end 8 10) (stroke (width 0.2) (type default)) (layer "F.SilkS"))\n'
    s += '  (fp_text user "OPTICAL FAU\\nKEEP-OUT ZONE" (at 0 8) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))\n'
    # Hatching lines for keep-out visual
    for i in range(-7, 8, 2):
        s += f'  (fp_line (start {i} 6) (end {i+2} 10) (stroke (width 0.1) (type default)) (layer "F.SilkS"))\n'

    # Keep-out on all copper layers for optical area
    s += '  (fp_rect (start -8 6) (end 8 10) (stroke (width 0.05) (type default)) (layer "Cmts.User"))\n'
    s += '  (fp_text user "NO COPPER - OPTICAL CAVITY" (at 0 8) (layer "Cmts.User") (effects (font (size 0.8 0.8) (thickness 0.1))))\n'

    # Reference and value
    s += '  (fp_text reference "REF**" (at 0 -12) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))\n'
    s += '  (fp_text value "TFLN_Photonic_Hybrid" (at 0 12) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))\n'

    # RF signal pads - left side (8 differential pairs, 50-ohm microstrip)
    pad_num = 1
    for i in range(8):
        y = -7 + i * 1.8
        # P pad
        s += f'  (pad "{pad_num}" smd rect (at -14.5 {y:.2f}) (size 1.2 0.4) (layers "F.Cu" "F.Paste" "F.Mask") (solder_mask_margin 0.05))\n'
        pad_num += 1
        # N pad
        s += f'  (pad "{pad_num}" smd rect (at -14.5 {y+0.65:.2f}) (size 1.2 0.4) (layers "F.Cu" "F.Paste" "F.Mask") (solder_mask_margin 0.05))\n'
        pad_num += 1

    # RF signal pads - right side (8 differential pairs)
    for i in range(8):
        y = -7 + i * 1.8
        s += f'  (pad "{pad_num}" smd rect (at 14.5 {y:.2f}) (size 1.2 0.4) (layers "F.Cu" "F.Paste" "F.Mask") (solder_mask_margin 0.05))\n'
        pad_num += 1
        s += f'  (pad "{pad_num}" smd rect (at 14.5 {y+0.65:.2f}) (size 1.2 0.4) (layers "F.Cu" "F.Paste" "F.Mask") (solder_mask_margin 0.05))\n'
        pad_num += 1

    # Bias/control pads - bottom
    for i in range(8):
        x = -7 + i * 2.0
        s += f'  (pad "{pad_num}" smd rect (at {x:.2f} -9.5) (size 0.6 1.0) (layers "F.Cu" "F.Paste" "F.Mask") (solder_mask_margin 0.05))\n'
        pad_num += 1

    # Power pads - bottom corners
    for i in range(4):
        x = -12 + i * 1.5
        s += f'  (pad "{pad_num}" smd rect (at {x:.2f} -9.5) (size 1.0 1.0) (layers "F.Cu" "F.Paste" "F.Mask") (solder_mask_margin 0.05))\n'
        pad_num += 1

    # GND pads
    for i in range(4):
        x = 7 + i * 1.5
        s += f'  (pad "{pad_num}" smd rect (at {x:.2f} -9.5) (size 1.0 1.0) (layers "F.Cu" "F.Paste" "F.Mask") (solder_mask_margin 0.05))\n'
        pad_num += 1

    # Thermal pad (large center ground)
    s += f'  (pad "{pad_num}" smd rect (at 0 0) (size 8 6) (layers "F.Cu" "F.Paste" "F.Mask") (solder_mask_margin 0.1) (zone_connect 1))\n'

    s += ')\n'

    with open(os.path.join(OUTDIR, "TFLN_Photonic_Hybrid.kicad_mod"), "w") as f:
        f.write(s)
    print(f"  TFLN_Photonic_Hybrid.kicad_mod")


def ddr5_dimm_288():
    """DDR5 288-pin vertical DIMM connector."""
    s = '(footprint "DDR5_DIMM_288pin"\n'
    s += '  (version 20240108)\n'
    s += '  (generator "TFLN_gen")\n'
    s += '  (generator_version "8.0")\n'
    s += '  (layer "F.Cu")\n'
    s += '  (descr "DDR5 288-pin Vertical DIMM Socket")\n'
    s += '  (tags "DDR5 DIMM 288 vertical")\n'
    s += '  (attr through_hole)\n'

    # DIMM slot is about 133.35mm long
    slot_len = 133.35
    slot_half = slot_len / 2.0

    s += f'  (fp_rect (start {-slot_half-2} -5) (end {slot_half+2} 12) (stroke (width 0.05) (type default)) (layer "F.CrtYd"))\n'
    s += f'  (fp_rect (start {-slot_half-1} -4) (end {slot_half+1} 11) (stroke (width 0.12) (type default)) (layer "F.SilkS"))\n'
    s += f'  (fp_text reference "REF**" (at 0 -6) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))\n'
    s += f'  (fp_text value "DDR5_DIMM_288pin" (at 0 13) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))\n'

    # Key notch
    s += f'  (fp_rect (start -1.5 -4) (end 1.5 2) (stroke (width 0.12) (type default)) (layer "F.SilkS"))\n'

    # 288 pins: 144 per side, 0.85mm pitch
    pitch = 0.85
    start_x = -(143 * pitch) / 2.0
    pad_num = 1

    # Side A (front)
    for i in range(144):
        x = start_x + i * pitch
        s += f'  (pad "{pad_num}" thru_hole circle (at {x:.3f} 0) (size 0.7 0.7) (drill 0.4) (layers "*.Cu" "*.Mask"))\n'
        pad_num += 1

    # Side B (back)
    for i in range(144):
        x = start_x + i * pitch
        s += f'  (pad "{pad_num}" thru_hole circle (at {x:.3f} 2.0) (size 0.7 0.7) (drill 0.4) (layers "*.Cu" "*.Mask"))\n'
        pad_num += 1

    # Mounting holes
    for xm in [-slot_half - 0.5, slot_half + 0.5]:
        s += f'  (pad "" thru_hole circle (at {xm:.3f} 1.0) (size 3.0 3.0) (drill 2.4) (layers "*.Cu" "*.Mask"))\n'

    s += ')\n'

    with open(os.path.join(OUTDIR, "DDR5_DIMM_288pin.kicad_mod"), "w") as f:
        f.write(s)
    print(f"  DDR5_DIMM_288pin.kicad_mod")


def vrm_drmos_array():
    """VRM DrMOS 24-phase array footprint."""
    s = '(footprint "VRM_DrMOS_Array"\n'
    s += '  (version 20240108)\n'
    s += '  (generator "TFLN_gen")\n'
    s += '  (generator_version "8.0")\n'
    s += '  (layer "F.Cu")\n'
    s += '  (descr "24-Phase VRM DrMOS Array with solid thermal reliefs")\n'
    s += '  (tags "VRM DrMOS 24-phase power")\n'
    s += '  (attr smd)\n'

    # Array layout: 2 rows of 12 DrMOS
    w = 60
    h = 15
    s += f'  (fp_rect (start {-w/2-1} {-h/2-1}) (end {w/2+1} {h/2+1}) (stroke (width 0.05) (type default)) (layer "F.CrtYd"))\n'
    s += f'  (fp_rect (start {-w/2} {-h/2}) (end {w/2} {h/2}) (stroke (width 0.12) (type default)) (layer "F.SilkS"))\n'
    s += f'  (fp_text reference "REF**" (at 0 {-h/2-2}) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))\n'
    s += f'  (fp_text value "VRM_DrMOS_Array" (at 0 {h/2+2}) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))\n'

    pad_num = 1
    # Row 1: 12 DrMOS units
    for i in range(12):
        x = -27.5 + i * 5.0
        # VIN pad (large)
        s += f'  (pad "{pad_num}" smd rect (at {x:.2f} -4) (size 3.0 2.0) (layers "F.Cu" "F.Paste" "F.Mask") (solder_mask_margin 0.05) (zone_connect 1))\n'
        pad_num += 1
        # VOUT pad (large, solid thermal relief)
        s += f'  (pad "{pad_num}" smd rect (at {x:.2f} -1) (size 3.0 2.0) (layers "F.Cu" "F.Paste" "F.Mask") (solder_mask_margin 0.05) (zone_connect 1))\n'
        pad_num += 1
        # PWM input
        s += f'  (pad "{pad_num}" smd rect (at {x:.2f} 2) (size 0.6 0.8) (layers "F.Cu" "F.Paste" "F.Mask"))\n'
        pad_num += 1

    # Row 2: 12 DrMOS units
    for i in range(12):
        x = -27.5 + i * 5.0
        s += f'  (pad "{pad_num}" smd rect (at {x:.2f} 4) (size 3.0 2.0) (layers "F.Cu" "F.Paste" "F.Mask") (solder_mask_margin 0.05) (zone_connect 1))\n'
        pad_num += 1
        s += f'  (pad "{pad_num}" smd rect (at {x:.2f} 7) (size 3.0 2.0) (layers "F.Cu" "F.Paste" "F.Mask") (solder_mask_margin 0.05) (zone_connect 1))\n'
        pad_num += 1
        s += f'  (pad "{pad_num}" smd rect (at {x:.2f} -6.5) (size 0.6 0.8) (layers "F.Cu" "F.Paste" "F.Mask"))\n'
        pad_num += 1

    # Large GND thermal pad
    s += f'  (pad "{pad_num}" smd rect (at 0 0) (size 55 3) (layers "F.Cu" "F.Paste" "F.Mask") (zone_connect 1))\n'

    s += ')\n'

    with open(os.path.join(OUTDIR, "VRM_DrMOS_Array.kicad_mod"), "w") as f:
        f.write(s)
    print(f"  VRM_DrMOS_Array.kicad_mod")


def pcie_x16_slot():
    """PCIe Gen6 x16 card-edge slot."""
    s = '(footprint "PCIe_x16_Slot"\n'
    s += '  (version 20240108)\n'
    s += '  (generator "TFLN_gen")\n'
    s += '  (generator_version "8.0")\n'
    s += '  (layer "F.Cu")\n'
    s += '  (descr "PCIe Gen6 x16 Card Edge Connector")\n'
    s += '  (tags "PCIe x16 Gen6 slot")\n'
    s += '  (attr through_hole)\n'

    slot_len = 89.0
    slot_half = slot_len / 2.0

    s += f'  (fp_rect (start {-slot_half-3} -5) (end {slot_half+3} 15) (stroke (width 0.05) (type default)) (layer "F.CrtYd"))\n'
    s += f'  (fp_rect (start {-slot_half-2} -4) (end {slot_half+2} 14) (stroke (width 0.12) (type default)) (layer "F.SilkS"))\n'
    s += f'  (fp_text reference "REF**" (at 0 -6) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))\n'
    s += f'  (fp_text value "PCIe_x16_Slot" (at 0 16) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))\n'

    # 82 pins per side (164 total), 1.0mm pitch
    pitch = 1.0
    start_x = -(81 * pitch) / 2.0
    pad_num = 1

    # Side A
    for i in range(82):
        x = start_x + i * pitch
        s += f'  (pad "A{i+1}" thru_hole rect (at {x:.3f} 0) (size 0.8 1.6) (drill 0.5) (layers "*.Cu" "*.Mask"))\n'
        pad_num += 1

    # Side B
    for i in range(82):
        x = start_x + i * pitch
        s += f'  (pad "B{i+1}" thru_hole rect (at {x:.3f} 3.0) (size 0.8 1.6) (drill 0.5) (layers "*.Cu" "*.Mask"))\n'
        pad_num += 1

    # Key notch at pin 11/12
    key_x = start_x + 11 * pitch
    s += f'  (fp_rect (start {key_x-1} -2) (end {key_x+1} 5) (stroke (width 0.12) (type default)) (layer "F.SilkS"))\n'

    # Mounting/retention posts
    for xm in [-slot_half - 1, slot_half + 1]:
        s += f'  (pad "" thru_hole circle (at {xm:.3f} 1.5) (size 3.5 3.5) (drill 2.8) (layers "*.Cu" "*.Mask"))\n'

    s += ')\n'

    with open(os.path.join(OUTDIR, "PCIe_x16_Slot.kicad_mod"), "w") as f:
        f.write(s)
    print(f"  PCIe_x16_Slot.kicad_mod")


def nvme_m2_socket():
    """NVMe M.2 Key-M socket."""
    s = '(footprint "NVMe_M2_Socket"\n'
    s += '  (version 20240108)\n'
    s += '  (generator "TFLN_gen")\n'
    s += '  (generator_version "8.0")\n'
    s += '  (layer "F.Cu")\n'
    s += '  (descr "M.2 Key-M Socket for NVMe SSD, 2280 form factor")\n'
    s += '  (tags "M.2 NVMe Key-M 2280")\n'
    s += '  (attr smd)\n'

    s += '  (fp_rect (start -12 -4) (end 12 4) (stroke (width 0.05) (type default)) (layer "F.CrtYd"))\n'
    s += '  (fp_rect (start -11.5 -3.5) (end 11.5 3.5) (stroke (width 0.12) (type default)) (layer "F.SilkS"))\n'
    s += '  (fp_text reference "REF**" (at 0 -5) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))\n'
    s += '  (fp_text value "NVMe_M2_Socket" (at 0 5) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))\n'

    # 67 pins, 0.5mm pitch
    pitch = 0.5
    start_x = -(66 * pitch) / 2.0
    for i in range(67):
        x = start_x + i * pitch
        # Key-M notch: skip pins 60-66 area (simplified)
        if 59 <= i <= 63:
            continue
        s += f'  (pad "{i+1}" smd rect (at {x:.3f} 0) (size 0.3 1.5) (layers "F.Cu" "F.Paste" "F.Mask"))\n'

    # Mounting pads
    s += '  (pad "" smd rect (at -10.5 0) (size 1.5 3.0) (layers "F.Cu" "F.Mask"))\n'
    s += '  (pad "" smd rect (at 10.5 0) (size 1.5 3.0) (layers "F.Cu" "F.Mask"))\n'

    s += ')\n'

    with open(os.path.join(OUTDIR, "NVMe_M2_Socket.kicad_mod"), "w") as f:
        f.write(s)
    print(f"  NVMe_M2_Socket.kicad_mod")


def power_input_connector():
    """High-current power input connector."""
    s = '(footprint "Power_Input_Connector"\n'
    s += '  (version 20240108)\n'
    s += '  (generator "TFLN_gen")\n'
    s += '  (generator_version "8.0")\n'
    s += '  (layer "F.Cu")\n'
    s += '  (descr "High-current 12V power input connector")\n'
    s += '  (tags "power 12V high-current")\n'
    s += '  (attr through_hole)\n'

    s += '  (fp_rect (start -10 -8) (end 10 8) (stroke (width 0.05) (type default)) (layer "F.CrtYd"))\n'
    s += '  (fp_rect (start -9.5 -7.5) (end 9.5 7.5) (stroke (width 0.12) (type default)) (layer "F.SilkS"))\n'
    s += '  (fp_text reference "REF**" (at 0 -9) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))\n'
    s += '  (fp_text value "Power_Input_Connector" (at 0 9) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))\n'

    pad_num = 1
    # 8 VIN pins
    for i in range(8):
        y = -5.25 + i * 1.5
        s += f'  (pad "{pad_num}" thru_hole circle (at -5 {y:.2f}) (size 2.5 2.5) (drill 1.5) (layers "*.Cu" "*.Mask"))\n'
        pad_num += 1
    # 8 GND pins
    for i in range(8):
        y = -5.25 + i * 1.5
        s += f'  (pad "{pad_num}" thru_hole circle (at 5 {y:.2f}) (size 2.5 2.5) (drill 1.5) (layers "*.Cu" "*.Mask"))\n'
        pad_num += 1

    s += ')\n'

    with open(os.path.join(OUTDIR, "Power_Input_Connector.kicad_mod"), "w") as f:
        f.write(s)
    print(f"  Power_Input_Connector.kicad_mod")


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    print("Generating footprints:")
    bga256_08mm()
    tfln_photonic_hybrid()
    ddr5_dimm_288()
    vrm_drmos_array()
    pcie_x16_slot()
    nvme_m2_socket()
    power_input_connector()
    print("All footprints generated!")


if __name__ == "__main__":
    main()
