import numpy as np
import matplotlib.pyplot as plt
from fea_solver import FEASolver
import os

def create_channel_waveguide(solver, core_width, core_height, n_core, n_clad):
    """Creates a simple channel waveguide index profile."""
    nx, ny = solver.nx, solver.ny
    n_dist = np.full((ny, nx), n_clad)
    
    # Calculate indices for core center
    x_center = solver.width / 2
    y_center = solver.height / 2
    
    x_start = int((x_center - core_width/2) / solver.dx)
    x_end = int((x_center + core_width/2) / solver.dx)
    y_start = int((y_center - core_height/2) / solver.dy)
    y_end = int((y_center + core_height/2) / solver.dy)
    
    n_dist[y_start:y_end, x_start:x_end] = n_core
    return n_dist

def run_analysis():
    print("Starting FEA Analysis for Optical Waveguide...")
    
    # Parameters (um)
    width = 4.0
    height = 3.0
    dx = 0.05
    dy = 0.05
    wl = 1.55
    
    print(f"Domain: {width}x{height} um, Grid: {dx}x{dy} um")
    
    solver = FEASolver(width, height, dx, dy, wl)
    
    # Material properties (Silicon on Insulator approximation)
    n_core = 3.47 # Si
    n_clad = 1.444 # SiO2
    core_w = 0.5 # 500nm
    core_h = 0.22 # 220nm
    
    print(f"Waveguide: Core n={n_core}, Clading n={n_clad}")
    print(f"Core Size: {core_w}x{core_h} um")
    
    n_profile = create_channel_waveguide(solver, core_w, core_h, n_core, n_clad)
    solver.set_refractive_index(n_profile)
    
    print("Assembling matrices...")
    solver.assemble_matrices()
    
    print("Solving for modes (this may take a moment)...")
    modes = solver.solve_modes(num_modes=3)
    
    results_dir = "fea_results"
    os.makedirs(results_dir, exist_ok=True)
    
    for i, mode in enumerate(modes):
        print(f"Mode {i}: n_eff = {mode['n_eff']:.6f}")
        
        plt.figure(figsize=(10, 8))
        plt.imshow(mode['field'], extent=[0, width, 0, height], origin='lower', cmap='magma')
        plt.colorbar(label='Electric Field Amplitude |E|')
        plt.title(f"Mode {i} (TE-like/TM-like)\n$n_{{eff}} = {mode['n_eff']:.6f}$")
        plt.xlabel("Width ($\mu m$)")
        plt.ylabel("Height ($\mu m$)")
        
        # Overlay core geometry
        rect = plt.Rectangle((width/2 - core_w/2, height/2 - core_h/2), core_w, core_h, 
                             linewidth=1, edgecolor='white', facecolor='none', linestyle='--')
        plt.gca().add_patch(rect)
        
        filename = os.path.join(results_dir, f"mode_{i}.png")
        plt.savefig(filename)
        print(f"Saved mode plot to {filename}")
        plt.close()

if __name__ == "__main__":
    run_analysis()
