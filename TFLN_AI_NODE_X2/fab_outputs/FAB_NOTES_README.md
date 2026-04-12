# TFLN_AI_NODE_X2 - Fabrication Package
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
