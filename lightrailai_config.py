"""
LightRailAI CPO Interconnect - Technical Design Specifications
"""

# 1.1 Device Overview
DEVICE_TYPE = "Co-Packaged Optics (CPO) Network Interface Card (NIC) with Neural Compute Engine (NCE)"
FORM_FACTOR = "PCIe Gen5 x16 (Standard Height, Half Length)"
THROUGHPUT = "3.2 Tbps (8x 400G Lanes)"
POWER_ENVELOPE = "<15W Total Module Power (<1 pJ/bit optical efficiency)"

# 1.2 Critical Signal Integrity Specs
RF_BANDWIDTH = "100 GHz per lane"
IMPEDANCE_SERDES = "85Ω±5% (Differential)"
IMPEDANCE_MODULATOR = "50Ω±2% (Single-Ended RF)"
DIELECTRIC_RF = "Rogers 4350B"

# 2. PCB Fabrication Data
FAB_VENDOR = "Seeed Fusion / PCBWay (Advanced Rigid-Flex capability)"
MATERIAL_HYBRID = "Rogers RO4350B (RF) + High-Tg FR4 (Digital/Power)"
TOTAL_THICKNESS = "1.6mm ± 10%"
LAYERS = 15

STACKUP = [
    {"layer": "L1", "type": "Top Signal", "material": "Rogers 4350B", "function": "RF In/Out, TFLN Modulator Drive", "criticality": "CRITICAL (50Ω Edge Launch)"},
    {"layer": "L2", "type": "Ground", "material": "Copper", "function": "RF Reference Plane", "criticality": "Solid Plane (No splits under RF traces)"},
    {"layer": "L3", "type": "Signal", "material": "Rogers 4350B", "function": "High-Speed SerDes (Rx/Tx)", "criticality": "Differential Stripline (85Ω)"},
    {"layer": "L4", "type": "Ground", "material": "Copper", "function": "SerDes Reference", "criticality": "Solid Plane"},
    {"layer": "L5", "type": "Signal", "material": "FR4", "function": "Low-Speed Control (I2C, SPI, GPIO)", "criticality": "Non-Critical"},
    {"layer": "L6", "type": "Power", "material": "FR4", "function": "1.8V Rail (LDO Output)", "criticality": "Power Plane"},
    {"layer": "L7", "type": "Ground", "material": "Copper", "function": "Digital Ground", "criticality": "Solid Plane"},
    {"layer": "L8", "type": "Signal", "material": "FR4", "function": "NCE Neuron Interconnects", "criticality": "Dense Routing"},
    {"layer": "L9", "type": "Ground", "material": "Copper", "function": "Digital Ground", "criticality": "Solid Plane"},
    {"layer": "L10", "type": "Power", "material": "FR4", "function": "3.3V Rail (Main Power)", "criticality": "Power Plane"},
    {"layer": "L11", "type": "Signal", "material": "FR4", "function": "FPGA/Controller Fanout", "criticality": "Dense Routing"},
    {"layer": "L12", "type": "Ground", "material": "Copper", "function": "Analog Ground", "criticality": "Partitioned for sensitive analog"},
    {"layer": "L13", "type": "Power", "material": "FR4", "function": "-5V / 12V (Bias/TEC)", "criticality": "Power Plane"},
    {"layer": "L14", "type": "Ground", "material": "Copper", "function": "Bottom Reference", "criticality": "Solid Plane"},
    {"layer": "L15", "type": "Bottom Signal", "material": "FR4", "function": "Test Points, Debug Header", "criticality": "Assembly Access"},
]

# 3. Bill of Materials
BOM = [
    {"designator": "U1", "desc": "TFLN Mach-Zehnder Modulator (400G)", "mfr": "NTT Electronics", "mpn": "TFLN-MZM-400G-C", "qty": 1, "function": "The Core Photonic Engine", "dnp": True},
    {"designator": "U2", "desc": "DFB Laser Diode (1550nm, 100mW)", "mfr": "NeoPhotonics", "mpn": "TLN-1550-100", "qty": 1, "function": "Optical Source (C-Band)"},
    {"designator": "U3", "desc": "High-Speed Photodetector (100GHz)", "mfr": "Finisar", "mpn": "XPDV4120R", "qty": 1, "function": "O-E Conversion"},
    {"designator": "U4", "desc": "RF Driver IC (100GHz, Diff)", "mfr": "Analog Devices", "mpn": "HMC8410", "qty": 1, "function": "Amplifies SerDes to drive TFLN"},
    {"designator": "U9", "desc": "SerDes IC (400G PAM4 Retimer)", "mfr": "Broadcom", "mpn": "BCM84881", "qty": 1, "function": "Electrical Interface to PCIe"},
    {"designator": "U10", "desc": "Precision Clock Generator (Jitter <50fs)", "mfr": "Silicon Labs", "mpn": "Si5395A", "qty": 1, "function": "Timing reference for PAM4"},
    {"designator": "OPT1", "desc": "Fiber-to-Chip Coupler (PM)", "mfr": "Corning", "mpn": "FC-TFLN-SMF28", "qty": 2, "function": "Light injection/extraction", "dnp": True},
    {"designator": "J1", "desc": "PCIe Gen5 x16 Edge Connector", "mfr": "TE Connectivity", "mpn": "2-2013289-6", "qty": 1, "function": "Data/Power from Host"},
    {"designator": "J4-J7", "desc": "SMA RF Connectors (50GHz)", "mfr": "Amphenol", "mpn": "132289", "qty": 4, "function": "Lab Testing / Eye Diagram output"},
    {"designator": "PCB1", "desc": "15-Layer Rogers/Hybrid PCB", "mfr": "Advanced Circuits", "mpn": "CUSTOM-15L-RF", "qty": 1, "function": "The LightRailAI Board"},
]
