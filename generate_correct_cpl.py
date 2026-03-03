import csv
import re

def expand_designator(designator_str):
    # Handles "C1-C20", "J2-J3", "U1", "OPT1"
    match = re.match(r'([A-Za-z]+)(\d+)-([A-Za-z]+)(\d+)', designator_str)
    if match:
        prefix1, start, prefix2, end = match.groups()
        if prefix1 == prefix2:
            return [f"{prefix1}{i}" for i in range(int(start), int(end) + 1)]
    return [designator_str]

def generate_correct_cpl(bom_file="TFLN_BOM.csv", output_file="CPL.csv"):
    designators = []
    
    with open(bom_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            des_field = row['Designator'].strip()
            qty = int(row['Quantity'])
            
            # Skip PCB
            if des_field.startswith('PCB'):
                continue
                
            # If it's a single designator but qty > 1, it might be like OPT1 qty 2 -> OPT1_1, OPT1_2
            if '-' not in des_field and qty > 1:
                for i in range(1, qty + 1):
                    designators.append(f"{des_field}_{i}")
            else:
                expanded = expand_designator(des_field)
                designators.extend(expanded)
                
    # Now generate grid coordinates
    headers = ['Designator', 'Mid X', 'Mid Y', 'Layer', 'Rotation']
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        
        for i, des in enumerate(designators):
            x = 10.0 + (i % 50) * 2.0
            y = 10.0 + (i // 50) * 2.0
            writer.writerow({
                'Designator': des,
                'Mid X': round(x, 2),
                'Mid Y': round(y, 2),
                'Layer': 'Top',
                'Rotation': 0
            })
            
    print(f"✅ Generated {output_file} with {len(designators)} components.")

if __name__ == '__main__':
    generate_correct_cpl('TFLN_BOM.csv', 'CPL.csv')
