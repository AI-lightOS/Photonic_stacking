# TFLN Photonic Modulator PCB Design

## Overview
This repository contains the complete design files for a **12-layer TFLN (Thin-Film Lithium Niobate) Photonic Modulator** PCB, designed for high-speed optical interconnects in AI datacenter applications.

## Design Specifications
| Parameter | Value |
|-----------|-------|
| Layers | 12 (Signal/Power/Ground) |
| Board Size | 100mm x 80mm |
| Min Track Width | 0.2mm |
| Min Via | 0.6mm / 0.3mm drill |
| Material | Rogers RO4350B |
| Data Rate | 400G-800G |

## File Formats Available

### Manufacturing Files
- **Gerber Files** (`gerber_files/`) - RS-274X format for PCB fabrication
- **Drill File** (`tfln_modulator.drl`) - Excellon format
- **BOM** (`TFLN_BOM.csv`) - Bill of Materials

### Design Files (Editable)
- **KiCad** (`tfln_modulator.kicad_pro`, `tfln_modulator.kicad_pcb`) - Open in KiCad 6+
- **EasyEDA** (`tfln_modulator_easyeda.json`) - Import into EasyEDA

### Visualization
- **3D Stack View** (`pcb_stack_3d.png`)
- **Populated Board** (`pcb_populated_green_dense.png`)

## Layer Stackup
```
L1  - Top Copper (RF Signals)
L2  - Ground Plane
L3  - Signal (High-Speed)
L4  - Power (+3V3)
L5  - Signal
L6  - Ground Plane
L7  - Signal
L8  - Power (+1V8)
L9  - Signal
L10 - Ground Plane
L11 - Signal
L12 - Bottom Copper (Ground)
```

## Key Components
| Ref | Description | Manufacturer |
|-----|-------------|--------------|
| U1 | TFLN Mach-Zehnder Modulator | NTT Electronics |
| U2 | DFB Laser Diode (1550nm) | NeoPhotonics |
| U3 | High-Speed Photodetector | Finisar |
| U4 | RF Driver IC (100GHz) | Analog Devices |
| U9 | SerDes (400G PAM4) | Broadcom |
| J1 | PCIe x16 Edge Connector | TE Connectivity |

## Usage with Auto-Routers

### DeepPCB
1. Download `tfln_modulator.kicad_pro`
2. Import into DeepPCB
3. Run auto-routing

### KiCad (Manual)
1. Open `tfln_modulator.kicad_pro` in KiCad 6+
2. Use File → Export → Specctra DSN for external routers

### EasyEDA
1. Import `tfln_modulator_easyeda.json`
2. Edit and route online

## Scripts
- `generate_gerber.py` - Regenerate Gerber files
- `generate_kicad.py` - Regenerate KiCad project
- `generate_easyeda.py` - Generate EasyEDA JSON
- `generate_bom.py` - Generate Bill of Materials
- `visualize_pcb_dense.py` - Render high-density PCB image

## License
MIT License - Free for commercial and personal use.

## Contact
LightRail AI - Photonic Computing Division
