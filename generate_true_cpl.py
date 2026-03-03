import re
import csv
import sys

def parse_kicad_pcb(filename):
    components = []
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        
    blocks = content.split("(footprint ")[1:]
    for block in blocks:
        # Extract designator
        ref_match = re.search(r'\(property\s+"Reference"\s+"(.*?)"', block)
        if not ref_match:
            ref_match = re.search(r'\(fp_text\s+reference\s+"?(.*?)"?\s', block)
            
        if not ref_match:
            continue
            
        designator = ref_match.group(1)
        
        # Avoid things that aren't real components
        if designator.startswith("REF**") or designator == "":
            continue
            
        # Extract at (at X Y [rot])
        # Sometimes there's unlocked or other things directly after 'at '.
        # (at 110 110) or (at 110 110 90) or (at 110.5 110.5 180 unlocked)
        at_match = re.search(r'\(at\s+([-+]?[0-9]*\.?[0-9]+)\s+([-+]?[0-9]*\.?[0-9]+)(?:\s+([-+]?[0-9]*\.?[0-9]+))?', block)
        if not at_match:
            continue
        
        mid_x = at_match.group(1)
        mid_y = at_match.group(2)
        rotation = at_match.group(3) if at_match.group(3) else "0"
        
        # Extract layer (layer "F.Cu")
        layer_match = re.search(r'\(layer\s+"?([^"\s\)]+)"?', block)
        layer = "Top"
        if layer_match:
            if layer_match.group(1) == "B.Cu":
                layer = "Bottom"
            elif layer_match.group(1) == "F.Cu":
                layer = "Top"
        
        components.append({
            'Designator': designator,
            'Mid X': round(float(mid_x), 3),
            'Mid Y': round(float(mid_y) * -1.0, 3) if float(mid_y) != 0 else 0, # Invert Y for standard CPL, often needed or we just keep native. Typical JLCPCB likes native X, Y. We'll use native X, Y just to be safe.
        })
        # Let's use native KiCad coordinates since it's most commonly expected unless offset.
        components[-1]['Mid Y'] = round(float(mid_y), 3)
        components[-1]['Layer'] = layer
        components[-1]['Rotation'] = round(float(rotation), 3)
        
    return components

def generate_cpl(kicad_file, output_file):
    components = parse_kicad_pcb(kicad_file)
    headers = ['Designator', 'Mid X', 'Mid Y', 'Layer', 'Rotation']
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for c in components:
            writer.writerow(c)
            
    print(f"Generated CPL with {len(components)} components.")

if __name__ == '__main__':
    generate_cpl('tfln_modulator.kicad_pcb', 'CPL.csv')
