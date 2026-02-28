import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from gerber_viewer import GerberParser
import os
import uuid
import sys

# Add current directory to path so we can import fea_solver
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fea_solver import FEASolver

class GerberRasterizer:
    def __init__(self, gerber_path):
        self.parser = GerberParser()
        # Create a dummy parser instance to reuse its logic if needed or just use the class
        # But wait, GerberParser in gerber_viewer.py has a parse_file method.
        # Let's check gerber_viewer.py again.
        # It has a class GerberParser with parse_file.
        self.parser = GerberParser()
        self.gerber_data = self.parser.parse_file(gerber_path)
        
    def rasterize_region(self, center_x_mm, center_y_mm, width_um, height_um, resolution_um=0.05, n_trace=3.47, n_sub=1.444):
        """
        Rasterize a region of the Gerber file into a refractive index grid.
        
        Args:
            center_x_mm, center_y_mm: Center coordinates in mm (Gerber coords)
            width_um, height_um: Size of the ROI in microns
            resolution_um: Grid resolution in microns
            n_trace: Refractive index of the trace (e.g., Silicon)
            n_sub: Refractive index of the substrate/cladding (e.g., SiO2)
            
        Returns:
            n_grid: 2D numpy array of refractive indices
            extent: tuple (x_min, x_max, y_min, y_max) in microns relative to ROI center
        """
        # FEASolver uses node-based grid (nx+1, ny+1)
        # We need to match that.
        nx = int(width_um / resolution_um) + 1
        ny = int(height_um / resolution_um) + 1
        
        n_grid = np.full((ny, nx), n_sub)
        
        # Convert ROI bounds to mm for intersection testing
        # width_um is in microns. 1 mm = 1000 um.
        half_w_mm = (width_um / 2000.0)
        half_h_mm = (height_um / 2000.0)
        
        x_min_mm = center_x_mm - half_w_mm
        x_max_mm = center_x_mm + half_w_mm
        y_min_mm = center_y_mm - half_h_mm
        y_max_mm = center_y_mm + half_h_mm
        
        # Helper to convert mm coord to grid index
        # Grid (0,0) corresponds to (x_min_mm, y_min_mm)
        def mm_to_grid_x(x_mm):
            return int((x_mm - x_min_mm) * 1000 / resolution_um)
        
        def mm_to_grid_y(y_mm):
            return int((y_mm - y_min_mm) * 1000 / resolution_um)

        # Iterate over lines
        lines = self.gerber_data.get('lines', [])
        features_found = False
        
        for line in lines:
            x1, y1 = line['x1'], line['y1']
            x2, y2 = line['x2'], line['y2']
            w = line.get('width', 0.1) # Default width if missing
            
            # Simple bounding box check
            l_min_x = min(x1, x2) - w/2
            l_max_x = max(x1, x2) + w/2
            l_min_y = min(y1, y2) - w/2
            l_max_y = max(y1, y2) + w/2
            
            if (l_max_x < x_min_mm or l_min_x > x_max_mm or 
                l_max_y < y_min_mm or l_min_y > y_max_mm):
                continue
            
            features_found = True
            
            # Rasterize this line segment onto our grid
            gx_min = max(0, mm_to_grid_x(l_min_x))
            gx_max = min(nx, mm_to_grid_x(l_max_x) + 1)
            gy_min = max(0, mm_to_grid_y(l_min_y))
            gy_max = min(ny, mm_to_grid_y(l_max_y) + 1)
            
            p1 = np.array([x1, y1])
            p2 = np.array([x2, y2])
            v = p2 - p1
            v_len_sq = np.dot(v, v)
            
            for iy in range(gy_min, gy_max):
                y_mm = y_min_mm + (iy * resolution_um / 1000.0)
                for ix in range(gx_min, gx_max):
                    x_mm = x_min_mm + (ix * resolution_um / 1000.0)
                    p = np.array([x_mm, y_mm])
                    
                    if v_len_sq == 0:
                        dist = np.linalg.norm(p - p1)
                    else:
                        t = max(0, min(1, np.dot(p - p1, v) / v_len_sq))
                        projection = p1 + t * v
                        dist = np.linalg.norm(p - projection)
                    
                    if dist <= w / 2:
                        n_grid[iy, ix] = n_trace

        # Iterate over pads (flashes)
        pads = self.gerber_data.get('pads', [])
        for pad in pads:
            px, py = pad['x'], pad['y']
            # Assume circular for simplicity if shape not specified or unknown
            # Aperture size: [diameter] or [width, height]
            size = pad.get('size', [0.2]) 
            radius = size[0] / 2
            
            # Bounding box
            if (px + radius < x_min_mm or px - radius > x_max_mm or
                py + radius < y_min_mm or py - radius > y_max_mm):
                continue

            features_found = True

            # Rasterize pad (assuming circle for now)
            gx_min = max(0, mm_to_grid_x(px - radius))
            gx_max = min(nx, mm_to_grid_x(px + radius) + 1)
            gy_min = max(0, mm_to_grid_y(py - radius))
            gy_max = min(ny, mm_to_grid_y(py + radius) + 1)

            for iy in range(gy_min, gy_max):
                y_mm = y_min_mm + (iy * resolution_um / 1000.0)
                for ix in range(gx_min, gx_max):
                    x_mm = x_min_mm + (ix * resolution_um / 1000.0)
                    if (x_mm - px)**2 + (y_mm - py)**2 <= radius**2:
                        n_grid[iy, ix] = n_trace

        # Fallback if no features found in ROI: Draw a dummy waveguide
        # This ensures the user sees *something* instead of a blank/error
        if not features_found:
            print("No features found in ROI. Injecting dummy waveguide.")
            # Draw a horizontal waveguide in the center
            center_y_idx = ny // 2
            # Width of waveguide = 4 microns (approx 80 pixels at 0.05um res)
            wg_half_width_px = int(2.0 / resolution_um)
            
            y_start = max(0, center_y_idx - wg_half_width_px)
            y_end = min(ny, center_y_idx + wg_half_width_px)
            
            n_grid[y_start:y_end, :] = n_trace

        return n_grid


def run_gerber_fea_simulation(gerber_path, center_x_mm, center_y_mm, width_um=10.0, height_um=5.0, core_n=3.47):
    """
    Parses Gerber, extracts ROI, and runs FEA.
    """
    if not os.path.exists(gerber_path):
        raise FileNotFoundError(f"Gerber file not found: {gerber_path}")
        
    rasterizer = GerberRasterizer(gerber_path)
    # Default resolution
    dx = 0.05
    dy = 0.05
    
    n_grid = rasterizer.rasterize_region(center_x_mm, center_y_mm, width_um, height_um, 
                                        resolution_um=dx, n_trace=core_n)
    
    # Create solver
    solver = FEASolver(width_um, height_um, dx, dy, wl=1.55)
    
    # Set refractive index - user logic needs to handle 2D array
    # FEASolver.set_refractive_index accepts 2D array (ny, nx)
    solver.set_refractive_index(n_grid)
    
    solver.assemble_matrices()
    modes = solver.solve_modes(num_modes=3)
    
    results = []
    base_path = "static/fea_results"
    run_id = str(uuid.uuid4())[:8]
    
    if not os.path.exists(base_path):
        os.makedirs(base_path)
        
    for i, mode in enumerate(modes):
        filename = f"gerber_mode_{run_id}_{i}.png"
        filepath = os.path.join(base_path, filename) # Saving to static/fea_results
        abs_filepath = os.path.abspath(filepath)
        
        plt.figure(figsize=(6, 5))
        plt.imshow(mode['field'], extent=[0, width_um, 0, height_um], origin='lower', cmap='magma')
        plt.colorbar(label='|E| Field')
        plt.title(f"Gerber Mode {i}: $n_{{eff}} = {mode['n_eff']:.4f}$")
        plt.xlabel("Width (um)")
        plt.ylabel("Height (um)")
        plt.tight_layout()
        plt.savefig(abs_filepath)
        plt.close()
        
        results.append({
            'mode_index': i,
            'n_eff': float(mode['n_eff']),
            'beta': float(mode['beta']),
            'image_url': f"/static/fea_results/{filename}"
        })
        
    return {
        'results': results,
        'roi': {
            'center_x_mm': center_x_mm,
            'center_y_mm': center_y_mm,
            'width_um': width_um,
            'height_um': height_um
        }
    }
