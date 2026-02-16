"""
Pick and Place (Centroid) File Generator for Seeed Fusion PCBA
Generates a CSV with Designator, Mid X, Mid Y, Layer, and Rotation.
Based on the 2095-component LightRail Intelligence Stack design.
"""

import csv
import random

def generate_pick_and_place(output_file="LightRail_Centroid.csv"):
    print(f"Generating {output_file}...")
    
    # Header: Designator, Mid X, Mid Y, Layer, Rotation
    headers = ['Designator', 'Mid X', 'Mid Y', 'Layer', 'Rotation', 'Comment']
    
    components = []
    
    # 1. Main Processor U1
    components.append({
        'Designator': 'U1',
        'Mid X': 53.34,
        'Mid Y': 55.57,
        'Layer': 'Top',
        'Rotation': 0,
        'Comment': 'TFLN_MZM_400G (DNP - Manual Align)'
    })
    
    # 2. Fiber Couplers OPT1 (DNP)
    for i in range(1, 3):
        components.append({
            'Designator': f'OPT1_{i}',
            'Mid X': 10 + i*5,
            'Mid Y': 5,
            'Layer': 'Top',
            'Rotation': 0,
            'Comment': 'FC-TFLN-SMF28 (DNP - Manual Align)'
        })
    
    # 2. Add 2094 Decoupling Capacitors (Matching generate_dsn.py distribution)
    random.seed(42)
    for i in range(1, 2095):
        x = 10 + (i % 50) * 1.8
        y = 10 + (i // 50) * 2.2
        components.append({
            'Designator': f'C{i}',
            'Mid X': round(x, 2),
            'Mid Y': round(y, 2),
            'Layer': 'Top',
            'Rotation': random.choice([0, 90, 180, 270]),
            'Comment': '0603_0.1uF'
        })

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(components)
        
    print(f"Successfully generated centroid file with {len(components)} components.")

if __name__ == "__main__":
    generate_pick_and_place()
