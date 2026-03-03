import csv
import os
import random

def generate_cpl(output_file="CPL.csv"):
    """
    Generate Component Placement List (CPL) / Pick and Place file.
    Standard format for JLCPCB and Seeed Fusion.
    """
    print(f"Generating {output_file}...")
    
    # Headers suitable for common fabricators
    headers = ['Designator', 'Mid X (mm)', 'Mid Y (mm)', 'Layer', 'Rotation']
    
    components = []
    
    # 1. Main Processor U1
    components.append({
        'Designator': 'U1',
        'Mid X (mm)': 53.34,
        'Mid Y (mm)': 55.57,
        'Layer': 'Top',
        'Rotation': 0
    })
    
    # 2. Fiber Couplers OPT1_1, OPT1_2
    for i in range(1, 3):
        components.append({
            'Designator': f'OPT1_{i}',
            'Mid X (mm)': 10 + i*5,
            'Mid Y (mm)': 5,
            'Layer': 'Top',
            'Rotation': 0
        })
    
    # 3. Add 2094 Decoupling Capacitors
    random.seed(42)
    for i in range(1, 2095):
        x = 10 + (i % 50) * 1.8
        y = 10 + (i // 50) * 2.2
        components.append({
            'Designator': f'C{i}',
            'Mid X (mm)': round(x, 2),
            'Mid Y (mm)': round(y, 2),
            'Layer': 'Top',
            'Rotation': random.choice([0, 90, 180, 270])
        })

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(components)
        
    print(f"Successfully generated CPL file with {len(components)} components.")

def generate_bom(output_file="BOM.csv"):
    """
    Generate Bill of Materials (BOM).
    Standard format for JLCPCB and Seeed Fusion.
    """
    print(f"Generating {output_file}...")
    
    headers = ['Designator', 'Comment', 'Footprint', 'LCSC Part #', 'Quantity']
    
    items = []
    
    # Bulk Caps limit of string length might be an issue, but let's just output the designator
    condensed_designator = "C1-C2094"
    items.append({
        'Designator': condensed_designator,
        'Comment': '100nF 25V X7R',
        'Footprint': '0603',
        'LCSC Part #': 'C14663', # generic 0603 100nF
        'Quantity': 2094
    })
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(items)
        
    print(f"Successfully generated BOM file with {len(items)} line items.")

if __name__ == "__main__":
    generate_cpl()
    generate_bom()
