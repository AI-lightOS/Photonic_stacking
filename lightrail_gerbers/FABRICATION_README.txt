LIGHTRAIL AI PLUGGABLE INTERCONNECT - FABRICATION PACKAGE
============================================================
Generated: 2026-02-17 09:19:17

STACKUP SPECIFICATIONS (TOP TO BOTTOM):
--------------------------------------------------------------------------------
Layer    | Name                 | Material        | Function
--------------------------------------------------------------------------------
L01      | L1_Top_RF            | Rogers 4350B    | Rogers 4350B - RF In/Out, TFLN Drive
L02      | L2_GND_RF            | High-Tg FR4     | Copper - RF Reference Plane
L03      | L3_SerDes            | Rogers 4350B    | Rogers 4350B - High-Speed SerDes (Rx/Tx)
L04      | L4_GND_SerDes        | High-Tg FR4     | Copper - SerDes Reference
L05      | L5_Control           | High-Tg FR4     | FR4 - Low-Speed Control (I2C, SPI, GPIO)
L06      | L6_Power_1V8         | High-Tg FR4     | FR4 - 1.8V Rail (LDO Output)
L07      | L7_GND_Dig           | High-Tg FR4     | Copper - Digital Ground
L08      | L8_NCE_Neuron        | High-Tg FR4     | FR4 - NCE Neuron Interconnects
L09      | L9_GND_Dig           | High-Tg FR4     | Copper - Digital Ground
L10      | L10_Power_3V3        | High-Tg FR4     | FR4 - 3.3V Rail (Main Power)
L11      | L11_Fanout           | High-Tg FR4     | FR4 - FPGA/Controller Fanout
L12      | L12_GND_Analog       | High-Tg FR4     | Copper - Analog Ground
L13      | L13_Power_Bias       | High-Tg FR4     | FR4 - -5V / 12V (Bias/TEC)
L14      | L14_GND_Bot          | High-Tg FR4     | Copper - Bottom Reference
L15      | L15_Bot_Signal       | High-Tg FR4     | FR4 - Test Points, Debug Header
--------------------------------------------------------------------------------

CRITICAL MANUFACTURING NOTES:
1. IMPEDANCE CONTROL: L1 (50 ohm SE), L3 (85 ohm DIFF).
2. BLIND VIAS: L1-L2, L1-L3.
3. PLATING: ENIG required for wire-bonding.
4. DIELECTRIC: Layers 1-2 and 3-4 MUST use Rogers 4350B cores.
