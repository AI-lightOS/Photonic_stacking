# Photonic Stacking Project: Pin Arrangement

## PCIe Gen 5.0 x16 Interface (Edge Connector)
Standard PCIe pinout according to CEM specification.
- **A1-A11 / B1-B11**: Power & Sideband (PRSNT1#, WAKE#, CLKREQ#, etc.)
- **A12-A82 / B12-B82**: 16 High-Speed Differential Pairs (REFCLK, PERp/n[0:15], PETp/n[0:15])

## TFLN Modulator Controller (Internal)
Register-mapped I/O controls for photonic components:

| Register Address | Name | Description |
| :--- | :--- | :--- |
| `0xF0000000` | CONTROL | Main system reset and enable |
| `0xF0000008` | LASER_POWER | 12-bit DAC control for DFB Lasers (0-50mW) |
| `0xF000000C` | MOD_BIAS | Bias voltage for Mach-Zehnder Interferometers |
| `0xF0000010` | PHASE_0 | Phase shifter 0 adjustment (radians) |
| `0xF0000018` | WDM_SEL | Wavelength channel selector (0-63) |

## Optical Port Mapping
- **Ports 1-8**: TX Transmitters (TFLN Modulated Output)
- **Ports 9-16**: RX Receivers (Detector Input)
