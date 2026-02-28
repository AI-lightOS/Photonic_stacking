import csv

def generate_cpo_bom():
    bom_data = [
        ["Designator", "Description", "Manufacturer", "MPN", "Qty", "Function"],
        ["U_CORE", "LightRail AI Neural Compute Engine (NCE) - CPO Core BGA", "LightRail-Semi", "LR-NCE-CPO-G3", "1", "Central AI Processing Unit"],
        ["OT0-OT7", "TFLN Optical Tiles (O-Tiles) - 400G Photonic Engine", "LightRail-Optical", "LR-OT-TFLN-G1", "8", "Multi-channel optical IO via CPO"],
        ["L0-L14", "High-Power Shielded Inductor (VRM Stage)", "TDK", "VLCF5028T-2R2N1R7", "15", "Multi-phase power for NCE Core"],
        ["C0-C419", "Ceramic Capacitor (0402, 1uF, 10V, X5R)", "Murata", "GRM155R61A105KE15D", "420", "Ultra-dense decoupling forest"],
        ["R0-R420", "Chip Resistor (0402, 50 Ohm, 1%)", "Vishay", "CRCW040250R0FKED", "421", "High-speed SerDes termination"],
        ["U_CLK", "Precision Clock Multiplier (Jitter <50fs)", "Skyworks", "Si5395A-A-GM", "1", "Multi-channel timing for 8 Tiles"],
        ["J1", "PCIe Gen5 x16 Edge Connector Gold-Fingers", "TE Connectivity", "2-2013289-6", "1", "Host Power/Data Interface"],
        ["PCB1", "15-Layer Rogers 4350B Hybrid HDI PCB", "Custom-Fab", "LR-CPO-15L-HDI", "1", "System Carrier Substrate"]
    ]
    
    output_file = "LightRail_CPO_BOM.csv"
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(bom_data)
        
    print(f"Generated {output_file} with {sum(int(row[4]) if row[4].isdigit() else 1 for row in bom_data[1:])} components.")

if __name__ == "__main__":
    generate_cpo_bom()
