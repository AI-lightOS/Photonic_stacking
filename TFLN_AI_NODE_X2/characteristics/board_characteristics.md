# TFLN_AI_NODE_X2 Board Characteristics

## 1. Physical Dimensions
| Parameter | Value |
|-----------|-------|
| Board Width | 305 mm (12.01") |
| Board Height | 280 mm (11.02") |
| Board Thickness | 3.2 mm (126 mil) |
| Layer Count | 22 copper layers |
| Surface Finish | ENIG (Electroless Nickel Immersion Gold) |
| Solder Mask | LPI (both sides), green |
| Silkscreen | White (both sides) |
| Board Material | Megtron 6 / FR4 hybrid |
| Copper Weight | 1oz standard, 2oz on power planes (L3, L7, L15, L19) |

## 2. Layer Stackup

| Layer | Name | Type | Thickness | Description |
|-------|------|------|-----------|-------------|
| L1 | F.Cu | Signal | 35 um (1oz) | Top signal + TFLN cavity |
| - | Prepreg | Dielectric | 100 um | Megtron 6, Er=3.6 |
| L2 | In1.Cu | GND | 35 um (1oz) | Solid reference plane |
| - | Core | Dielectric | 100 um | FR4, Er=4.2 |
| L3 | In2.Cu | Power | 70 um (2oz) | V_CORE 0.8V heavy copper |
| - | Prepreg | Dielectric | 100 um | FR4, Er=4.2 |
| L4 | In3.Cu | Signal | 35 um (1oz) | PCIe Gen6 routing |
| - | Core | Dielectric | 100 um | Megtron 6, Er=3.6 |
| L5 | In4.Cu | GND | 35 um (1oz) | Reference plane |
| - | Prepreg | Dielectric | 100 um | FR4, Er=4.2 |
| L6 | In5.Cu | Signal | 35 um (1oz) | DDR5 routing |
| - | Core | Dielectric | 100 um | Megtron 6, Er=3.6 |
| L7 | In6.Cu | Power | 70 um (2oz) | V_IO 1.1V |
| - | Prepreg | Dielectric | 100 um | FR4, Er=4.2 |
| L8 | In7.Cu | Signal | 35 um (1oz) | General routing |
| - | Core | Dielectric | 100 um | FR4, Er=4.2 |
| L9 | In8.Cu | GND | 35 um (1oz) | Reference plane |
| - | Prepreg | Dielectric | 100 um | FR4, Er=4.2 |
| L10 | In9.Cu | Signal | 35 um (1oz) | General routing |
| - | Core | Dielectric | 100 um | FR4, Er=4.2 |
| L11 | In10.Cu | Signal | 35 um (1oz) | Mid-board crossover (top) |
| - | Prepreg | Dielectric | 100 um | FR4, Er=4.2 |
| L12 | In11.Cu | Signal | 35 um (1oz) | Mid-board crossover (bottom) |
| - | Core | Dielectric | 100 um | FR4, Er=4.2 |
| L13 | In12.Cu | GND | 35 um (1oz) | Reference plane |
| - | Prepreg | Dielectric | 100 um | FR4, Er=4.2 |
| L14 | In13.Cu | Signal | 35 um (1oz) | General routing |
| - | Core | Dielectric | 100 um | FR4, Er=4.2 |
| L15 | In14.Cu | Power | 70 um (2oz) | V_DDQ 1.1V |
| - | Prepreg | Dielectric | 100 um | FR4, Er=4.2 |
| L16 | In15.Cu | Signal | 35 um (1oz) | DDR5 routing (bottom) |
| - | Core | Dielectric | 100 um | Megtron 6, Er=3.6 |
| L17 | In16.Cu | GND | 35 um (1oz) | Reference plane |
| - | Prepreg | Dielectric | 100 um | FR4, Er=4.2 |
| L18 | In17.Cu | Signal | 35 um (1oz) | General routing |
| - | Core | Dielectric | 100 um | FR4, Er=4.2 |
| L19 | In18.Cu | Power | 70 um (2oz) | V_3V3 auxiliary |
| - | Prepreg | Dielectric | 100 um | FR4, Er=4.2 |
| L20 | In19.Cu | GND | 35 um (1oz) | Reference plane |
| - | Core | Dielectric | 100 um | FR4, Er=4.2 |
| L21 | In20.Cu | Signal | 35 um (1oz) | Bottom signal routing |
| - | Prepreg | Dielectric | 100 um | Megtron 6, Er=3.6 |
| L22 | B.Cu | Signal | 35 um (1oz) | Bottom signal + components |

## 3. Impedance Control

| Net Class | Trace Width | Clearance | Diff Pair Width | Diff Pair Gap | Target Z0 | Target Zdiff |
|-----------|-------------|-----------|-----------------|---------------|-----------|-------------|
| Default | 0.20 mm | 0.15 mm | N/A | N/A | 50 ohm | N/A |
| DDR5_DQ | 0.10 mm | 0.12 mm | 0.10 mm | 0.15 mm | 40 ohm | 80 ohm |
| PCIe_Gen6 | 0.12 mm | 0.12 mm | 0.12 mm | 0.18 mm | 42.5 ohm | 85 ohm |
| TFLN_RF | 0.15 mm | 0.20 mm | 0.15 mm | 0.25 mm | 50 ohm | 100 ohm |

## 4. Power Delivery Characteristics

### Power Rails
| Rail | Voltage | Max Current | Copper Weight | Planes |
|------|---------|-------------|---------------|--------|
| V_CORE | 0.8V | 1200A | 2oz | L3 (In2.Cu) |
| V_IO | 1.1V | 200A | 2oz | L7 (In6.Cu) |
| V_DDQ | 1.1V | 100A | 2oz | L15 (In14.Cu) |
| V_3V3 | 3.3V | 50A | 2oz | L19 (In18.Cu) |
| GND | 0V | Return | 1oz | L2, L5, L9, L13, L17, L20 |

### VRM Specifications (per array)
| Parameter | Value |
|-----------|-------|
| Topology | Multi-phase synchronous buck |
| Phases | 24 |
| Input Voltage | 12V |
| Switching Frequency | 600 kHz |
| Max Current per Phase | 50A |
| Efficiency | 92% typical |
| Thermal Relief | Solid (no spokes) |
| Ripple | < 5 mV p-p |

### Power Budget
| Component | Count | Power (W) |
|-----------|-------|-----------|
| AI Compute Unit | 2 | 2 x 400W = 800W |
| TFLN Photonic Engine | 2 | 2 x 15W = 30W |
| DDR5 DIMM | 4 | 4 x 12W = 48W |
| VRM Loss | 4 | 4 x 21W = 84W |
| NVMe | 4 | 4 x 8W = 32W |
| Misc (clocks, LEDs) | - | 6W |
| **Total** | - | **~1000W** |

## 5. Signal Integrity Parameters

### PCIe Gen6 (64 GT/s PAM4)
| Parameter | Target |
|-----------|--------|
| Data Rate | 64 GT/s (PAM4) |
| Lane Count | 16 per slot (8 slots) |
| Insertion Loss (12") | < 20 dB at 32 GHz |
| Return Loss | < -10 dB |
| Crosstalk (NEXT) | < -30 dB |
| Routing Layer | L4 (In3.Cu) |
| Via stub (max) | Back-drilled to < 5 mil |

### DDR5-4800
| Parameter | Target |
|-----------|--------|
| Data Rate | 4800 MT/s |
| Bus Width | 64-bit per DIMM |
| Topology | Point-to-point |
| Max Trace Length | 150 mm |
| Length Matching | +/- 2.5 mm intra-byte |
| Routing Layers | L6, L16 (In5.Cu, In15.Cu) |

### TFLN RF
| Parameter | Target |
|-----------|--------|
| Bandwidth | > 100 GHz |
| V_pi | 1.5V |
| Impedance | 100 ohm differential |
| Length Match (P/N) | +/- 0.05 mm |
| Routing | L1 (F.Cu) only, no vias |
| Max Loss | < 1 dB at 50 GHz |

## 6. Thermal Characteristics

| Parameter | Value |
|-----------|-------|
| Max Junction Temp (SoC) | 105 deg C |
| Ambient Operating Temp | 0 to 45 deg C |
| Airflow Requirement | > 50 CFM forced air |
| Heatsink Required | Yes, vapor chamber recommended |
| Thermal Vias (BGA) | 256 per BGA, 0.3mm drill |
| Power Plane Thermal Relief | Solid connection (VRM pads) |

## 7. Manufacturing Specifications

| Parameter | Value |
|-----------|-------|
| Min Trace Width | 0.08 mm (3.15 mil) |
| Min Clearance | 0.10 mm (3.94 mil) |
| Min Via Drill | 0.20 mm (7.87 mil) |
| Min Via Pad | 0.45 mm (17.7 mil) |
| Min Annular Ring | 0.125 mm (4.92 mil) |
| Aspect Ratio (max) | 16:1 |
| Solder Mask Registration | +/- 50 um |
| Silkscreen Min Width | 0.15 mm |
| Back-Drill Tolerance | +/- 100 um |
| Panel Size | 457 x 610 mm |
| Panelization | 1-up (board too large for multi-up) |

## 8. Reliability & Testing

| Test | Specification |
|------|--------------|
| IPC Class | Class 3 (high reliability) |
| Cross-section | Per IPC-6012 |
| Impedance Test | TDR, +/- 10% |
| Microsection | 3 coupons per panel |
| Ionic Contamination | < 1.56 ug NaCl/cm2 |
| Thermal Cycling | -40 to +125 deg C, 1000 cycles |
| CAF Testing | Per IPC-TM-650 2.6.25 |
