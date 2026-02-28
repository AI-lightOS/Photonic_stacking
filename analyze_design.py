import os
import sys
import glob
from gerber_viewer import GerberParser, parse_drill_file

def analyze_gerber_files(gerber_dir='gerber_files'):
    print(f"Analyzing Gerber Files in '{gerber_dir}'...")
    
    # Check if directory exists
    if not os.path.exists(gerber_dir):
        print(f"Error: Directory '{gerber_dir}' not found.")
        return

    # List all relevant files
    extensions = ['.gtl', '.gbl', '.g2', '.g3', '.g4', '.g5', '.g6', '.g7', '.g8', '.g9', '.g10', '.g11', 
                  '.gts', '.gbs', '.gto', '.gbo', '.gm1', '.drl']
    
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(gerber_dir, f'*{ext}')))
        
    if not files:
        print("No Gerber files found.")
        return

    parser = GerberParser()
    
    min_trace_width = float('inf')
    min_drill_diameter = float('inf')
    copper_layers = set()
    
    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = float('-inf'), float('-inf')
    
    for filepath in files:
        filename = os.path.basename(filepath)
        ext = os.path.splitext(filename)[1]
        
        # Determine layer type
        is_copper = ext in ['.gtl', '.gbl'] or (ext.startswith('.g') and ext[2:].isdigit())
        if is_copper:
            copper_layers.add(filename)
            
        print(f"Parsing {filename}...")
        
        try:
            if ext == '.drl':
                drill_data = parse_drill_file(filepath)
                # Check tools
                for tool_code, size in drill_data.get('tools', {}).items():
                    if size < min_drill_diameter:
                        min_drill_diameter = size
                # Check holes for bounds
                for hole in drill_data.get('holes', []):
                    min_x = min(min_x, hole['x'])
                    max_x = max(max_x, hole['x'])
                    min_y = min(min_y, hole['y'])
                    max_y = max(max_y, hole['y'])
            else:
                data = parser.parse_file(filepath)
                
                # Check lines for trace width (only on copper layers)
                if is_copper:
                    for line in data.get('lines', []):
                        width = line.get('width', 0)
                        if width > 0 and width < min_trace_width:
                            min_trace_width = width
                        
                        # Update bounds
                        min_x = min(min_x, line['x1'], line['x2'])
                        max_x = max(max_x, line['x1'], line['x2'])
                        min_y = min(min_y, line['y1'], line['y2'])
                        max_y = max(max_y, line['y1'], line['y2'])
                
                # Check pads
                for pad in data.get('pads', []):
                    # Update bounds
                    min_x = min(min_x, pad['x'])
                    max_x = max(max_x, pad['x'])
                    min_y = min(min_y, pad['y'])
                    max_y = max(max_y, pad['y'])
                    
        except Exception as e:
            print(f"Warning: Failed to parse {filename}: {e}")

    # Calculate results
    width_mm = max_x - min_x if max_x > min_x else 0
    height_mm = max_y - min_y if max_y > min_y else 0
    
    print("\n" + "="*40)
    print("       DESIGN ANALYSIS REPORT       ")
    print("="*40)
    print(f"Board Dimensions:   {width_mm:.2f} mm x {height_mm:.2f} mm")
    print(f"Copper Layer Count: {len(copper_layers)}")
    if min_trace_width != float('inf'):
        print(f"Min Trace Width:    {min_trace_width:.4f} mm ({min_trace_width/0.0254:.2f} mil)")
    else:
        print("Min Trace Width:    N/A")
        
    if min_drill_diameter != float('inf'):
        print(f"Min Drill Diameter: {min_drill_diameter:.4f} mm ({min_drill_diameter/0.0254:.2f} mil)")
    else:
        print("Min Drill Diameter: N/A")
    print("="*40)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        analyze_gerber_files(sys.argv[1])
    else:
        analyze_gerber_files()
