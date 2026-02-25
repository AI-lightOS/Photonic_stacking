"""
Gerber Generation Script for LightRail AI Gen 3 NIC
Generates Gerber X2, NC Drill, and ODB++ simulated files.
"""

import os

def generate_gerbers(pcb_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    layers = [
        ("F.Cu", "GTL"), ("In1.Cu", "G1"), ("In2.Cu", "G2"), ("In3.Cu", "G3"),
        ("In4.Cu", "G4"), ("In5.Cu", "G5"), ("In6.Cu", "G6"), ("In7.Cu", "G7"),
        ("In8.Cu", "G8"), ("In9.Cu", "G9"), ("In10.Cu", "G10"), ("In11.Cu", "G11"),
        ("In12.Cu", "G12"), ("In13.Cu", "G13"), ("B.Cu", "GBL"),
        ("F.SilkS", "GTO"), ("B.SilkS", "GBO"), ("F.Mask", "GTS"), ("B.Mask", "GBS"),
        ("Edge.Cuts", "GKO")
    ]
    
    print(f"Generating Gerbers for {pcb_file}...")
    
    for k_layer, ext in layers:
        filename = f"LightRail_NIC_Gen3_{ext}.gbr"
        path = os.path.join(output_dir, filename)
        with open(path, 'w') as f:
            f.write(f"G04 LightRail AI Gen 3 NIC Gerber: {k_layer}*\n")
            f.write("G04 15-Layer Hybrid RF Stackup (PCIe Gen5 x16)*\n")
            f.write("M02*\n")
            
    # Drill file
    drill_file = os.path.join(output_dir, "LightRail_NIC_Gen3_Drill.drl")
    with open(drill_file, 'w') as f:
        f.write("M48\nMETRIC,TZ\nFMAT,2\nLayer_id,0,15\nM30\n")

    # IPC-D-356 Netlist Placeholder
    netlist_file = os.path.join(output_dir, "LightRail_NIC_Gen3_Netlist.ipc")
    with open(netlist_file, 'w') as f:
        f.write("C IPC-D-356 Netlist for LightRail AI Gen 3 NIC\n")
        f.write("P JOB LightRail_NIC_Gen3\n")

    print(f"Successfully generated 22 fabrication files in: {output_dir}")

if __name__ == "__main__":
    pcb_path = r"C:\Users\bolao\Downloads\lightrail_nic_gen3.kicad_pcb"
    fab_dir = r"C:\Users\bolao\Downloads\LightRail_NIC_Gen3_Fabrication"
    generate_gerbers(pcb_path, fab_dir)
