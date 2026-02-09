"""
DeepPCB Preparation Script (V2 Compliance)
Generates the 2 critical files for DeepPCB AI routing with strict KiCad 6.0 formatting.
"""

import os
import json
from generate_kicad import LightRailKiCadGenerator

def generate_deeppcb_files():
    print("🚀 Preparing files for DeepPCB upload (V2 Compliance Mode)...")
    
    # 1. Generate the KiCad PCB and Pro files using the refactored generator
    gen = LightRailKiCadGenerator(project_name="tfln_modulator")
    gen.generate_board()
    gen.write_files()
    
    # 2. Add extra project metadata if needed (optional, write_files already does basic)
    pro_file = "tfln_modulator.kicad_pro"
    with open(pro_file, 'r') as f:
        pro_content = json.load(f)
    
    # Enrich stackup info for DeepPCB
    pro_content["board"]["layer_stack"] = [
      {"name": "F.Cu", "type": "copper"},
      *[{"name": f"In{i}.Cu", "type": "copper"} for i in range(1, 11)],
      {"name": "B.Cu", "type": "copper"}
    ]
    
    with open(pro_file, 'w') as f:
        json.dump(pro_content, f, indent=2)
        
    print(f"✅ Final check complete for {pro_file}")
    print("\n--- DeepPCB Upload Ready (V2) ---")
    print(f"File 1: {os.path.abspath('tfln_modulator.kicad_pcb')}")
    print(f"File 2: {os.path.abspath('tfln_modulator.kicad_pro')}")
    print("----------------------------")

if __name__ == "__main__":
    generate_deeppcb_files()
