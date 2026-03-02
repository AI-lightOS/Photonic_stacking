# Photonic Stacking Project: Netlist

## Logical Signal Architecture

### 1. High-Speed Optical Data Path
- **OPT_IN [0:15]** -> Fiber-Chip Coupling -> TFLN Waveguide Array
- **TFLN Waveguide [0:15]** -> Mach-Zehnder Modulators -> **OPT_OUT [0:15]**

### 2. Control & Readout Signals
- **HOST_PCIE_GEN5_X16** <-> DMA Engine (8 Channels)
- **DMA_DATA_BUS** <-> Hybrid FPGA Fabric
- **FPGA_GPIO [0:63]** -> TFLN Modulator Biasing/RF Drive
- **DETECTOR_ANALOG [0:63]** -> Transimpedance Amplifiers (TIA) -> FPGA ADC

## Power Network
- **+12V (PCIe)** -> DC-DC Converter Array
- **+3.3V** -> Laser Diode Drivers, FPGA I/O
- **+1.8V** -> High-Speed TFLN Driver Circuitry
- **GND** -> Solid Reference Plane (Layer 2)
