# Fabrication Specification for LightRail AI TFLN Network Interface Card

## 1. PCB Stackup Design (20-Layer Hybrid RF/Optical)

**Layer 1 (Top Signal / Photonic Mount):** Rogers RO4350B. Impedance‑matched 50Ω single‑ended traces for RF drivers; dedicated physical channels for TFLN waveguide coupling.

**Layer 2 (GND Plane 1):** Solid copper reference for Layer 1.

**Layer 3 (High‑Speed RF):** 85Ω differential pairs for 100 Gbaud PAM4 lines connecting the SerDes (U9) to the TFLN Modulators (U1).

**Layer 4 (GND Plane 2):** RF shielding.

**Layers 5‑8 (Analog Power Interposer):** Dedicated analog power planes (1.8 V, 3.3 V) delivering clean, point‑of‑load voltage to the lasers and modulators, minimizing digital noise.

**Layers 9‑12 (Digital Routing):** PCIe Gen5 x16 logic, control signals (I²C, SPI), and telemetry routing.

**Layers 13‑16 (Digital Power & GND):** Digital power delivery for the central 3‑Trillion Transistor AI Engine and FPGA Controller.

**Layers 17‑18 (Secondary High‑Speed):** Secondary high‑speed routing for detector bank feedback.

**Layer 19 (GND Plane 3):** Bottom reference shield.

**Layer 20 (Bottom Signal):** Low‑speed peripherals, debug headers, and decoupling capacitor mounts.

## 2. Bill of Materials (BOM)

| Designator | Description | Manufacturer | Part Number | Qty |
|------------|-------------|--------------|-------------|-----|
| U_CORE | LightRail AI Compute Engine (3T Transistor, CPO Pluggable) | LightRail AI | LR‑AI‑CORE‑V1 | 1 |
| U1 | TFLN Mach‑Zehnder Modulator (100GHz BW, C‑band) | NTT Electronics | TFLN‑MZM‑400G‑C | 1 |
| U2 | DFB Laser Diode (1550nm, 100mW, C‑band) | NeoPhotonics | TLN‑1550‑100 | 1 |
| U3 | High‑Speed Photodetector (100GHz, InGaAs PIN) | Finisar / II‑VI | XPDV4120R | 1 |
| U4 | RF Driver IC (100GHz, 50Ω) | Analog Devices | HMC8410 | 1 |
| U5 | Laser Driver IC (2.5Gbps, auto power control) | Maxim Integrated | MAX3669 | 1 |
| U8 | TEC Controller (Thermoelectric cooler, ±5A) | Wavelength Elec. | MPT5000 | 1 |
| U9 | SerDes IC (400G PAM4, 100Gbaud, retimer) | Broadcom | BCM84881 | 1 |
| U10 | Clock Generator (100GHz, <50fs jitter) | Silicon Labs | Si5395A | 1 |
| OPT1 | Fiber‑to‑Chip Coupler (Single‑mode, <0.5dB loss) | Corning | FC‑TFLN‑SMF28 | 2 |
| J1 | PCIe Gen5 x16 Edge Connector | TE Connectivity | 2‑2013289‑6 | 1 |
| C41‑C2095 | MLCC Decoupling Capacitors (0.1µF, 25V, X7R, 0603) | Murata | GRM188R71E104KA01 | 2055 |

## 3. Component PIN Definitions & Topology‑Aware Wiring Map

- **Left Edge (Optical I/O):** MPO_Input and MPO_Output ports. Optical fibers route directly into the OPT1 couplers.
- **Top Left (Optical Power Generation):** Laser_Source (U2) mounted alongside the TEC_Driver (U8) for thermal stabilization. Continuous‑wave light is piped via Optical Waveguide (TFLN) into the modulator.
- **Center‑Left (Data Encoding):** Modulator_Arr (U1) receives light from the laser. RF_Driver (U4) converts electrical signals from the central chip into electro‑optic phase shifts inside the TFLN crystal.
- **Absolute Center (AI Engine):** Massive LightRail AI Core acts as the master node. Embedded Co‑Packaged Optics (CPO) socket. Electrical lanes (PAM4) from the core are ultra‑short (<2 cm) to the modulators.
- **Center‑Right (Detection):** Detector_Bank (U3) captures incoming light and converts it back to electrical data for the central processor.
- **Bottom Edge (Host Interface):** Controller (U9) near the bottom gold fingers to manage PCIe Gen5 traffic.

## 4. Visual Concept & Routing Diagram Prompt

**Visual Concept:** A high‑resolution, top‑down schematic view of the LightRail AI PCB. The board substrate is a dark, matte charcoal. In the center sits the massive "LightRail AI Core" chip with a pluggable CPO optical engine. Standard electrical traces (PCIe, power) are rendered as subtle, dark copper lines. The photonic routing dominates the visual: Thin‑Film Lithium Niobate (TFLN) waveguides are rendered as intensely glowing cyan and white beams. These luminous light beams split from the DFB laser modules on the top left, route through the central AI nodes for computation, and flow out to the detector banks on the right, visualizing instantaneous photonic data flow.

## 5. Fabrication File Set Manifest (For Export)

**Gerber Files (RS‑274X):**
- LightRail_Gen3_L01_Top.gbr … LightRail_Gen3_L20_Bottom.gbr
- LightRail_Gen3_SolderMask_Top.gbr / _Bot.gbr
- LightRail_Gen3_SilkScreen_Top.gbr / _Bot.gbr (featuring "LightRail AI" branding centered)
- LightRail_Gen3_SolderPaste_Top.gbr / _Bot.gbr
- LightRail_Gen3_Profile.gbr (board outline)

**NC Drill Files (Excellon):**
- LightRail_Gen3_PTH.drl (plated through‑holes)
- LightRail_Gen3_NPTH.drl (mounting holes for CPO socket/heatsink)
- LightRail_Gen3_Blind_L1_L3.drl (micro‑vias for RF routing)

**IPC‑356 Netlist:**
- LightRail_Gen3_BareBoard_Test.ipc (automated flying‑probe continuity testing)

**Pick and Place (XYRS):**
- LightRail_Gen3_Centroids.csv (X/Y coordinates and rotation for 2,095 components)

---
*This specification should be added to the repository on the `fabrication` branch as `fabrication_spec.md`.*
