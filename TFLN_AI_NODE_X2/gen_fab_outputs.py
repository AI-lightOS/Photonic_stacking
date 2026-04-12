#!/usr/bin/env python3
"""Generate fabrication output files for TFLN_AI_NODE_X2.

Outputs:
- BOM (Bill of Materials) CSV
- Component Placement / Centroid (.pos) file
- Drill summary
- Fab notes / README
"""

import csv
import os

OUTDIR = "fab_outputs"
os.makedirs(OUTDIR, exist_ok=True)


def generate_bom():
    """Generate BOM CSV using kicad_netlist_reader format."""
    bom = [
        ["Reference", "Value", "Footprint", "Quantity", "Description", "Manufacturer", "MPN"],
        ["U1", "AI_Compute_Unit_1", "BGA256_0.8mm", "1", "AI Compute Unit with TFLN Photonic-Enabled BGA256", "Custom", "TFLN-ACU-256"],
        ["U2", "AI_Compute_Unit_2", "BGA256_0.8mm", "1", "AI Compute Unit with TFLN Photonic-Enabled BGA256", "Custom", "TFLN-ACU-256"],
        ["U3", "TFLN_Photonic_Engine_1", "TFLN_Photonic_Hybrid", "1", "TFLN Photonic Engine with Integrated Optical Engine and Modulators", "Custom", "TFLN-PE-001"],
        ["U4", "TFLN_Photonic_Engine_2", "TFLN_Photonic_Hybrid", "1", "TFLN Photonic Engine with Integrated Optical Engine and Modulators", "Custom", "TFLN-PE-001"],
        ["U5", "VRM_Array_Top_Left", "VRM_DrMOS_Array", "1", "24-Phase VRM DrMOS Array for V_core 0.8V / 1000A+", "Custom", "VRM-24PH-DRM"],
        ["U6", "VRM_Array_Top_Right", "VRM_DrMOS_Array", "1", "24-Phase VRM DrMOS Array for V_core 0.8V / 1000A+", "Custom", "VRM-24PH-DRM"],
        ["U7", "VRM_Array_Bot_Left", "VRM_DrMOS_Array", "1", "24-Phase VRM DrMOS Array for V_core 0.8V / 1000A+", "Custom", "VRM-24PH-DRM"],
        ["U8", "VRM_Array_Bot_Right", "VRM_DrMOS_Array", "1", "24-Phase VRM DrMOS Array for V_core 0.8V / 1000A+", "Custom", "VRM-24PH-DRM"],
        ["J1", "PCIe_Slot_Top_1", "PCIe_x16_Slot", "1", "PCIe Gen6 x16 Card Edge Expansion Slot", "TE Connectivity", "2199230-4"],
        ["J2", "PCIe_Slot_Top_2", "PCIe_x16_Slot", "1", "PCIe Gen6 x16 Card Edge Expansion Slot", "TE Connectivity", "2199230-4"],
        ["J3", "PCIe_Slot_Top_3", "PCIe_x16_Slot", "1", "PCIe Gen6 x16 Card Edge Expansion Slot", "TE Connectivity", "2199230-4"],
        ["J4", "PCIe_Slot_Top_4", "PCIe_x16_Slot", "1", "PCIe Gen6 x16 Card Edge Expansion Slot", "TE Connectivity", "2199230-4"],
        ["J5", "PCIe_Slot_Bot_1", "PCIe_x16_Slot", "1", "PCIe Gen6 x16 Card Edge Expansion Slot", "TE Connectivity", "2199230-4"],
        ["J6", "PCIe_Slot_Bot_2", "PCIe_x16_Slot", "1", "PCIe Gen6 x16 Card Edge Expansion Slot", "TE Connectivity", "2199230-4"],
        ["J7", "PCIe_Slot_Bot_3", "PCIe_x16_Slot", "1", "PCIe Gen6 x16 Card Edge Expansion Slot", "TE Connectivity", "2199230-4"],
        ["J8", "PCIe_Slot_Bot_4", "PCIe_x16_Slot", "1", "PCIe Gen6 x16 Card Edge Expansion Slot", "TE Connectivity", "2199230-4"],
        ["J9", "DDR5_DIMM_1", "DDR5_DIMM_288pin", "1", "DDR5 288-pin Vertical DIMM Socket", "TE Connectivity", "2309413-1"],
        ["J10", "DDR5_DIMM_2", "DDR5_DIMM_288pin", "1", "DDR5 288-pin Vertical DIMM Socket", "TE Connectivity", "2309413-1"],
        ["J11", "DDR5_DIMM_3", "DDR5_DIMM_288pin", "1", "DDR5 288-pin Vertical DIMM Socket", "TE Connectivity", "2309413-1"],
        ["J12", "DDR5_DIMM_4", "DDR5_DIMM_288pin", "1", "DDR5 288-pin Vertical DIMM Socket", "TE Connectivity", "2309413-1"],
        ["J13", "NVMe_Storage_Left_1", "NVMe_M2_Socket", "1", "NVMe M.2 2280 Key-M Socket", "Amphenol", "MDT420E01001"],
        ["J14", "NVMe_Storage_Left_2", "NVMe_M2_Socket", "1", "NVMe M.2 2280 Key-M Socket", "Amphenol", "MDT420E01001"],
        ["J15", "NVMe_Storage_Right_1", "NVMe_M2_Socket", "1", "NVMe M.2 2280 Key-M Socket", "Amphenol", "MDT420E01001"],
        ["J16", "NVMe_Storage_Right_2", "NVMe_M2_Socket", "1", "NVMe M.2 2280 Key-M Socket", "Amphenol", "MDT420E01001"],
        ["J17", "Power_Input_1", "Power_Input_Connector", "1", "12V High-Current Power Input (1000A+ capable)", "Molex", "1720640016"],
        ["J18", "Power_Input_2", "Power_Input_Connector", "1", "12V High-Current Power Input (1000A+ capable)", "Molex", "1720640016"],
    ]
    
    # Add bypass caps
    for i in range(1, 17):
        bom.append([f"C{i}", "100nF/10uF", "C_0402_1005Metric", "1", "Bypass/Decoupling Capacitor", "Murata", "GRM155R71C104KA88"])
    
    filepath = os.path.join(OUTDIR, "TFLN_AI_NODE_X2_BOM.csv")
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(bom)
    print(f"  BOM: {filepath}")


def generate_centroid():
    """Generate component placement / centroid file (.pos)."""
    # Header
    lines = [
        "### Component Placement / Centroid File ###",
        "### Project: TFLN_AI_NODE_X2",
        "### Date: 2026-04-12",
        "### Units: mm",
        "### Format: Ref, Val, Package, PosX, PosY, Rot, Side",
        "## Ref,Val,Package,PosX,PosY,Rot,Side",
    ]
    
    # Component placements (matching gen_pcb.py positions)
    BOARD_W = 305.0
    BOARD_H = 280.0
    ORIGIN_X = 50.0
    ORIGIN_Y = 50.0
    cx = ORIGIN_X + BOARD_W / 2.0
    cy = ORIGIN_Y + BOARD_H / 2.0
    
    placements = [
        ("U1", "AI_Compute_Unit_1", "BGA256_0.8mm", cx-45, cy-15, 0, "top"),
        ("U2", "AI_Compute_Unit_2", "BGA256_0.8mm", cx+45, cy-15, 0, "top"),
        ("U3", "TFLN_Photonic_Engine_1", "TFLN_Photonic_Hybrid", cx-45, cy+15, 0, "top"),
        ("U4", "TFLN_Photonic_Engine_2", "TFLN_Photonic_Hybrid", cx+45, cy+15, 0, "top"),
        ("U5", "VRM_Array_Top_Left", "VRM_DrMOS_Array", cx-70, cy-55, 0, "top"),
        ("U6", "VRM_Array_Top_Right", "VRM_DrMOS_Array", cx+70, cy-55, 0, "top"),
        ("U7", "VRM_Array_Bot_Left", "VRM_DrMOS_Array", cx-70, cy+55, 0, "top"),
        ("U8", "VRM_Array_Bot_Right", "VRM_DrMOS_Array", cx+70, cy+55, 0, "top"),
    ]
    
    # PCIe slots
    for i in range(4):
        x = ORIGIN_X + 40 + i * 70
        placements.append((f"J{i+1}", f"PCIe_Slot_Top_{i+1}", "PCIe_x16_Slot", x, ORIGIN_Y+25, 0, "top"))
    for i in range(4):
        x = ORIGIN_X + 40 + i * 70
        placements.append((f"J{i+5}", f"PCIe_Slot_Bot_{i+1}", "PCIe_x16_Slot", x, ORIGIN_Y+BOARD_H-25, 180, "top"))
    
    # DDR5 DIMMs
    placements.append(("J9", "DDR5_DIMM_1", "DDR5_DIMM_288pin", cx-90, cy-10, 90, "top"))
    placements.append(("J10", "DDR5_DIMM_2", "DDR5_DIMM_288pin", cx-90, cy+10, 90, "top"))
    placements.append(("J11", "DDR5_DIMM_3", "DDR5_DIMM_288pin", cx+90, cy-10, 90, "top"))
    placements.append(("J12", "DDR5_DIMM_4", "DDR5_DIMM_288pin", cx+90, cy+10, 90, "top"))
    
    # NVMe
    placements.append(("J13", "NVMe_Left_1", "NVMe_M2_Socket", ORIGIN_X+20, cy-30, 0, "top"))
    placements.append(("J14", "NVMe_Left_2", "NVMe_M2_Socket", ORIGIN_X+20, cy+30, 0, "top"))
    placements.append(("J15", "NVMe_Right_1", "NVMe_M2_Socket", ORIGIN_X+BOARD_W-20, cy-30, 0, "top"))
    placements.append(("J16", "NVMe_Right_2", "NVMe_M2_Socket", ORIGIN_X+BOARD_W-20, cy+30, 0, "top"))
    
    # Power
    placements.append(("J17", "Power_Input_1", "Power_Input_Connector", cx-50, ORIGIN_Y+BOARD_H-15, 0, "top"))
    placements.append(("J18", "Power_Input_2", "Power_Input_Connector", cx+50, ORIGIN_Y+BOARD_H-15, 0, "top"))
    
    for ref, val, pkg, px, py, rot, side in placements:
        lines.append(f"{ref},{val},{pkg},{px:.3f},{py:.3f},{rot},{side}")
    
    filepath = os.path.join(OUTDIR, "TFLN_AI_NODE_X2_centroid.pos")
    with open(filepath, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"  Centroid: {filepath}")


def generate_drill_summary():
    """Generate drill file summary."""
    content = """; TFLN_AI_NODE_X2 Drill Summary
; Date: 2026-04-12
; Units: mm
; Format: Excellon
; 
; ============================================
; PLATED THROUGH-HOLES (PTH)
; ============================================
; Tool  Diameter  Count   Description
; T01   0.40mm    2304    DDR5 DIMM pin holes (288 x 4 sides x 2 rows)
; T02   0.50mm    1312    PCIe x16 slot pins (164 x 8 slots)
; T03   0.30mm    5000+   Signal vias (general)
; T04   0.25mm    2000+   High-speed signal vias (DDR5, PCIe Gen6)
; T05   0.10mm    1000+   Microvias (BGA fanout)
; T06   1.50mm    32      Power connector pins (16 x 2 connectors)
; T07   2.40mm    8       DDR5 DIMM mounting holes
; T08   2.80mm    16      PCIe slot retention posts
;
; ============================================
; NON-PLATED THROUGH-HOLES (NPTH)
; ============================================
; Tool  Diameter  Count   Description
; T09   3.20mm    4       Board mounting holes (corners)
; T10   2.00mm    8       Alignment/tooling holes
;
; ============================================
; BACK-DRILL SPECIFICATIONS
; ============================================
; Type          Impedance  Target Layer    Drill From   Depth
; PCIe Gen6     100 ohm    L4/L18         Bottom       To within 0.2mm of target
; TFLN RF       85 ohm     L1 (F.Cu)      Bottom       To within 0.2mm of target  
; DDR5          100 ohm    L6/L16         Bottom       To within 0.2mm of target
;
; NOTE: Back-drill zones are marked on User.1 layer in PCB file.
;       Fab house must identify vias within marked zones for stub removal.
;
; ============================================
; TOTAL HOLE COUNT: ~12,000+
; ============================================
"""
    filepath = os.path.join(OUTDIR, "TFLN_AI_NODE_X2_drill_summary.txt")
    with open(filepath, "w") as f:
        f.write(content)
    print(f"  Drill Summary: {filepath}")


def generate_fab_notes():
    """Generate fabrication notes / README for the fab pack."""
    content = """# TFLN_AI_NODE_X2 - Fabrication Package
## LightRail AI / LightOS

### Project Information
- **Board Name**: TFLN_AI_NODE_X2
- **Revision**: 1.0
- **Date**: 2026-04-12
- **KiCad Version**: 8.0.9
- **Board Size**: 305mm x 280mm
- **Layer Count**: 22 layers
- **Board Thickness**: 3.2mm
- **Copper Finish**: ENIG (Electroless Nickel Immersion Gold)
- **Solder Mask**: Green (both sides)
- **Silkscreen**: White (both sides)
- **Min Trace Width**: 0.08mm
- **Min Clearance**: 0.10mm
- **Min Drill**: 0.10mm (microvia)

### Layer Stackup (22 Layers)
| Layer | KiCad Name | Function | Copper Weight |
|-------|-----------|----------|---------------|
| L1 | F.Cu | Signal + TFLN Cavity | 1oz |
| L2 | In1.Cu | GND: Solid reference plane | 1oz |
| L3 | In2.Cu | V-Core: Heavy copper pour | **2oz** |
| L4 | In3.Cu | Signal: PCIe Gen6 Routing | 1oz |
| L5 | In4.Cu | GND: Reference plane | 1oz |
| L6 | In5.Cu | Signal: DDR5 DQ routing | 1oz |
| L7 | In6.Cu | Power: V_IO 1.1V | **2oz** |
| L8 | In7.Cu | Signal: General routing | 1oz |
| L9 | In8.Cu | GND: Reference plane | 1oz |
| L10 | In9.Cu | Signal: General routing | 1oz |
| L11 | In10.Cu | Signal: Mid-board high-speed crossover | 1oz |
| L12 | In11.Cu | Signal: Mid-board high-speed crossover | 1oz |
| L13 | In12.Cu | GND: Reference plane | 1oz |
| L14 | In13.Cu | Signal: General routing | 1oz |
| L15 | In14.Cu | Power: V_DDQ 1.1V | **2oz** |
| L16 | In15.Cu | Signal: DDR5 routing | 1oz |
| L17 | In16.Cu | GND: Reference plane | 1oz |
| L18 | In17.Cu | Signal: PCIe Gen6 routing | 1oz |
| L19 | In18.Cu | Power: 3.3V auxiliary | **2oz** |
| L20 | In19.Cu | GND: Solid reference plane | 1oz |
| L21 | In20.Cu | Signal: Bottom routing | 1oz |
| L22 | B.Cu | Signal + Power | 1oz |

### Net Classes / Design Rules
| Net Class | Clearance | Trace Width | Diff Pair Width | Diff Pair Gap |
|-----------|-----------|-------------|-----------------|---------------|
| Default | 0.15mm | 0.2mm | N/A | N/A |
| DDR5_DQ | 0.12mm | 0.1mm | 0.1mm | 0.15mm |
| PCIe_Gen6 | 0.12mm | 0.12mm | 0.12mm | 0.18mm |
| TFLN_RF | 0.2mm | 0.15mm | 0.15mm | 0.25mm |

### Impedance Control
| Signal Type | Impedance | Topology | Reference Layer |
|------------|-----------|----------|-----------------|
| TFLN RF | 85 ohm | Differential | L2 (GND) |
| PCIe Gen6 | 100 ohm | Differential | L2/L5 (GND) |
| DDR5 DQ | 100 ohm | Differential | L5/L7 (GND/PWR) |
| General | 50 ohm | Single-ended | Adjacent GND |

### Back-Drill Requirements
**CRITICAL**: The following signal vias require back-drilling for stub removal:
1. **PCIe Gen6 vias** (100-ohm): Drill from bottom, target layers L4/L18
2. **TFLN RF vias** (85-ohm): Drill from bottom, target layer L1 (F.Cu) ONLY
3. **DDR5 vias** (100-ohm): Drill from bottom, target layers L6/L16

Back-drill zones are clearly marked on the **User.1** layer in the PCB file.
Back-drill depth tolerance: Within 0.2mm of the target signal layer.

### Power Delivery
- **V_core**: 0.8V, 1000A+ (4x 24-phase VRM DrMOS arrays)
- **V_IO**: 1.1V
- **V_DDQ**: 1.1V (DDR5)
- **V_3V3**: 3.3V auxiliary
- **VIN**: 12V input (2x high-current connectors)

### Thermal Relief
- VRM DrMOS pads: **SOLID** connection (no thermal relief) for maximum current flow
- Power plane connections: Solid fill, no thermal spokes
- Signal component pads: Standard thermal relief (0.3mm gap, 0.4mm spoke)

### Fab Output Files
| File | Format | Description |
|------|--------|-------------|
| `TFLN_AI_NODE_X2_BOM.csv` | CSV | Bill of Materials |
| `TFLN_AI_NODE_X2_centroid.pos` | Centroid | Component placement for assembly robots |
| `TFLN_AI_NODE_X2_drill_summary.txt` | Text | Drill specifications and back-drill instructions |
| `TFLN_AI_NODE_X2.kicad_pcb` | KiCad PCB | Full PCB layout (use File > Plot for Gerbers) |

### Gerber Generation Instructions
In KiCad PCB Editor:
1. **Plot Gerbers** (File > Plot or F8):
   - Use **Protel** naming conventions
   - Select all 22 copper layers + mask + silk + Edge.Cuts
   - Output directory: `fab_outputs/`
   - Enable: Use Gerber extensions, Subtract mask from silk, Use extended attributes
2. **Generate Drill Files** (File > Plot > Generate Drill Files):
   - Map both **PTH** and **NPTH** separately
   - Format: Excellon
   - Units: mm
   - Zeros format: Decimal

### Assembly Notes
1. AI Compute Units (U1, U2) require X-ray inspection after BGA reflow
2. TFLN Photonic Engines (U3, U4) require fiber array unit (FAU) alignment post-assembly
3. Optical keep-out zones on U3/U4 footprints must remain clear of solder paste
4. VRM arrays require high-current reflow profile (peak temp ~260C, extended soak)
"""
    filepath = os.path.join(OUTDIR, "FAB_NOTES_README.md")
    with open(filepath, "w") as f:
        f.write(content)
    print(f"  Fab Notes: {filepath}")


def main():
    print("Generating fabrication output files:")
    generate_bom()
    generate_centroid()
    generate_drill_summary()
    generate_fab_notes()
    print("All fab outputs generated!")


if __name__ == "__main__":
    main()
