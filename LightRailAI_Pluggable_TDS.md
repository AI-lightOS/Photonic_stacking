# Technical Design Specification (TDS): LightRail AI Pluggable Interconnect

## 1. Overview
The "Antigravity" CPO/NCE Pluggable Interconnect is a high-performance network interface module designed for AI clusters. It integrates Thin-Film Lithium Niobate (TFLN) modulators on silicon photonics to achieve massive throughput with industry-leading efficiency.

## 2. Technical Specifications
- **Device Type**: Co-Packaged Optics (CPO) Pluggable Interconnect
- **Form Factor**: PCIe Gen5 x16 (Standard Height, Half Length)
- **Throughput**: 3.2 Tbps (8x 400G Lanes)
- **Modulation**: PAM4 (200 Gbaud) / PAM8 (267 Gbaud)
- **Optical Efficiency**: <1 pJ/bit
- **Power Envelope**: <15W Total

## 3. PCB Fabrication & Stack-Up (15-Layer Hybrid)
The board uses a hybrid material stack to balance high-frequency performance with digital routing density.

| Layer | Type | Material | Function | Impedance |
|-------|------|----------|----------|-----------|
| L1 | Top Signal | Rogers 4350B | RF I/O, TFLN Drive | 50Ω SE |
| L2 | Ground | Copper | RF Reference | - |
| L3 | Signal | Rogers 4350B | SerDes (Rx/Tx) | 85Ω Diff |
| L4 | Ground | Copper | SerDes Reference | - |
| L5 | Signal | FR4 | Low-Speed Control | - |
| L6 | Power | FR4 | 1.8V Rail | - |
| L7 | Ground | Copper | Digital Ground | - |
| L8 | Signal | FR4 | NCE Neuron Interconnects | - |
| L9 | Ground | Copper | Digital Ground | - |
| L10 | Power | FR4 | 3.3V Rail | - |
| L11 | Signal | FR4 | FPGA/Controller Fanout | - |
| L12 | Ground | Copper | Analog Ground | - |
| L13 | Power | FR4 | -5V / 12V (Bias/TEC) | - |
| L14 | Ground | Copper | Bottom Reference | - |
| L15 | Bottom Signal | FR4 | Test Points, Debug | - |

## 4. Bill of Materials (BOM) Highlights
| Designator | Component | MPN | Qty |
|------------|-----------|-----|-----|
| U1 | TFLN Mach-Zehnder Modulator | TFLN-MZM-400G-C | 1 |
| U2 | DFB Laser Diode (1550nm) | TLN-1550-100 | 1 |
| U9 | SerDes IC (400G Retimer) | BCM84881 | 1 |
| J1 | PCIe Gen5 x16 Edge Connector | TE 2-2013289-6 | 1 |

## 5. Manufacturing Notes
- **Vias**: Blind (L1-L2, L1-L3), Buried (L3-L12).
- **Plating**: ENIG (Electroless Nickel Immersion Gold).
- **RF Traces**: Must use Rogers 4350B dielectric for layers 1 and 3.
