import os
import zipfile

def package_project_explicit():
    root = "c:\\Users\\bolao\\.gemini\\antigravity\\scratch\\Photonic_stacking"
    target_zip = "LightRail_AI_Source_Project.zip"
    
    # Define files we DEFINITELY want to include based on previous find output
    primary_files = [
        "tfln_modulator.kicad_pcb",
        "tfln_modulator.kicad_pro",
        "tfln_modulator.dsn",
        "LightRail_AI.PrjPcb",
        "CircuitMaker_Files/tfln_modulator.kicad_pcb",
        "CircuitMaker_Files/LightRail_NCE_MVP.kicad_sch",
        "CircuitMaker_Files/LightRail_AI.PrjPcb",
        "LightRail_AI_Final/tfln_modulator.kicad_pcb",
        "LightRail_AI_Final/tfln_modulator.kicad_pro"
    ]
    
    with zipfile.ZipFile(target_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for rel_path in primary_files:
            abs_path = os.path.join(root, rel_path)
            if os.path.exists(abs_path):
                zf.write(abs_path, rel_path)
                print(f"Added: {rel_path}")
            else:
                print(f"Skipped (not found): {rel_path}")
    
    print(f"✅ Successfully packaged DESIGN SOURCE into {target_zip}")

if __name__ == "__main__":
    package_project_explicit()
