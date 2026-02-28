import numpy as np
import matplotlib
matplotlib.use('Agg') # Use non-interactive backend
import matplotlib.pyplot as plt
from fea_solver import FEASolver
import os
import uuid

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
    
    # Clip indices to be within bounds
    x_start = max(0, x_start)
    x_end = min(nx, x_end)
    y_start = max(0, y_start)
    y_end = min(ny, y_end)

    n_dist[y_start:y_end, x_start:x_end] = n_core
    return n_dist

def run_fea_simulation(width, height, core_w, core_h, wl, n_core=3.47, n_clad=1.444):
    """
    Runs the FEA simulation and returns results with image paths.
    """
    # Grid resolution (fixed for performance/stability for now, or could be dynamic)
    dx = 0.05
    dy = 0.05
    
    solver = FEASolver(width, height, dx, dy, wl)
    n_profile = create_channel_waveguide(solver, core_w, core_h, n_core, n_clad)
    solver.set_refractive_index(n_profile)
    
    solver.assemble_matrices()
    modes = solver.solve_modes(num_modes=3)
    
    results = []
    base_path = "static/fea_results"
    
    # Generate unique run ID to avoid caching issues
    run_id = str(uuid.uuid4())[:8]

    # Ensure output directory exists
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    for i, mode in enumerate(modes):
        filename = f"mode_{run_id}_{i}.png"
        filepath = os.path.join(base_path, filename)
        
        plt.figure(figsize=(6, 5))
        plt.imshow(mode['field'], extent=[0, width, 0, height], origin='lower', cmap='magma')
        plt.colorbar(label='|E| Field')
        plt.title(f"Mode {i}: $n_{{eff}} = {mode['n_eff']:.4f}$")
        plt.xlabel("Width ($\mu m$)")
        plt.ylabel("Height ($\mu m$)")
        
        # Overlay core
        rect = plt.Rectangle((width/2 - core_w/2, height/2 - core_h/2), core_w, core_h, 
                             linewidth=1, edgecolor='white', facecolor='none', linestyle='--')
        plt.gca().add_patch(rect)
        
        plt.tight_layout()
        plt.savefig(filepath)
        plt.close()
        
        results.append({
            'mode_index': i,
            'n_eff': float(mode['n_eff']),
            'beta': float(mode['beta']),
            'image_url': f"/static/fea_results/{filename}"
        })
        
    return results
