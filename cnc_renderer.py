import os
import re
import matplotlib.pyplot as plt
import glob

class CNCRenderer:
    def __init__(self, input_dir="cnc_files", output_dir="rendered_cnc"):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def parse_gcode(self, filepath):
        """Parses a G-code file and returns a list of paths."""
        paths = []
        current_path = []
        current_x = 0.0
        current_y = 0.0
        
        # Simple finite state machine
        # We start at (0,0). 
        # G00 (Rapid) -> Ends current cut path, moves to new pos.
        # G01 (Cut) -> Adds line segment from current pos to new pos.
        
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip().upper()
                if not line:
                    continue
                
                # Extract coordinates if present
                x_match = re.search(r'X([\d\.-]+)', line)
                y_match = re.search(r'Y([\d\.-]+)', line)
                
                new_x = float(x_match.group(1)) if x_match else current_x
                new_y = float(y_match.group(1)) if y_match else current_y
                
                if 'G00' in line:
                    # Rapid move - stop current path if we were cutting
                    if current_path:
                        paths.append(current_path)
                        current_path = []
                    # Update position without drawing
                    current_x = new_x
                    current_y = new_y
                    
                elif 'G01' in line:
                    # Linear cut - start new path if needed or continue
                    if not current_path:
                         current_path.append((current_x, current_y))
                    
                    current_path.append((new_x, new_y))
                    current_x = new_x
                    current_y = new_y
        
        # Add the last path if exists
        if current_path:
            paths.append(current_path)
            
        return paths

    def render_file(self, filename):
        input_path = os.path.join(self.input_dir, filename)
        paths = self.parse_gcode(input_path)
        
        if not paths:
            print(f"No paths found in {filename}")
            return

        plt.figure(figsize=(10, 10))
        for path in paths:
            xs, ys = zip(*path)
            plt.plot(xs, ys, 'b-', linewidth=1)
            
        plt.title(f"CNC Render: {filename}")
        plt.xlabel("X (inches)")
        plt.ylabel("Y (inches)")
        plt.axis('equal')
        plt.grid(True)
        
        output_filename = filename + ".png"
        output_path = os.path.join(self.output_dir, output_filename)
        plt.savefig(output_path)
        plt.close()
        print(f"Rendered {filename} -> {output_path}")

    def render_all(self):
        print(f"Rendering CNC files from {self.input_dir} to {self.output_dir}...")
        files = glob.glob(os.path.join(self.input_dir, "*.nc"))
        for file in files:
            filename = os.path.basename(file)
            self.render_file(filename)

if __name__ == "__main__":
    renderer = CNCRenderer()
    renderer.render_all()
