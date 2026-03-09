# LightRail Gen3: Assembly & Testing Instructions

## 1. Assembly Instruction Drawing (Overview)
**Project**: LightRail AI 26-Layer Photonic Interconnect
**Form Factor**: PCIe x16 Standard (167mm x 111mm)

### Component Placement Overview
- **U1 (Center)**: NCE AI Intelligence Stack (BGA-324). Mounted on Top layer.
- **U2 (North-West)**: LightRail DFB Laser Source.
- **OT0-OT7 (Periphery)**: TFLN Optical Modulator Tiles. Face-to-Face bonding required for photonic alignment.
- **C1-C2055**: High-density decoupling capacitor grid. Standard 0402/0603 footprint.
- **J1 (Bottom Edge)**: PCIe Gen5 x16 Gold Fingers.

### Critical Assembly Notes
1. **Z-Height Control**: The 26-layer stackup is 2.0mm thick. Ensure pick-and-place height is calibrated.
2. **Surface Finish**: ENIG (Electroless Nickel Immersion Gold) is used on all pads. Handle with clean-room gloves to avoid contamination of the TFLN modulators.
3. **Reflow Profile**: Use SAC305 Lead-Free profile. Max peak temp 245°C.

## 2. IC Programming & Firmware
- **U1 (AI Core)**: SPI Flash header located at J4.
- **Firmware**: `LightRail_v4.0_Production.bin`
- **Programming Interface**: Use Standard JTAG/SPI Programmer.
- **Target OS**: LightRail OS v4.1 (Kernel 5.15-photonic).

## 3. Functional Testing Procedure (Post-Assembly)

### Phase 1: Electrical Validation
- Check impedance on RF layers (L1, L3). Target single-ended 50Ω, differential 85Ω (±10%).
- Boundary Scan (JTAG): Verify connectivity on all 324 BGA pads of U1.

### Phase 2: Power-On Stress Test
- Apply 12V via PCIe connector.
- Verify 1.0V (AI Core), 1.8V (LDO), and 3.3V (VCC) rails.
- Current draw should not exceed 12A at peak inference (150W peak).

### Phase 3: Photonic & RF Validation
- **Optical Loopback**: Inject 1550nm C-band laser at OT0. Measure output at OT7. Max insertion loss < 3.0dB.
- **RF Sweep**: Sweep signal on TFLN electrodes from 1GHz to 100GHz. Verify Vpi < 1.9V.

### Phase 4: Full System Link
- Install in PCIe Gen5 slot.
- Run `lightrail-diag --full-test`.
- Passed criteria: Bit Error Rate (BER) < 1e-12.

---
**Document ID**: LR-G3-ASM-01
**Revision**: 3.2
**Date**: 2026-03-06
