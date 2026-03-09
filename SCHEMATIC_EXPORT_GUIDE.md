# LightRail AI: Schematic Export Guide

The design source includes native KiCad schematic files. Follow these steps to view or export the schematic for review or manufacturing.

## Source Files

- **Primary Schematic**: `CircuitMaker_Files/LightRail_NCE_MVP.kicad_sch`
- **Component Libraries**: Embedded within the `.kicad_sch` file (KiCad 7.0+ compatible).

## How to View

1. **Install KiCad**: Ensure you have KiCad 7.0 or newer installed (kicad.org).
2. **Open Project**: Open `tfln_modulator.kicad_pro` in the project root.
3. **Open Schematic**: Click on the "Schematic Editor" button or open the `.kicad_sch` file directly.

## How to Export PDF/SVG

From the KiCad Schematic Editor:
1. Go to **File > Plot**.
2. Select **PDF** or **SVG** as the output format.
3. Choose the output directory and click **Plot All Pages**.

## Characteristics Covered in Schematic

- **FPGA Bank Assignments**: High-speed SerDes mapping for PCIe and Optical buffers.
- **Power Delivery Network (PDN)**: Buck converter architectures for 1.8V and 3.3V rails.
- **Optical Front-End**: Transimpedance amplifiers (TIA) and Mach-Zehnder modulator drivers.
- **Micro-control**: USB-C interface and SPI/I2C sensor mesh.
