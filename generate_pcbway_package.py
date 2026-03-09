import os
import shutil
import zipfile
import subprocess

def generate_pcbway_package():
    print("🚀 Initializing PCBWay Export Package...")
    
    # 1. Define Paths
    base_dir = r"c:\Users\bolao\.gemini\antigravity\scratch\Photonic_stacking"
    target_dir = os.path.join(base_dir, "PCBWay_Submission")
    gerber_source = os.path.join(base_dir, "gerber_files")
    output_zip = os.path.join(base_dir, "PCBWay_Project.zip")
    
    # Clean/Create target directory
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.makedirs(target_dir)
    os.makedirs(os.path.join(target_dir, "Gerbers"))
    
    print(f"📁 Created folder: {target_dir}")

    # 2. Run Generation Scripts to ensure latest data
    print("🔄 Regenerating Gerber and VLSI files...")
    scripts = ["generate_gerber.py", "generate_vlsi.py", "generate_manufacturing_data.py"]
    for script in scripts:
        script_path = os.path.join(base_dir, script)
        if os.path.exists(script_path):
            print(f"  Running {script}...")
            subprocess.run(["python", script_path], cwd=base_dir, check=True)

    # 3. Copy Gerber Files
    print("📌 Copying Gerber and Drill files...")
    if os.path.exists(gerber_source):
        for file in os.listdir(gerber_source):
            if file.endswith(('.gtl', '.gbl', '.gts', '.gbs', '.gto', '.gbo', '.gm1', '.drl', '.gbr', '.g1', '.g2', '.g3', '.g4', '.g5', '.g6', '.g7', '.g8', '.g9', '.g10', '.g11', '.g12', '.g13', '.g14')):
                shutil.copy2(os.path.join(gerber_source, file), os.path.join(target_dir, "Gerbers", file))
    
    # 4. Copy BOM and CPL files
    print("📊 Copying BOM and Assembly files...")
    bom_files = ["BOM.csv", "CPL.csv", "TFLN_BOM.csv", "LightRail_Centroid.csv"]
    for file in bom_files:
        src = os.path.join(base_dir, file)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(target_dir, file))
            print(f"  Added {file}")

    # 5. Create Design Summary for PCBWay
    summary_path = os.path.join(target_dir, "PCBWay_Design_Summary.txt")
    with open(summary_path, 'w') as f:
        f.write("Project: LightRail AI TFLN Photonic Modulator\n")
        f.write("Manufacturer: PCBWay Submission\n")
        f.write("Stackup: 15-Layer Hybrid (Copper/FR4/Rogers)\n")
        f.write("Units: Metric (mm)\n")
        f.write("Gerber Type: RS-274X\n")
        f.write("\nAlignment Note: VLSI Photonics and FPGA logic layers are aligned to the PCB center.\n")

    # 6. Create Zip Archive
    print(f"📦 Creating ZIP archive: {output_zip}...")
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # Create a relative path for the zip file header
                rel_path = os.path.relpath(file_path, target_dir)
                zipf.write(file_path, rel_path)

    print(f"\n✅ SUCCESS: PCBWay package ready in {target_dir}")
    print(f"📂 Zip created: {output_zip}")

if __name__ == "__main__":
    generate_pcbway_package()
