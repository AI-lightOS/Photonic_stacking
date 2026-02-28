"""
BOM and Pick & Place Generation for LightRail AI Gen 3 NIC
Generates CSV files for the 2,095 components.
"""

import csv
import os

def generate_bom_nic_gen3():
    bom_data = [
        ["Designator", "Description", "Manufacturer", "MPN", "Qty", "Footprint"],
        ["U1", "TFLN-MZM-400G-C Modulator Array", "LightRail-Optical", "LR-TFLN-MZM-400G", "1", "TFLN_MZM_400G"],
        ["U2", "DFB Laser Source (CW-C-Band)", "Lumentum", "LR-DFB-C-BAND", "1", "DFB_Laser_U2"],
        ["U3", "Sub-micron Waveguide Routing Core", "LightRail-Silicon", "LR-OPT-CORE-G3", "1", "Optical_Core_U3"],
        ["U4", "XPDV4120R High-Speed Photodetector Bank", "Finisar", "XPDV4120R", "1", "Detector_Bank_U4"],
        ["U8", "MPT5000 TEC Driver", "Melexis", "MPT5000", "1", "TEC_Driver_U8"],
        ["U9", "BCM84881 Controller (FPGA/SerDes)", "Broadcom", "BCM84881", "1", "BCM84881_BGA"],
        ["J1", "PCIe Gen5 x16 Edge Connector", "TE Connectivity", "2013289-6", "1", "PCIe_x16_Edge"],
        ["MPO1", "MPO Input Fiber Array Connector", "US Conec", "MPO-12-IN", "1", "MPO_Array"],
        ["MPO2", "MPO Output Fiber Array Connector", "US Conec", "MPO-12-OUT", "1", "MPO_Array"]
    ]
    
    # Add 2055 decoupling capacitors
    for i in range(2055):
        bom_data.append([f"C{i+1}", "0603 MLCC 0.1uF 10V X5R", "Murata", "GRM188R61A104KA01D", "1", "C_0603_1608Metric"])

    bom_file = "LightRail_NIC_Gen3_BOM.csv"
    with open(bom_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(bom_data)
        
    # Pick & Place
    pnp_data = [["Designator", "X", "Y", "Layer", "Rotation"]]
    pnp_data.append(["U1", "35", "55", "Top", "0"])
    pnp_data.append(["U2", "30", "20", "Top", "0"])
    pnp_data.append(["U3", "83.5", "55", "Top", "0"])
    pnp_data.append(["U4", "120", "55", "Top", "0"])
    pnp_data.append(["U8", "50", "20", "Top", "0"])
    pnp_data.append(["U9", "83.5", "85", "Top", "0"])
    
    pnp_file = "LightRail_NIC_Gen3_PNP.csv"
    with open(pnp_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(pnp_data)

    print(f"Generated BOM: {bom_file}")
    print(f"Generated PNP: {pnp_file}")

if __name__ == "__main__":
    generate_bom_nic_gen3()
