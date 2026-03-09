# LightRail AI: Design Characteristics (26-Layer PCB)

This document outlines the technical specifications for the LightRail AI Photonic Accelerator PCB.

## Layer Stackup (26 Layers)

The board uses a high-density, 26-layer sequential buildup to support the Xilinx Kintex-7 FPGA, photonic modulators, and high-speed PCIe Gen5 interfaces.

| Layer | Type | Copper Thickness | Material | Dielectric Thickness |
|-------|------|------------------|----------|----------------------|
| 1 (F.Cu) | Signal | 35µm | FR4-High Tg | - |
| 2 (In1) | GND Plane | 35µm | Prepreg | 0.1mm |
| 3 (In2) | High-Speed Signal | 35µm | Core | 0.2mm |
| 4 (In3) | GND Plane | 35µm | Prepreg | 0.1mm |
| 5 (In4) | VCC_CORE (1.8V) | 70µm | Core | 0.3mm |
| 6-21 | Mixed | 35µm | Core/Prepreg | Variable |
| 22 (In21) | Power Plane | 35µm | Prepreg | 0.1mm |
| 23 (In22) | GND Plane | 35µm | Core | 0.2mm |
| 24 (In23) | High-Speed Signal | 35µm | Prepreg | 0.1mm |
| 25 (In24) | GND Plane | 35µm | Core | 0.2mm |
| 26 (B.Cu) | Signal | 35µm | - | - |

## Impedance Control

Targets are based on IPC-2141A standards for differential signaling and microstrip lines.

- **Single-Ended Signals**: 50Ω ± 10%
- **Differential Pairs (USB/PCIe/Optical)**: 100Ω ± 10%
- **Clock Lines**: 50Ω ± 5%

## Manufacturing Requirements

- **Material**: ISOLA 370HR (FR4-High Tg) or Megtron 6 (Ultra-low loss for 200Gbps paths).
- **Minimum Trace/Space**: 0.075mm (3 mil).
- **Minimum Via Drill**: 0.15mm (6 mil).
- **Surface Finish**: ENIG (Electroless Nickel Immersion Gold) recommended for BGA and Optical alignment.
