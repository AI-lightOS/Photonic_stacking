import sys
import os
import traceback

# Add current directory to path
sys.path.append(os.getcwd())

from gerber_fea import run_gerber_fea_simulation

try:
    print("Running Gerber FEA simulation...")
    # Using parameters from the UI default
    results = run_gerber_fea_simulation(
        gerber_path='gerber_files/tfln_modulator_top.gtl',
        center_x_mm=50.0,
        center_y_mm=50.0,
        width_um=20.0,
        height_um=10.0,
        core_n=3.47
    )
    print("Success!")
    print(results)
except Exception:
    traceback.print_exc()
