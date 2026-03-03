import os
import zipfile

def create_final_fabrication_package():
    output_zip = "LightRail_AI_Complete_Fabrication_V3.zip"
    gerber_dir = "gerber_files"
    
    # List of files to include from the root
    root_files = [
        "tfln_modulator.kicad_pcb",
        "tfln_modulator.kicad_pro",
        "tfln_modulator.dsn",
        "tfln_modulator.net",
        "BOM.csv",
        "CPL.csv",
        "TFLN_BOM.csv",
        "TFLN_BOM_Summary.txt",
        "TFLN_Technical_Report.docx",
        "TFLN_System_Diagram.png",
        "DESIGN_PACKAGE_SUMMARY.md",
        "DeepPCB_Project.zip"
    ]
    
    print(f"Creating {output_zip}...")
    
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add root files
        for file in root_files:
            if os.path.exists(file):
                zipf.write(file, file)
                print(f"  Added {file}")
            else:
                print(f"Warning: {file} not found!")

        # Add Gerber directory
        if os.path.exists(gerber_dir):
            for foldername, subfolders, filenames in os.walk(gerber_dir):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    # Add file to zip, preserving relative path
                    zipf.write(file_path, file_path)
                    print(f"  Added {file_path}")
        else:
            print(f"Warning: {gerber_dir} not found!")

    print(f"\n✅ Complete Fabrication Package created: {os.path.abspath(output_zip)}")

if __name__ == "__main__":
    create_final_fabrication_package()
