import os
import re
import zipfile

class GerberToCNC:
    def __init__(self, input_dir="gerber_files", output_dir="cnc_files"):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def parse_coordinate(self, val_str):
        # Format is X3.6 (e.g. 1000000 = 1.000000 inch)
        # We assume the format is consistent with generate_gerber.py
        try:
            val = int(val_str)
            return val / 1000000.0
        except ValueError:
            return 0.0

    def convert_file(self, filename):
        input_path = os.path.join(self.input_dir, filename)
        output_filename = filename + ".nc"
        output_path = os.path.join(self.output_dir, output_filename)
        
        with open(input_path, 'r') as f_in, open(output_path, 'w') as f_out:
            # G-code Header
            f_out.write("%\n")
            f_out.write(f"(Converted from {filename})\n")
            f_out.write("G20 (Units: Inches)\n") # generate_gerber specifies MOIN (Inches)
            f_out.write("G90 (Absolute coordinates)\n")
            f_out.write("G17 (XY Plane)\n")
            f_out.write("G00 Z0.1 (Safe height)\n")
            f_out.write("M03 S1000 (Spindle on)\n")
            
            # Simple regex to find X...Y...D... lines
            # Example: X1000000Y1000000D02*
            coord_pattern = re.compile(r'X(\d+)Y(\d+)D(\d+)')
            
            has_moves = False
            
            for line in f_in:
                line = line.strip()
                if not line:
                    continue
                
                # Check for linear moves
                match = coord_pattern.search(line)
                if match:
                    x_str, y_str, d_code = match.groups()
                    x_val = self.parse_coordinate(x_str)
                    y_val = self.parse_coordinate(y_str)
                    
                    if d_code == '02': # Move (Light Off / Spindle Up equivalents usually G00, but in routing often just Z up/down)
                        # For simple routing: lift Z, move, drop Z?
                        # Or just G00/G01. Let's stick to simple G00/G01 for XY logic first.
                        # Usually D02 in Gerber is "Exposure Off" -> Move to location.
                        f_out.write(f"G00 X{x_val:.6f} Y{y_val:.6f}\n")
                        has_moves = True
                    elif d_code == '01': # Draw (Light On / Spindle Down)
                        # Depending on machine, might need Z down first.
                        # Assuming 2D path for now or that previous G00 handled positioning.
                        # Actually a proper mill needs Z logic.
                        # Simplified: G01 implies cutting.
                        f_out.write(f"G01 X{x_val:.6f} Y{y_val:.6f} F10.0\n") 
                        has_moves = True
                        
            # Footer
            f_out.write("M05 (Spindle off)\n")
            f_out.write("M30 (End program)\n")
            f_out.write("%\n")
            
        print(f"Converted {filename} -> {output_filename}")
        return output_path

    def convert_all(self):
        print(f"Converting Gerber files in {self.input_dir} to CNC files in {self.output_dir}...")
        generated_files = []
        for filename in os.listdir(self.input_dir):
            # Check for standard Gerber extensions and numbered layer extensions
            ext = os.path.splitext(filename)[1].lower()
            if ext in ['.gtl', '.gbl', '.gts', '.gbs', '.gto', '.gbo', '.gm1', '.drl'] or \
               re.match(r'\.g\d+', ext):
                 # Handle generic extension layers like .g10, .g11 which endswith might miss if not careful, 
                 # actually os.listdir returns filenames, so startswith/endswith is fine.
                 # The file extensions in previous list were .gtl, .gbl, .gbs, .gts, .gto, .gm1, .g2, .g3 ... .g11 
                 # Let's just try to convert anything that looks like a gerber.
                 # Better: ignore potential non-gerber files like README.txt
                 if filename.lower() == 'readme.txt':
                     continue
                 
                 output_file = self.convert_file(filename)
                 generated_files.append(output_file)
        
        return generated_files

    def zip_files(self, file_list, zip_name="cnc_files.zip"):
        zip_path = os.path.join(self.output_dir, zip_name)
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in file_list:
                zipf.write(file, os.path.basename(file))
        print(f"Zipped {len(file_list)} files into {zip_path}")
        return zip_path

if __name__ == "__main__":
    converter = GerberToCNC()
    cnc_files = converter.convert_all()
    converter.zip_files(cnc_files)
