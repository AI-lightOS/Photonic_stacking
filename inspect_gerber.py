import sys
import os
import json

# Add current directory to path
sys.path.append(os.getcwd())

from gerber_viewer import GerberParser

def inspect_gerber(filepath):
    parser = GerberParser()
    data = parser.parse_file(filepath)
    
    print(f"Loaded {filepath}")
    print(f"Lines: {len(data.get('lines', []))}")
    print(f"Pads: {len(data.get('pads', []))}")
    
    # Check for elements near 50, 50
    center_x = 50.0
    center_y = 50.0
    roi_w = 1.0 # mm big window
    
    print(f"\nChecking region around ({center_x}, {center_y}) +/- {roi_w/2} mm")
    
    found_lines = []
    for line in data.get('lines', []):
        min_x = min(line['x1'], line['x2'])
        max_x = max(line['x1'], line['x2'])
        min_y = min(line['y1'], line['y2'])
        max_y = max(line['y1'], line['y2'])
        
        if (max_x >= center_x - roi_w/2 and min_x <= center_x + roi_w/2 and
            max_y >= center_y - roi_w/2 and min_y <= center_y + roi_w/2):
            found_lines.append(line)
            
    print(f"Found {len(found_lines)} lines in ROI")
    if found_lines:
        print("Sample line:", found_lines[0])

    found_pads = []
    for pad in data.get('pads', []):
        if (pad['x'] >= center_x - roi_w/2 and pad['x'] <= center_x + roi_w/2 and
            pad['y'] >= center_y - roi_w/2 and pad['y'] <= center_y + roi_w/2):
            found_pads.append(pad)
            
    print(f"Found {len(found_pads)} pads in ROI")
    if found_pads:
        print("Sample pad:", found_pads[0])

if __name__ == "__main__":
    inspect_gerber('gerber_files/tfln_modulator_top.gtl')
