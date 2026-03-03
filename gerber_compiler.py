import os

def generate_gerber_header():
    return [
        "%FSLAX36Y36*%",  # Coordinate format: Absolute, Leading zeros, X3.6, Y3.6
        "%MOIN*%",        # Units: Inches (using inches for standard gerber compatibility, but we can do mm)
        "%G01*%",         # Linear interpolation
        "%G70*%",         # Select Inches
        "%ADD10C,0.010*%", # Aperture 10: Circle 10mil
        "%ADD11R,0.050X0.050*%", # Aperture 11: Rectangle 50x50mil
        "G54D10*",        # Select Aperture 10
    ]

def mm_to_inches_gerber(mm):
    # Format for X3.6 (e.g., 1.234567 inches -> 1234567)
    inches = mm / 25.4
    return int(round(inches * 1000000))

def compile_gerber(components, layer_name):
    lines = generate_gerber_header()
    
    for comp in components:
        # Simple logic: Flash at component center
        # For an MVP, we just represent the component footprint with a basic shape
        x = mm_to_inches_gerber(float(comp['X_mm']))
        y = mm_to_inches_gerber(float(comp['Y_mm']))
        
        # Select aperture based on component type if needed
        # D11 for ICs, D10 for Passives
        aperture = "D11" if comp['Designator'].startswith(('U', 'J', 'OPT')) else "D10"
        lines.append(f"{aperture}*")
        lines.append(f"X{x:09d}Y{y:09d}D03*")  # Flash at X,Y
        
    lines.append("M02*")  # End of file
    return "\n".join(lines)

def generate_pick_and_place(components, side):
    # CSV format: Designator, X, Y, Rotation, Layer
    lines = ["Designator,X_mm,Y_mm,Rotation,Layer"]
    side_comps = [c for c in components if c['Layer'] == side]
    for comp in side_comps:
        lines.append(f"{comp['Designator']},{comp['X_mm']},{comp['Y_mm']},{comp['Rotation']},{comp['Layer']}")
    return "\n".join(lines)

def generate_assembly_gerber(components, side):
    # Assembly layer is similar to Silkscreen but with more detail/polarity
    lines = generate_gerber_header()
    side_comps = [c for c in components if c['Layer'] == side]
    for comp in side_comps:
        x = mm_to_inches_gerber(float(comp['X_mm']))
        y = mm_to_inches_gerber(float(comp['Y_mm']))
        
        # Draw a box for the footprint center (Assembly view)
        lines.append("D11*") # 50x50 mil rectangle for ICs, or generic
        lines.append(f"X{x:09d}Y{y:09d}D03*")
        
        # Add a polarity dot if it's an IC or Diode
        if comp['Designator'].startswith(('U', 'D')):
            lines.append("D10*") # 10mil circle for polarity
            # Offset slightly for pin 1/polarity
            px = mm_to_inches_gerber(float(comp['X_mm']) + 1.0)
            py = mm_to_inches_gerber(float(comp['Y_mm']) + 1.0)
            lines.append(f"X{px:09d}Y{py:09d}D03*")

    lines.append("M02*")
    return "\n".join(lines)

def generate_drill_file(components):
    # Excellon Drill File format
    lines = [
        "M48",           # Header start
        "INCH,LZ",       # Units (Inches, Leading Zeros)
        "T01C0.020",     # Tool 1: 20mil PTH
        "T02C0.050",     # Tool 2: 50mil NPTH
        "%",             # Header end
        "G05",           # Drill mode
        "G90",           # Absolute coordinates
    ]
    
    for comp in components:
        x = mm_to_inches_gerber(float(comp['X_mm']))
        y = mm_to_inches_gerber(float(comp['Y_mm']))
        tool = "T01" if comp['Designator'].startswith(('U', 'J', 'OPT', 'R', 'L', 'C')) else "T02"
        lines.append(tool)
        lines.append(f"X{x:06d}Y{y:06d}*") # Added * to coordinate
        
    lines.append("M30")  # End of program
    return "\n".join(lines)

def generate_ipc_netlist(components):
    # Very basic IPC-356-like placeholder
    lines = ["P  JOB LightRail_Gen3", "P  UNITS CUST 0", "P  IMAGE PRIMARY"]
    for comp in components:
        lines.append(f"317{comp['Designator']:>10}  {comp['Value']:>15}")
    lines.append("999")
    return "\n".join(lines)

def run_compiler():
    # Load components
    components = []
    with open('components.csv', 'r') as f:
        import csv
        reader = csv.DictReader(f)
        for row in reader:
            components.append(row)
            
    # Output directory
    out_dir = 'Gerbers_Compiled'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        
    # Generate 20 Signal/Plane layers
    for i in range(1, 21):
        layer_id = f"L{i:02d}"
        if i == 1: suffix = "Top"
        elif i == 20: suffix = "Bottom"
        else: suffix = f"Inner{i-1}"
        
        filename = f"LightRail_Gen3_{layer_id}_{suffix}.gbr"
        comp_subset = [c for c in components if (i == 1 and c['Layer'] == 'Top') or (i == 20 and c['Layer'] == 'Bottom')]
        content = compile_gerber(comp_subset, layer_id)
        with open(os.path.join(out_dir, filename), 'w') as f:
            f.write(content)
            
    # Generate Silk, Mask, Paste
    for s in ['SilkScreen', 'SolderMask', 'SolderPaste']:
        for side in ['Top', 'Bot']:
            filename = f"LightRail_Gen3_{s}_{side}.gbr"
            content = compile_gerber(components, s)
            with open(os.path.join(out_dir, filename), 'w') as f:
                f.write(content)

    # NEW: Generate Assembly Layers
    for side in ['Top', 'Bottom']:
        filename = f"LightRail_Gen3_{side}_Assembly.gbr"
        content = generate_assembly_gerber(components, side)
        with open(os.path.join(out_dir, filename), 'w') as f:
            f.write(content)

    # NEW: Generate Pick and Place (X-Y) files
    for side in ['Top', 'Bottom']:
        filename = f"LightRail_Gen3_Pick_and_Place_{side}.csv"
        content = generate_pick_and_place(components, side)
        with open(os.path.join(out_dir, filename), 'w') as f:
            f.write(content)

    # Generate Drill, IPC, Centroids
    with open(os.path.join(out_dir, 'LightRail_Gen3_PTH.drl'), 'w') as f:
        f.write(generate_drill_file(components))
    with open(os.path.join(out_dir, 'LightRail_Gen3_BareBoard_Test.ipc'), 'w') as f:
        f.write(generate_ipc_netlist(components))
    with open(os.path.join(out_dir, 'LightRail_Gen3_Centroids.csv'), 'w') as f:
        import shutil
        shutil.copyfile('components.csv', os.path.join(out_dir, 'LightRail_Gen3_Centroids.csv'))

    print(f"Compiled all manufacturing files to {out_dir}")

if __name__ == "__main__":
    run_compiler()
