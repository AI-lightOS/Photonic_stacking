import csv

def generate_20l_bom():
    bom_data = [
        ["Designator", "Description", "Manufacturer", "MPN", "Qty", "Function"],
        ["CORE1", "LightRail AI 20-Layer 3D Photonic Intelligence Stack", "LightRail-Fabrication", "LR-20L-INTEL-G1", "1", "Complete 20-Layer AI Compute Engine"],
        ["L1-Interposer", "Analog Power Interposer (1.5kW+ Embedded Regulators)", "LightRail-Power", "LR-PWR-L1-1.5KW", "1", "Phase 1: Analog Power Base Layer"],
        ["L2-Engine", "Integrated Light Engine (Heterogeneous DFB Laser Array)", "Lumentum", "LR-LHE-G2", "1", "Phase 1: Continuous Optical Power Supply"],
        ["L3-TFLN", "TFLN 3D Interposer (Co-Packaged Optics Substrate)", "LightRail-Optical", "LR-TFLN-800G", "1", "Phase 2: The Physical Fabric Foundation"],
        ["L7-Memristor", "Memristive Synaptic Grid (Analog Compute-in-Memory)", "LightRail-NV", "LR-MEM-BIOSYN", "1", "Phase 3: Analog Compute & Memory"],
        ["L9-Ternary", "Ternary Logic Encoder (-1, 0, +1)", "LightRail-Logic", "LR-TRIT-BASE3-ENC", "1", "Phase 4: Beyond Binary Logic Core"],
        ["C0-C2054", "0201 Ultra-Thin MLCC (0.1uF, 10V, X5R)", "Murata", "GRM033R61A104ME15D", "2055", "3D Decoupling nodes for Exascale 20L Stack"],
        ["J1", "PCIe Gen5 x16 Edge Interface", "TE Connectivity", "2013289-6", "1", "High-Speed Host Data Bridge"],
        ["Fab1", "20-Layer Rogers 4350B Hybrid Photonic Substrate", "LightRail-PCB", "LR-20L-HDI-PHASE7", "1", "The Exascale Photonic Intelligence Carrier"]
    ]
    
    output_file = "LightRail_20L_BOM.csv"
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(bom_data)
        
    print(f"Generated 20-Layer BOM: {output_file}")

if __name__ == "__main__":
    generate_20l_bom()
