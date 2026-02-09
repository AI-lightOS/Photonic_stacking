import os
import zipfile

def package_deeppcb():
    output_zip = "DeepPCB_Project.zip"
    files_to_include = ["tfln_modulator.kicad_pcb", "tfln_modulator.kicad_pro"]
    
    print(f"Creating {output_zip} for DeepPCB upload...")
    
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_include:
            if os.path.exists(file):
                zipf.write(file, os.path.basename(file))
                print(f"  Added {file}")
            else:
                print(f"Error: {file} not found!")

    print(f"\n✅ DeepPCB Package created: {os.path.abspath(output_zip)}")

if __name__ == "__main__":
    package_deeppcb()
