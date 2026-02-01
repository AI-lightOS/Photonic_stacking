import os
import zipfile
import glob

def create_manufacturer_package():
    output_zip = "manufacturer_package.zip"
    gerber_dir = "gerber_files"
    bom_files = ["TFLN_BOM.csv", "TFLN_BOM_Summary.txt"]
    
    print(f"Creating {output_zip}...")
    
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add Gerber files
        if os.path.exists(gerber_dir):
            for foldername, subfolders, filenames in os.walk(gerber_dir):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    # Add file to zip, preserving relative path inside 'gerbers/' folder in zip
                    zipf.write(file_path, os.path.join('gerbers', filename))
                    print(f"  Added {filename}")
        else:
            print(f"Warning: {gerber_dir} not found!")

        # Add BOM files
        for bom_file in bom_files:
            if os.path.exists(bom_file):
                zipf.write(bom_file, os.path.basename(bom_file))
                print(f"  Added {bom_file}")
            else:
                print(f"Warning: {bom_file} not found!")
                
    print(f"\n✅ Package created: {os.path.abspath(output_zip)}")

if __name__ == "__main__":
    create_manufacturer_package()
