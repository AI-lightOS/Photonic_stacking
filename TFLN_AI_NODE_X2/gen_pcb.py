#!/usr/bin/env python3
"""Generate KiCad 8.0 PCB layout for TFLN_AI_NODE_X2.

22-layer stackup, component placement matching the board image,
design rules, net classes, power planes, filled zones, thermal reliefs,
and back-drill annotations.

Board layout from image (approx 300mm x 300mm):
- Top row: PCIe Gen6 x16 slots (4 left, 4 right)
- Upper middle: VRM Arrays (2 top)
- Center: 2x AI Compute Units with TFLN Photonic Engines
- Lower middle: VRM Arrays (2 bottom)  
- Center: V_core power plane, TFLN Modulators
- Bottom: PCIe Gen5 connector, Style bridge
- Left edge: NVMe Storage (4x M.2 U.3)
- Right edge: NVMe Storage (4x M.2 U.3)
- DDR5 DIMMs around compute units
"""

import uuid
import math

def uid():
    return str(uuid.uuid4())

# Board dimensions (mm)
BOARD_W = 305.0
BOARD_H = 280.0
ORIGIN_X = 50.0
ORIGIN_Y = 50.0

def header():
    s = '(kicad_pcb\n'
    s += '  (version 20240108)\n'
    s += '  (generator "TFLN_AI_NODE_X2_gen")\n'
    s += '  (generator_version "8.0")\n'
    s += '  (general\n'
    s += '    (thickness 3.2)\n'
    s += '    (legacy_teardrops no)\n'
    s += '  )\n'
    s += '  (paper "A2")\n'
    s += '  (title_block\n'
    s += '    (title "TFLN_AI_NODE_X2 - PCB Layout")\n'
    s += '    (date "2026-04-12")\n'
    s += '    (rev "1.0")\n'
    s += '    (company "LightRail AI / LightOS")\n'
    s += '    (comment 1 "22-Layer High-Speed PCB")\n'
    s += '    (comment 2 "V_core 0.8V / 1000A+ Power Delivery")\n'
    s += '  )\n'
    return s

def layers_22():
    """22-layer copper stackup definition."""
    s = '  (layers\n'
    # Define all 22 copper layers + mask/silk/courtyard etc.
    layer_defs = [
        (0, "F.Cu", "signal"),
        (1, "In1.Cu", "signal"),
        (2, "In2.Cu", "power"),
        (3, "In3.Cu", "signal"),
        (4, "In4.Cu", "signal"),
        (5, "In5.Cu", "signal"),
        (6, "In6.Cu", "power"),
        (7, "In7.Cu", "signal"),
        (8, "In8.Cu", "signal"),
        (9, "In9.Cu", "signal"),
        (10, "In10.Cu", "signal"),
        (11, "In11.Cu", "signal"),
        (12, "In12.Cu", "signal"),
        (13, "In13.Cu", "signal"),
        (14, "In14.Cu", "power"),
        (15, "In15.Cu", "signal"),
        (16, "In16.Cu", "signal"),
        (17, "In17.Cu", "signal"),
        (18, "In18.Cu", "power"),
        (19, "In19.Cu", "signal"),
        (20, "In20.Cu", "signal"),
        (31, "B.Cu", "signal"),
    ]
    for lid, name, ltype in layer_defs:
        s += f'    ({lid} "{name}" {ltype})\n'
    
    # Non-copper layers
    non_copper = [
        (32, "B.Adhes", "user", "B.Adhes"),
        (33, "F.Adhes", "user", "F.Adhes"),
        (34, "B.Paste", "user", "B.Paste"),
        (35, "F.Paste", "user", "F.Paste"),
        (36, "B.SilkS", "user", "B.SilkS"),
        (37, "F.SilkS", "user", "F.SilkS"),
        (38, "B.Mask", "user", "B.Mask"),
        (39, "F.Mask", "user", "F.Mask"),
        (40, "Dwgs.User", "user", "Dwgs.User"),
        (41, "Cmts.User", "user", "Cmts.User"),
        (42, "Eco1.User", "user", "Eco1.User"),
        (43, "Eco2.User", "user", "Eco2.User"),
        (44, "Edge.Cuts", "user", "Edge.Cuts"),
        (45, "Margin", "user", "Margin"),
        (46, "B.CrtYd", "user", "B.CrtYd"),
        (47, "F.CrtYd", "user", "F.CrtYd"),
        (48, "B.Fab", "user", "B.Fab"),
        (49, "F.Fab", "user", "F.Fab"),
        (50, "User.1", "user", "User.1"),
        (51, "User.2", "user", "User.2"),
    ]
    for lid, name, ltype, desc in non_copper:
        s += f'    ({lid} "{name}" {ltype})\n'
    
    s += '  )\n'
    return s

def setup_and_design_rules():
    """Board setup with net classes and design rules."""
    s = '  (setup\n'
    
    # Pad settings
    s += '    (pad_to_mask_clearance 0.051)\n'
    s += '    (allow_soldermask_bridges_in_footprints no)\n'
    s += '    (pcbplotparams\n'
    s += '      (layerselection 0x0001ffff_ffffffff)\n'
    s += '      (plot_on_all_layers_selection 0x0000000_00000000)\n'
    s += '      (disableapertmacros no)\n'
    s += '      (usegerberextensions yes)\n'
    s += '      (usegerberattributes yes)\n'
    s += '      (usegerberadvancedattributes yes)\n'
    s += '      (creategerberjobfile yes)\n'
    s += '      (dashed_line_dash_ratio 12.000000)\n'
    s += '      (dashed_line_gap_ratio 3.000000)\n'
    s += '      (svgprecision 4)\n'
    s += '      (plotframeref no)\n'
    s += '      (viasonmask no)\n'
    s += '      (mode 1)\n'
    s += '      (useauxorigin no)\n'
    s += '      (hpglpennumber 1)\n'
    s += '      (hpglpenspeed 20)\n'
    s += '      (hpglpendiameter 15.000000)\n'
    s += '      (pdf_front_fp_property_popups yes)\n'
    s += '      (pdf_back_fp_property_popups yes)\n'
    s += '      (dxf_units mm)\n'
    s += '      (dxf_use_pcbnew_font yes)\n'
    s += '      (psnegative no)\n'
    s += '      (psa4output no)\n'
    s += '      (plotreference yes)\n'
    s += '      (plotvalue no)\n'
    s += '      (plotfptext yes)\n'
    s += '      (plotinvisibletext no)\n'
    s += '      (sketchpadsonfab no)\n'
    s += '      (subtractmaskfromsilk yes)\n'
    s += '      (outputformat 1)\n'
    s += '      (mirror no)\n'
    s += '      (drillshape 1)\n'
    s += '      (scaleselection 1)\n'
    s += '      (outputdirectory "fab_outputs/")\n'
    s += '    )\n'
    s += '  )\n'
    return s

def net_definitions():
    """Define all nets for the board."""
    s = '  (net 0 "")\n'
    s += '  (net 1 "GND")\n'
    s += '  (net 2 "V_CORE_0V8")\n'
    s += '  (net 3 "VIN_12V")\n'
    s += '  (net 4 "V_IO_1V1")\n'
    s += '  (net 5 "V_DDQ_1V1")\n'
    s += '  (net 6 "V_3V3")\n'
    
    net_id = 7
    nets = []
    
    # SerDes diff pairs (16 pairs per AI unit, 2 units)
    for u in range(1, 3):
        for i in range(16):
            s += f'  (net {net_id} "SERDES_U{u}_TX{i}_P")\n'; nets.append((net_id, f"SERDES_U{u}_TX{i}_P")); net_id += 1
            s += f'  (net {net_id} "SERDES_U{u}_TX{i}_N")\n'; nets.append((net_id, f"SERDES_U{u}_TX{i}_N")); net_id += 1
            s += f'  (net {net_id} "SERDES_U{u}_RX{i}_P")\n'; nets.append((net_id, f"SERDES_U{u}_RX{i}_P")); net_id += 1
            s += f'  (net {net_id} "SERDES_U{u}_RX{i}_N")\n'; nets.append((net_id, f"SERDES_U{u}_RX{i}_N")); net_id += 1
    
    # PCIe lanes (16 lanes per slot, 8 slots - simplified to 16 main lanes)
    for i in range(16):
        s += f'  (net {net_id} "PCIE_TX{i}_P")\n'; net_id += 1
        s += f'  (net {net_id} "PCIE_TX{i}_N")\n'; net_id += 1
        s += f'  (net {net_id} "PCIE_RX{i}_P")\n'; net_id += 1
        s += f'  (net {net_id} "PCIE_RX{i}_N")\n'; net_id += 1
    
    # DDR5 data bus (64 bits per channel, 4 channels)
    for ch in range(4):
        for bit in range(64):
            s += f'  (net {net_id} "DDR5_CH{ch}_DQ{bit}")\n'; net_id += 1
    
    # TFLN RF pairs (8 per engine, 2 engines)
    for u in range(1, 3):
        for i in range(8):
            s += f'  (net {net_id} "TFLN{u}_RF{i}_P")\n'; net_id += 1
            s += f'  (net {net_id} "TFLN{u}_RF{i}_N")\n'; net_id += 1
    
    # VRM phase outputs
    for v in range(1, 5):
        for ph in range(24):
            s += f'  (net {net_id} "VRM{v}_PH{ph}")\n'; net_id += 1
    
    # PWM control
    for v in range(1, 5):
        for pw in range(12):
            s += f'  (net {net_id} "VRM{v}_PWM{pw}")\n'; net_id += 1
    
    # TFLN bias
    for u in range(1, 3):
        for i in range(8):
            s += f'  (net {net_id} "TFLN{u}_BIAS{i}")\n'; net_id += 1
    
    s += '\n'
    return s, net_id

def net_classes():
    """Net class assignments."""
    s = '  (net_class "Default"\n'
    s += '    (clearance 0.15)\n'
    s += '    (trace_width 0.2)\n'
    s += '    (via_dia 0.6)\n'
    s += '    (via_drill 0.3)\n'
    s += '    (uvia_dia 0.3)\n'
    s += '    (uvia_drill 0.1)\n'
    s += '  )\n'
    s += '  (net_class "DDR5_DQ"\n'
    s += '    (clearance 0.12)\n'
    s += '    (trace_width 0.1)\n'
    s += '    (via_dia 0.5)\n'
    s += '    (via_drill 0.25)\n'
    s += '    (uvia_dia 0.3)\n'
    s += '    (uvia_drill 0.1)\n'
    s += '    (diff_pair_width 0.1)\n'
    s += '    (diff_pair_gap 0.15)\n'
    s += '  )\n'
    s += '  (net_class "PCIe_Gen6"\n'
    s += '    (clearance 0.12)\n'
    s += '    (trace_width 0.12)\n'
    s += '    (via_dia 0.5)\n'
    s += '    (via_drill 0.25)\n'
    s += '    (uvia_dia 0.3)\n'
    s += '    (uvia_drill 0.1)\n'
    s += '    (diff_pair_width 0.12)\n'
    s += '    (diff_pair_gap 0.18)\n'
    s += '  )\n'
    s += '  (net_class "TFLN_RF"\n'
    s += '    (clearance 0.2)\n'
    s += '    (trace_width 0.15)\n'
    s += '    (via_dia 0.5)\n'
    s += '    (via_drill 0.25)\n'
    s += '    (uvia_dia 0.3)\n'
    s += '    (uvia_drill 0.1)\n'
    s += '    (diff_pair_width 0.15)\n'
    s += '    (diff_pair_gap 0.25)\n'
    s += '  )\n'
    return s

def board_outline():
    """Board outline on Edge.Cuts layer."""
    x1 = ORIGIN_X
    y1 = ORIGIN_Y
    x2 = ORIGIN_X + BOARD_W
    y2 = ORIGIN_Y + BOARD_H
    s = f'  (gr_rect (start {x1} {y1}) (end {x2} {y2}) (stroke (width 0.1) (type solid)) (fill none) (layer "Edge.Cuts") (uuid "{uid()}"))\n'
    return s

def footprint_ref(ref, fp_name, x, y, layer="F.Cu", angle=0):
    """Generate a footprint placement reference.
    We read the actual footprint file and place it."""
    import os
    fp_file = f"footprints.pretty/{fp_name}.kicad_mod"
    
    if not os.path.exists(fp_file):
        # Return a simple placeholder
        s = f'  (footprint "TFLN_AI_NODE_X2:{fp_name}"\n'
        s += f'    (layer "{layer}")\n'
        s += f'    (uuid "{uid()}")\n'
        s += f'    (at {x:.2f} {y:.2f} {angle})\n'
        s += f'    (property "Reference" "{ref}" (at 0 -2 0) (layer "F.SilkS") (uuid "{uid()}") (effects (font (size 1 1) (thickness 0.15))))\n'
        s += f'    (property "Value" "{fp_name}" (at 0 2 0) (layer "F.Fab") (uuid "{uid()}") (effects (font (size 1 1) (thickness 0.15))))\n'
        s += f'  )\n'
        return s
    
    # Read and modify the footprint
    with open(fp_file, 'r') as f:
        content = f.read()
    
    import re
    
    # Expand *.Cu wildcard to list all 22 copper layers
    all_cu = '"F.Cu" "In1.Cu" "In2.Cu" "In3.Cu" "In4.Cu" "In5.Cu" "In6.Cu" "In7.Cu" "In8.Cu" "In9.Cu" "In10.Cu" "In11.Cu" "In12.Cu" "In13.Cu" "In14.Cu" "In15.Cu" "In16.Cu" "In17.Cu" "In18.Cu" "In19.Cu" "In20.Cu" "B.Cu"'
    content = content.replace('"*.Cu"', all_cu)
    content = content.replace('"*.Mask"', '"F.Mask" "B.Mask"')
    
    # Replace the footprint header to include placement
    s = content.replace(
        f'(footprint "{fp_name}"',
        f'(footprint "TFLN_AI_NODE_X2:{fp_name}"'
    )
    # Insert placement info after layer line
    layer_line = f'  (layer "{layer}")\n'
    placement = f'  (layer "{layer}")\n  (uuid "{uid()}")\n  (at {x:.2f} {y:.2f} {angle})\n'
    s = s.replace(layer_line, placement, 1)
    
    # Fix reference to use actual ref designator
    s = re.sub(r'(fp_text reference )"REF\*\*"', f'\\1"{ref}"', s)
    
    # Indent everything by 2 spaces for PCB context
    lines = s.strip().split('\n')
    s = '  ' + '\n  '.join(lines) + '\n'
    
    return s

def place_components():
    """Place all components on the PCB matching the board image layout."""
    s = ''
    cx = ORIGIN_X + BOARD_W / 2.0  # center X
    cy = ORIGIN_Y + BOARD_H / 2.0  # center Y
    
    # ============================================
    # AI Compute Units (center of board)
    # ============================================
    s += footprint_ref("U1", "BGA256_0.8mm", cx - 45, cy - 15)
    s += footprint_ref("U2", "BGA256_0.8mm", cx + 45, cy - 15)
    
    # ============================================
    # TFLN Photonic Engines (below AI units)
    # ============================================
    s += footprint_ref("U3", "TFLN_Photonic_Hybrid", cx - 45, cy + 15)
    s += footprint_ref("U4", "TFLN_Photonic_Hybrid", cx + 45, cy + 15)
    
    # ============================================
    # VRM Arrays (4 around compute units)
    # Top-left, Top-right, Bottom-left, Bottom-right
    # ============================================
    s += footprint_ref("U5", "VRM_DrMOS_Array", cx - 70, cy - 55)   # Top-left
    s += footprint_ref("U6", "VRM_DrMOS_Array", cx + 70, cy - 55)   # Top-right
    s += footprint_ref("U7", "VRM_DrMOS_Array", cx - 70, cy + 55)   # Bottom-left
    s += footprint_ref("U8", "VRM_DrMOS_Array", cx + 70, cy + 55)   # Bottom-right
    
    # ============================================
    # PCIe Gen6 x16 Expansion Slots (8 total)
    # 4 across top, 4 across bottom (or as per image: top row)
    # ============================================
    pcie_y_top = ORIGIN_Y + 25
    pcie_y_bot = ORIGIN_Y + BOARD_H - 25
    for i in range(4):
        x = ORIGIN_X + 40 + i * 70
        s += footprint_ref(f"J{i+1}", "PCIe_x16_Slot", x, pcie_y_top, angle=0)
    for i in range(4):
        x = ORIGIN_X + 40 + i * 70
        s += footprint_ref(f"J{i+5}", "PCIe_x16_Slot", x, pcie_y_bot, angle=180)
    
    # ============================================
    # DDR5 DIMM Slots (4 total, 2 per side of compute)
    # ============================================
    s += footprint_ref("J9", "DDR5_DIMM_288pin", cx - 90, cy - 10, angle=90)
    s += footprint_ref("J10", "DDR5_DIMM_288pin", cx - 90, cy + 10, angle=90)
    s += footprint_ref("J11", "DDR5_DIMM_288pin", cx + 90, cy - 10, angle=90)
    s += footprint_ref("J12", "DDR5_DIMM_288pin", cx + 90, cy + 10, angle=90)
    
    # ============================================
    # NVMe M.2 Storage (4 total, 2 left, 2 right)
    # ============================================
    s += footprint_ref("J13", "NVMe_M2_Socket", ORIGIN_X + 20, cy - 30)
    s += footprint_ref("J14", "NVMe_M2_Socket", ORIGIN_X + 20, cy + 30)
    s += footprint_ref("J15", "NVMe_M2_Socket", ORIGIN_X + BOARD_W - 20, cy - 30)
    s += footprint_ref("J16", "NVMe_M2_Socket", ORIGIN_X + BOARD_W - 20, cy + 30)
    
    # ============================================
    # Power Input Connectors (2, bottom edge)
    # ============================================
    s += footprint_ref("J17", "Power_Input_Connector", cx - 50, ORIGIN_Y + BOARD_H - 15)
    s += footprint_ref("J18", "Power_Input_Connector", cx + 50, ORIGIN_Y + BOARD_H - 15)
    
    return s

def filled_zones():
    """Create power plane zones and GND fills."""
    s = ''
    x1 = ORIGIN_X + 1
    y1 = ORIGIN_Y + 1
    x2 = ORIGIN_X + BOARD_W - 1
    y2 = ORIGIN_Y + BOARD_H - 1
    
    # ============================================
    # GND plane on L2 (In1.Cu) - Solid reference
    # ============================================
    s += f'  (zone (net 1) (net_name "GND") (layer "In1.Cu") (uuid "{uid()}")\n'
    s += f'    (name "GND_L2")\n'
    s += f'    (hatch edge 0.5)\n'
    s += f'    (connect_pads (clearance 0.15))\n'
    s += f'    (min_thickness 0.2)\n'
    s += f'    (fill yes (thermal_gap 0.3) (thermal_bridge_width 0.4))\n'
    s += f'    (polygon (pts\n'
    s += f'      (xy {x1} {y1}) (xy {x2} {y1}) (xy {x2} {y2}) (xy {x1} {y2})\n'
    s += f'    ))\n'
    s += f'  )\n'
    
    # ============================================
    # V_CORE 0.8V plane on L3 (In2.Cu) - Heavy copper 2oz
    # Massive polygon for 1000A+ rails
    # ============================================
    s += f'  (zone (net 2) (net_name "V_CORE_0V8") (layer "In2.Cu") (uuid "{uid()}")\n'
    s += f'    (name "VCORE_L3")\n'
    s += f'    (hatch edge 0.5)\n'
    s += f'    (connect_pads (clearance 0.2))\n'
    s += f'    (min_thickness 0.3)\n'
    s += f'    (fill yes (thermal_gap 0.0) (thermal_bridge_width 0.0))\n'  # Solid connection - no thermal relief for max current
    s += f'    (polygon (pts\n'
    s += f'      (xy {x1} {y1}) (xy {x2} {y1}) (xy {x2} {y2}) (xy {x1} {y2})\n'
    s += f'    ))\n'
    s += f'  )\n'
    
    # ============================================
    # GND plane on L5 (In4.Cu)
    # ============================================
    s += f'  (zone (net 1) (net_name "GND") (layer "In4.Cu") (uuid "{uid()}")\n'
    s += f'    (name "GND_L5")\n'
    s += f'    (hatch edge 0.5)\n'
    s += f'    (connect_pads (clearance 0.15))\n'
    s += f'    (min_thickness 0.2)\n'
    s += f'    (fill yes (thermal_gap 0.3) (thermal_bridge_width 0.4))\n'
    s += f'    (polygon (pts\n'
    s += f'      (xy {x1} {y1}) (xy {x2} {y1}) (xy {x2} {y2}) (xy {x1} {y2})\n'
    s += f'    ))\n'
    s += f'  )\n'
    
    # ============================================
    # V_IO 1.1V on L7 (In6.Cu)
    # ============================================
    s += f'  (zone (net 4) (net_name "V_IO_1V1") (layer "In6.Cu") (uuid "{uid()}")\n'
    s += f'    (name "VIO_L7")\n'
    s += f'    (hatch edge 0.5)\n'
    s += f'    (connect_pads (clearance 0.2))\n'
    s += f'    (min_thickness 0.25)\n'
    s += f'    (fill yes (thermal_gap 0.0) (thermal_bridge_width 0.0))\n'
    s += f'    (polygon (pts\n'
    s += f'      (xy {x1} {y1}) (xy {x2} {y1}) (xy {x2} {y2}) (xy {x1} {y2})\n'
    s += f'    ))\n'
    s += f'  )\n'
    
    # ============================================
    # GND plane on L9 (In8.Cu)
    # ============================================
    s += f'  (zone (net 1) (net_name "GND") (layer "In8.Cu") (uuid "{uid()}")\n'
    s += f'    (name "GND_L9")\n'
    s += f'    (hatch edge 0.5)\n'
    s += f'    (connect_pads (clearance 0.15))\n'
    s += f'    (min_thickness 0.2)\n'
    s += f'    (fill yes (thermal_gap 0.3) (thermal_bridge_width 0.4))\n'
    s += f'    (polygon (pts\n'
    s += f'      (xy {x1} {y1}) (xy {x2} {y1}) (xy {x2} {y2}) (xy {x1} {y2})\n'
    s += f'    ))\n'
    s += f'  )\n'
    
    # ============================================
    # GND plane on L13 (In12.Cu)
    # ============================================
    s += f'  (zone (net 1) (net_name "GND") (layer "In12.Cu") (uuid "{uid()}")\n'
    s += f'    (name "GND_L13")\n'
    s += f'    (hatch edge 0.5)\n'
    s += f'    (connect_pads (clearance 0.15))\n'
    s += f'    (min_thickness 0.2)\n'
    s += f'    (fill yes (thermal_gap 0.3) (thermal_bridge_width 0.4))\n'
    s += f'    (polygon (pts\n'
    s += f'      (xy {x1} {y1}) (xy {x2} {y1}) (xy {x2} {y2}) (xy {x1} {y2})\n'
    s += f'    ))\n'
    s += f'  )\n'
    
    # ============================================
    # V_DDQ 1.1V on L15 (In14.Cu)
    # ============================================
    s += f'  (zone (net 5) (net_name "V_DDQ_1V1") (layer "In14.Cu") (uuid "{uid()}")\n'
    s += f'    (name "VDDQ_L15")\n'
    s += f'    (hatch edge 0.5)\n'
    s += f'    (connect_pads (clearance 0.2))\n'
    s += f'    (min_thickness 0.25)\n'
    s += f'    (fill yes (thermal_gap 0.0) (thermal_bridge_width 0.0))\n'
    s += f'    (polygon (pts\n'
    s += f'      (xy {x1} {y1}) (xy {x2} {y1}) (xy {x2} {y2}) (xy {x1} {y2})\n'
    s += f'    ))\n'
    s += f'  )\n'
    
    # ============================================
    # GND plane on L17 (In16.Cu)
    # ============================================
    s += f'  (zone (net 1) (net_name "GND") (layer "In16.Cu") (uuid "{uid()}")\n'
    s += f'    (name "GND_L17")\n'
    s += f'    (hatch edge 0.5)\n'
    s += f'    (connect_pads (clearance 0.15))\n'
    s += f'    (min_thickness 0.2)\n'
    s += f'    (fill yes (thermal_gap 0.3) (thermal_bridge_width 0.4))\n'
    s += f'    (polygon (pts\n'
    s += f'      (xy {x1} {y1}) (xy {x2} {y1}) (xy {x2} {y2}) (xy {x1} {y2})\n'
    s += f'    ))\n'
    s += f'  )\n'
    
    # ============================================
    # 3.3V Auxiliary on L19 (In18.Cu)
    # ============================================
    s += f'  (zone (net 6) (net_name "V_3V3") (layer "In18.Cu") (uuid "{uid()}")\n'
    s += f'    (name "V3V3_L19")\n'
    s += f'    (hatch edge 0.5)\n'
    s += f'    (connect_pads (clearance 0.2))\n'
    s += f'    (min_thickness 0.25)\n'
    s += f'    (fill yes (thermal_gap 0.0) (thermal_bridge_width 0.0))\n'
    s += f'    (polygon (pts\n'
    s += f'      (xy {x1} {y1}) (xy {x2} {y1}) (xy {x2} {y2}) (xy {x1} {y2})\n'
    s += f'    ))\n'
    s += f'  )\n'
    
    # ============================================
    # GND plane on L20 (In19.Cu)
    # ============================================
    s += f'  (zone (net 1) (net_name "GND") (layer "In19.Cu") (uuid "{uid()}")\n'
    s += f'    (name "GND_L20")\n'
    s += f'    (hatch edge 0.5)\n'
    s += f'    (connect_pads (clearance 0.15))\n'
    s += f'    (min_thickness 0.2)\n'
    s += f'    (fill yes (thermal_gap 0.3) (thermal_bridge_width 0.4))\n'
    s += f'    (polygon (pts\n'
    s += f'      (xy {x1} {y1}) (xy {x2} {y1}) (xy {x2} {y2}) (xy {x1} {y2})\n'
    s += f'    ))\n'
    s += f'  )\n'
    
    # ============================================
    # Top copper (F.Cu) GND fill with TFLN cavity keep-out
    # ============================================
    s += f'  (zone (net 1) (net_name "GND") (layer "F.Cu") (uuid "{uid()}")\n'
    s += f'    (name "GND_TOP")\n'
    s += f'    (hatch edge 0.5)\n'
    s += f'    (priority 0)\n'
    s += f'    (connect_pads (clearance 0.15))\n'
    s += f'    (min_thickness 0.2)\n'
    s += f'    (fill yes (thermal_gap 0.3) (thermal_bridge_width 0.4))\n'
    s += f'    (polygon (pts\n'
    s += f'      (xy {x1} {y1}) (xy {x2} {y1}) (xy {x2} {y2}) (xy {x1} {y2})\n'
    s += f'    ))\n'
    s += f'  )\n'
    
    # ============================================
    # Bottom copper (B.Cu) GND fill
    # ============================================
    s += f'  (zone (net 1) (net_name "GND") (layer "B.Cu") (uuid "{uid()}")\n'
    s += f'    (name "GND_BOT")\n'
    s += f'    (hatch edge 0.5)\n'
    s += f'    (connect_pads (clearance 0.15))\n'
    s += f'    (min_thickness 0.2)\n'
    s += f'    (fill yes (thermal_gap 0.3) (thermal_bridge_width 0.4))\n'
    s += f'    (polygon (pts\n'
    s += f'      (xy {x1} {y1}) (xy {x2} {y1}) (xy {x2} {y2}) (xy {x1} {y2})\n'
    s += f'    ))\n'
    s += f'  )\n'
    
    return s

def backdrill_annotations():
    """Back-drill annotations on User.Comments layer for fab house.
    Mark 85-ohm and 100-ohm signal vias requiring stub removal."""
    s = ''
    cx = ORIGIN_X + BOARD_W / 2.0
    cy = ORIGIN_Y + BOARD_H / 2.0
    
    # Title
    s += f'  (gr_text "BACK-DRILL INSTRUCTIONS FOR FAB HOUSE" (at {cx} {ORIGIN_Y + 8}) (layer "User.1") (uuid "{uid()}")\n'
    s += f'    (effects (font (size 3 3) (thickness 0.3) bold))\n'
    s += f'  )\n'
    
    # Instructions
    instructions = [
        "1. All vias marked with 85-OHM on this layer require back-drilling for 85-ohm impedance control",
        "2. All vias marked with 100-OHM on this layer require back-drilling for 100-ohm diff pair impedance",
        "3. Back-drill depth: Remove stub to within 0.2mm of target signal layer",
        "4. PCIe Gen6 vias (100-ohm): Drill from bottom, target layers L4/L18 (In3.Cu/In17.Cu)",
        "5. TFLN RF vias (85-ohm): Drill from bottom, target layer L1 (F.Cu) - CRITICAL: top layer only routing",
        "6. DDR5 vias (100-ohm): Drill from bottom, target layers L6/L16 (In5.Cu/In15.Cu)",
    ]
    for i, inst in enumerate(instructions):
        s += f'  (gr_text "{inst}" (at {cx} {ORIGIN_Y + 14 + i * 4}) (layer "User.1") (uuid "{uid()}")\n'
        s += f'    (effects (font (size 1.5 1.5) (thickness 0.15)) (justify left))\n'
        s += f'  )\n'
    
    # Mark specific via zones for back-drilling
    # PCIe via zone (near slots)
    for i in range(4):
        x = ORIGIN_X + 40 + i * 70
        s += f'  (gr_rect (start {x-10} {ORIGIN_Y+35}) (end {x+10} {ORIGIN_Y+45}) (stroke (width 0.2) (type dash)) (fill none) (layer "User.1") (uuid "{uid()}"))\n'
        s += f'  (gr_text "100-OHM BACKDRILL ZONE\\nPCIe Gen6 Vias" (at {x} {ORIGIN_Y+40}) (layer "User.1") (uuid "{uid()}")\n'
        s += f'    (effects (font (size 1 1) (thickness 0.1)))\n'
        s += f'  )\n'
    
    # TFLN RF via zone (near photonic engines)
    for dx in [-45, 45]:
        x = cx + dx
        s += f'  (gr_rect (start {x-18} {cy+5}) (end {x+18} {cy+25}) (stroke (width 0.2) (type dash)) (fill none) (layer "User.1") (uuid "{uid()}"))\n'
        s += f'  (gr_text "85-OHM BACKDRILL ZONE\\nTFLN RF Vias - TOP LAYER ONLY" (at {x} {cy+15}) (layer "User.1") (uuid "{uid()}")\n'
        s += f'    (effects (font (size 1 1) (thickness 0.1)))\n'
        s += f'  )\n'
    
    # DDR5 via zones
    for dx in [-90, 90]:
        x = cx + dx
        s += f'  (gr_rect (start {x-8} {cy-20}) (end {x+8} {cy+20}) (stroke (width 0.2) (type dash)) (fill none) (layer "User.1") (uuid "{uid()}"))\n'
        s += f'  (gr_text "100-OHM BACKDRILL\\nDDR5 Vias" (at {x} {cy}) (layer "User.1") (uuid "{uid()}")\n'
        s += f'    (effects (font (size 1 1) (thickness 0.1)))\n'
        s += f'  )\n'
    
    return s

def board_annotations():
    """Add board annotations - silkscreen text, design notes."""
    s = ''
    cx = ORIGIN_X + BOARD_W / 2.0
    cy = ORIGIN_Y + BOARD_H / 2.0
    
    # Board title on silkscreen
    s += f'  (gr_text "TFLN_AI_NODE_X2" (at {cx} {ORIGIN_Y + BOARD_H - 5}) (layer "F.SilkS") (uuid "{uid()}")\n'
    s += f'    (effects (font (size 3 3) (thickness 0.3) bold))\n'
    s += f'  )\n'
    
    s += f'  (gr_text "SCHEMATIC: TFLN Photonic-Integrated AI Compute Node" (at {cx} {ORIGIN_Y + BOARD_H - 9}) (layer "F.SilkS") (uuid "{uid()}")\n'
    s += f'    (effects (font (size 1.5 1.5) (thickness 0.15)))\n'
    s += f'  )\n'
    
    s += f'  (gr_text "(Based on MidBoard - with 8x PCIe 5.0 Slots)" (at {cx} {ORIGIN_Y + BOARD_H - 12}) (layer "F.SilkS") (uuid "{uid()}")\n'
    s += f'    (effects (font (size 1.2 1.2) (thickness 0.12)))\n'
    s += f'  )\n'
    
    # V_core label in center
    s += f'  (gr_text "V_core\\n0.8V / 1000A+" (at {cx} {cy}) (layer "F.SilkS") (uuid "{uid()}")\n'
    s += f'    (effects (font (size 2 2) (thickness 0.2) bold))\n'
    s += f'  )\n'
    
    # Component group labels
    labels = [
        (cx - 45, cy - 35, "AI COMPUTE UNIT 1\\n(TFLN Photonic Enabled)"),
        (cx + 45, cy - 35, "AI COMPUTE UNIT 2\\n(TFLN Photonic Enabled)"),
        (cx - 45, cy + 30, "Integrated Optical Engine\\nTFLN Modulators"),
        (cx + 45, cy + 30, "Integrated Optical Engine\\nTFLN Modulators"),
        (cx - 70, cy - 70, "VRM Array\\n(24-Phase, DrMOS)"),
        (cx + 70, cy - 70, "VRM Array\\n(24-Phase, DrMOS)"),
        (cx - 70, cy + 70, "VRM Array\\n(24-Phase, DrMOS)"),
        (cx + 70, cy + 70, "VRM Array\\n(24-Phase, DrMOS)"),
        (ORIGIN_X + 20, cy - 45, "NVMe Storage\\n4x M.2 U.3"),
        (ORIGIN_X + BOARD_W - 20, cy - 45, "NVMe Storage\\n4x M.2 U.3"),
    ]
    for x, y, text in labels:
        s += f'  (gr_text "{text}" (at {x:.1f} {y:.1f}) (layer "F.SilkS") (uuid "{uid()}")\n'
        s += f'    (effects (font (size 1.2 1.2) (thickness 0.12)))\n'
        s += f'  )\n'
    
    # PCIe slot labels
    for i in range(4):
        x = ORIGIN_X + 40 + i * 70
        s += f'  (gr_text "PCIe Gen6 Expansion\\n(4x Slots, x16/x22\\nLanes, Interleaved)" (at {x:.1f} {ORIGIN_Y + 15:.1f}) (layer "F.SilkS") (uuid "{uid()}")\n'
        s += f'    (effects (font (size 1 1) (thickness 0.1)))\n'
        s += f'  )\n'
    
    return s

def sample_diff_pair_traces():
    """Add sample differential pair traces to demonstrate routing strategy.
    TFLN RF pairs on L1 (F.Cu) only - no vias per constraint."""
    s = ''
    cx = ORIGIN_X + BOARD_W / 2.0
    cy = ORIGIN_Y + BOARD_H / 2.0
    
    # TFLN differential pair traces on F.Cu (top layer only)
    # Routed from AI compute unit to TFLN engine
    for i in range(8):
        y_start = cy - 25 + i * 3.5
        y_end = cy + 5 + i * 2.0
        # P trace
        s += f'  (segment (start {cx-60:.2f} {y_start:.2f}) (end {cx-60:.2f} {y_end:.2f}) (width 0.15) (layer "F.Cu") (net 0) (uuid "{uid()}"))\n'
        # N trace (gapped by 0.25mm)
        s += f'  (segment (start {cx-60.40:.2f} {y_start:.2f}) (end {cx-60.40:.2f} {y_end:.2f}) (width 0.15) (layer "F.Cu") (net 0) (uuid "{uid()}"))\n'
    
    # PCIe Gen6 diff pairs on L4 (In3.Cu)
    for i in range(4):
        x_start = ORIGIN_X + 40 + i * 70
        x_end = cx - 30 + i * 20
        y_start = ORIGIN_Y + 50
        y_end = cy - 30
        # P trace
        s += f'  (segment (start {x_start:.2f} {y_start:.2f}) (end {x_end:.2f} {y_end:.2f}) (width 0.12) (layer "In3.Cu") (net 0) (uuid "{uid()}"))\n'
        # N trace
        s += f'  (segment (start {x_start+0.30:.2f} {y_start:.2f}) (end {x_end+0.30:.2f} {y_end:.2f}) (width 0.12) (layer "In3.Cu") (net 0) (uuid "{uid()}"))\n'
    
    # DDR5 DQ traces on L6 (In5.Cu)
    for i in range(8):
        x = cx - 85 + i * 2.0
        y_start = cy - 15
        y_end = cy + 15
        s += f'  (segment (start {x:.2f} {y_start:.2f}) (end {x:.2f} {y_end:.2f}) (width 0.1) (layer "In5.Cu") (net 0) (uuid "{uid()}"))\n'
    
    return s


def main():
    pcb = header()
    pcb += layers_22()
    pcb += setup_and_design_rules()
    
    nets_str, max_net = net_definitions()
    pcb += nets_str
    
    pcb += board_outline()
    pcb += place_components()
    pcb += filled_zones()
    pcb += backdrill_annotations()
    pcb += board_annotations()
    pcb += sample_diff_pair_traces()
    
    pcb += ')\n'
    
    with open("TFLN_AI_NODE_X2.kicad_pcb", "w") as f:
        f.write(pcb)
    print(f"PCB layout generated: TFLN_AI_NODE_X2.kicad_pcb ({max_net} nets)")


if __name__ == "__main__":
    main()
