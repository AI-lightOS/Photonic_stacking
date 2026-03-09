import csv
import os
import math
from datetime import datetime

def to_gerber_units(val_mm):
    val_inches = val_mm / 25.4
    return int(val_inches * 100000) # format 2.5 is 2 digit int and 5 frac meaning * 1e5
    

def generate_fabrication_gerbers(cpl_file="CPL.csv", output_dir="gerber_export"):
    os.makedirs(output_dir, exist_ok=True)
    
    components = []
    headers_ok = False
    with open(cpl_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'Mid X (mm)' in row:
                components.append({
                    'Designator': row['Designator'],
                    'X': float(row['Mid X (mm)']),
                    'Y': float(row['Mid Y (mm)']),
                    'Layer': row['Layer'],
                    'Rotation': float(row['Rotation'])
                })

    print(f"Loaded {len(components)} components from CPL to generate matching gerbers.")
    
    # Generate Top Copper (GTL)
    with open(f"{output_dir}/tfln_modulator_top.gtl", 'w', encoding='utf-8') as f:
        f.write("G04 TFLN Photonic Modulator - Top Copper Layer*\n")
        f.write("%FSLAX25Y25*%\n")
        f.write("%MOIN*%\n")
        f.write("%ADD10R,0.040000X0.020000*%\n") # Define a 40x20mil rect aperture
        f.write("G01*\n")
        for i, comp in enumerate(components):
            if comp['Layer'].lower() == 'top':
                x_gu = to_gerber_units(comp['X'])
                y_gu = to_gerber_units(comp['Y'])
                # Just draw a dot at the component center
                f.write(f"D10*\n")
                f.write(f"X{x_gu}Y{y_gu}D02*\n")
                f.write(f"X{x_gu}Y{y_gu}D01*\n")
                f.write(f"X{x_gu}Y{y_gu}D03*\n") # Flash aperture
        f.write("M02*\n")

    # Generate Top Solder Paste (GTP)
    with open(f"{output_dir}/tfln_modulator_top.gtp", 'w', encoding='utf-8') as f:
        f.write("G04 TFLN Photonic Modulator - Top Paste Layer*\n")
        f.write("%FSLAX25Y25*%\n")
        f.write("%MOIN*%\n")
        f.write("%ADD10R,0.040000X0.020000*%\n") # Define a 40x20mil rect aperture
        f.write("G01*\n")
        for i, comp in enumerate(components):
            if comp['Layer'].lower() == 'top':
                x_gu = to_gerber_units(comp['X'])
                y_gu = to_gerber_units(comp['Y'])
                f.write(f"D10*\n")
                f.write(f"X{x_gu}Y{y_gu}D03*\n") # Flash aperture
        f.write("M02*\n")
        
    # Generate Top Solder Mask (GTS)
    with open(f"{output_dir}/tfln_modulator_top_mask.gts", 'w', encoding='utf-8') as f:
        f.write("G04 TFLN Photonic Modulator - Top Mask Layer*\n")
        f.write("%FSLAX25Y25*%\n")
        f.write("%MOIN*%\n")
        f.write("%ADD10R,0.042000X0.022000*%\n") 
        f.write("G01*\n")
        for i, comp in enumerate(components):
            if comp['Layer'].lower() == 'top':
                x_gu = to_gerber_units(comp['X'])
                y_gu = to_gerber_units(comp['Y'])
                f.write(f"D10*\n")
                f.write(f"X{x_gu}Y{y_gu}D03*\n") # Flash aperture
        f.write("M02*\n")

    # Board Outline (Edge Cuts / GKO)
    with open(f"{output_dir}/tfln_modulator_outline.gm1", 'w', encoding='utf-8') as f:
        f.write("G04 Board Outline*\n")
        f.write("%FSLAX25Y25*%\n")
        f.write("%MOIN*%\n")
        f.write("%ADD10C,0.010000*%\n")
        f.write("G01*\n")
        f.write("D10*\n")
        # Find max/min dimensions based on components
        max_x = max(c['X'] for c in components) + 10
        max_y = max(c['Y'] for c in components) + 10
        min_x = min(c['X'] for c in components) - 10
        min_y = min(c['Y'] for c in components) - 10
        # Convert to gerber units
        gu_min_x = to_gerber_units(min_x)
        gu_min_y = to_gerber_units(min_y)
        gu_max_x = to_gerber_units(max_x)
        gu_max_y = to_gerber_units(max_y)
        
        f.write(f"X{gu_min_x}Y{gu_min_y}D02*\n")
        f.write(f"X{gu_max_x}Y{gu_min_y}D01*\n")
        f.write(f"X{gu_max_x}Y{gu_max_y}D01*\n")
        f.write(f"X{gu_min_x}Y{gu_max_y}D01*\n")
        f.write(f"X{gu_min_x}Y{gu_min_y}D01*\n")
        f.write("M02*\n")

    # Bottom copper
    with open(f"{output_dir}/tfln_modulator_bottom.gbl", 'w', encoding='utf-8') as f:
        f.write("G04 TFLN Photonic Modulator - Bottom Copper Layer*\n")
        f.write("%FSLAX25Y25*%\n")
        f.write("%MOIN*%\n")
        f.write("M02*\n")
        
    # Bottom Mask
    with open(f"{output_dir}/tfln_modulator_bottom_mask.gbs", 'w', encoding='utf-8') as f:
        f.write("G04 TFLN Photonic Modulator - Bottom Mask Layer*\n")
        f.write("%FSLAX25Y25*%\n")
        f.write("%MOIN*%\n")
        f.write("M02*\n")

    # Inner layers
    for x in range(2, 5):
        with open(f"{output_dir}/tfln_modulator_l{x}.g{x}", 'w', encoding='utf-8') as f:
            f.write(f"G04 TFLN Photonic Modulator - Inner Layer {x}*\n")
            f.write("%FSLAX25Y25*%\n")
            f.write("%MOIN*%\n")
            f.write("M02*\n")
            
    # Drill file
    with open(f"{output_dir}/tfln_modulator.drl", 'w', encoding='utf-8') as f:
        f.write("M48\n")
        f.write("FMAT,2\n")
        f.write("METRIC,TZ\n")
        f.write("T1C2.00\n")
        f.write("%\n")
        f.write("T1\n")
        f.write(f"X{round(min_x, 3)}Y{round(min_y, 3)}\n")
        f.write(f"X{round(max_x, 3)}Y{round(min_y, 3)}\n")
        f.write(f"X{round(max_x, 3)}Y{round(max_y, 3)}\n")
        f.write(f"X{round(min_x, 3)}Y{round(max_y, 3)}\n")
        f.write("M30\n")
        
    print(f"Gerbers generated in {output_dir}")

if __name__ == '__main__':
    generate_fabrication_gerbers()
