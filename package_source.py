import os
import zipfile

def package_project():
    root = "c:\\Users\\bolao\\.gemini\\antigravity\\scratch\\Photonic_stacking"
    target_zip = "LightRail_AI_Source_Project.zip"
    
    # We want the main KiCad and descriptor files
    extensions = {'.kicad_pcb', '.kicad_sch', '.kicad_pro', '.PrjPcb', '.dsn'}
    
    with zipfile.ZipFile(target_zip, 'w') as zf:
        for folder, subs, files in os.walk(root):
            # Skip large or irrelevant directories
            subs[:] = [d for d in subs if d not in {'.git', '__pycache__'} and not d.startswith('Final_Gerber_Upload')]
            
            for filename in files:
                ext = os.path.splitext(filename)[1]
                if ext in extensions:
                    # Maintain relative path for clarity
                    rel_path = os.path.relpath(os.path.join(folder, filename), root)
                    zf.write(os.path.join(folder, filename), rel_path)
    
    print(f"✅ Packaged project files into {target_zip}")

if __name__ == "__main__":
    package_project()
