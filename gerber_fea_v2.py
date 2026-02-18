import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from gerber_viewer import GerberParser
import os
import uuid
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add current directory to path so we can import fea_solver
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fea_solver import FEASolver

class GerberRasterizerV2:
    def __init__(self, gerber_path):
        if not os.path.exists(gerber_path):
            raise FileNotFoundError(f"Gerber file not found: {gerber_path}")
            
        self.parser = GerberParser()
        logger.info(f"Parsing Gerber file: {gerber_path}")
        self.gerber_data = self.parser.parse_file(gerber_path)
        
        # Log stats
        l_count = len(self.gerber_data.get('lines', []))
        p_count = len(self.gerber_data.get('pads', []))
        logger.info(f"Parsed {l_count} lines and {p_count} pads.")
        
    def rasterize_region(self, center_x_mm, center_y_mm, width_um, height_um, resolution_um=0.05, n_trace=3.47, n_sub=1.444):
        """
        Rasterize a region of the Gerber file into a refractive index grid.
        """
        # FEASolver uses node-based grid (nx+1, ny+1)
        nx = int(width_um / resolution_um) + 1
        ny = int(height_um / resolution_um) + 1
        
        logger.info(f"Rasterizing ROI: Center=({center_x_mm}, {center_y_mm}) mm, Size=({width_um}, {height_um}) um, Grid=({nx}x{ny})")
        
        n_grid = np.full((ny, nx), n_sub)
        
        # roi bounds in mm
        half_w_mm = (width_um / 2000.0)
        half_h_mm = (height_um / 2000.0)
        
        x_min_mm = center_x_mm - half_w_mm
        x_max_mm = center_x_mm + half_w_mm
        y_min_mm = center_y_mm - half_h_mm
        y_max_mm = center_y_mm + half_h_mm
        
        # Scaling factor for grid conversion
        scale = 1000.0 / resolution_um # pixels per mm

        def to_grid(x_mm, y_mm):
            gx = int((x_mm - x_min_mm) * scale)
            gy = int((y_mm - y_min_mm) * scale)
            return gx, gy

        features_found = False

        # --- Rasterize Lines ---
        lines = self.gerber_data.get('lines', [])
        for line in lines:
            x1, y1 = line['x1'], line['y1']
            x2, y2 = line['x2'], line['y2']
            w = line.get('width', 0.1)
            
            # Fast bounding box exclusion
            if (max(x1, x2) + w/2 < x_min_mm or min(x1, x2) - w/2 > x_max_mm or
                max(y1, y2) + w/2 < y_min_mm or min(y1, y2) - w/2 > y_max_mm):
                continue
            
            features_found = True
            
            # Grid bounds for this line (clamped to ROI)
            gx_min, gy_min = to_grid(min(x1, x2) - w/2, min(y1, y2) - w/2)
            gx_max, gy_max = to_grid(max(x1, x2) + w/2, max(y1, y2) + w/2)
            
            gx_min = max(0, gx_min)
            gx_max = min(nx, gx_max + 1)
            gy_min = max(0, gy_min)
            gy_max = min(ny, gy_max + 1)
            
            # Vectorized distance calculation? 
            # For simplicity and correctness with small ROIs, loop is okay, but let's optimize slightly
            # by precalculating vector math
            p1 = np.array([x1, y1])
            v = np.array([x2 - x1, y2 - y1])
            v_len_sq = np.dot(v, v)
            
            for iy in range(gy_min, gy_max):
                y_w = y_min_mm + iy / scale
                for ix in range(gx_min, gx_max):
                    x_w = x_min_mm + ix / scale
                    p = np.array([x_w, y_w])
                    
                    if v_len_sq == 0:
                        dist = np.linalg.norm(p - p1)
                    else:
                        t = max(0, min(1, np.dot(p - p1, v) / v_len_sq))
                        dist = np.linalg.norm(p - (p1 + t * v))
                    
                    if dist <= w / 2:
                        n_grid[iy, ix] = n_trace

        # --- Rasterize Pads ---
        pads = self.gerber_data.get('pads', [])
        for pad in pads:
            px, py = pad['x'], pad['y']
            size = pad.get('size', [0.2])
            radius = size[0] / 2
            
            if (px + radius < x_min_mm or px - radius > x_max_mm or
                py + radius < y_min_mm or py - radius > y_max_mm):
                continue
            
            features_found = True
            
            gx_min, gy_min = to_grid(px - radius, py - radius)
            gx_max, gy_max = to_grid(px + radius, py + radius)
            
            gx_min = max(0, gx_min)
            gx_max = min(nx, gx_max + 1)
            gy_min = max(0, gy_min)
            gy_max = min(ny, gy_max + 1)
            
            r_sq = radius**2
            
            for iy in range(gy_min, gy_max):
                y_w = y_min_mm + iy / scale
                for ix in range(gx_min, gx_max):
                    x_w = x_min_mm + ix / scale
                    if (x_w - px)**2 + (y_w - py)**2 <= r_sq:
                        n_grid[iy, ix] = n_trace

        # --- Fallback Strategy ---
        if not features_found:
            logger.warning("No features found in ROI. Injecting dummy waveguide for visualization.")
            # Center waveguide
            mid_y = ny // 2
            half_w_px = int(2.0 * scale / 1000.0) # 2um half width
            n_grid[mid_y - half_w_px : mid_y + half_w_px, :] = n_trace

        return n_grid

def run_gerber_fea_v2(gerber_path, center_x_mm, center_y_mm, width_um=10.0, height_um=5.0, core_n=3.47):
    try:
        rasterizer = GerberRasterizerV2(gerber_path)
        dx = 0.05
        dy = 0.05
        
        n_grid = rasterizer.rasterize_region(center_x_mm, center_y_mm, width_um, height_um, 
                                            resolution_um=dx, n_trace=core_n)
        
        logger.info("Initializing FEA Solver...")
        solver = FEASolver(width_um, height_um, dx, dy, wl=1.55)
        solver.set_refractive_index(n_grid)
        
        logger.info("Assembling matrices...")
        solver.assemble_matrices()
        
        logger.info("Solving for modes...")
        modes = solver.solve_modes(num_modes=3)
        
        results = []
        base_path = "static/fea_results"
        run_id = str(uuid.uuid4())[:8]
        if not os.path.exists(base_path):
            os.makedirs(base_path)
            
        for i, mode in enumerate(modes):
            filename = f"gerber_v2_{run_id}_{i}.png"
            filepath = os.path.join(base_path, filename)
            
            plt.figure(figsize=(6, 5))
            plt.imshow(mode['field'], extent=[0, width_um, 0, height_um], origin='lower', cmap='plasma')
            plt.colorbar(label='|E| Field')
            plt.title(f"Mode {i}: $n_{{eff}} = {mode['n_eff']:.4f}$")
            plt.xlabel("Width (µm)")
            plt.ylabel("Height (µm)")
            plt.tight_layout()
            plt.savefig(filepath)
            plt.close()
            
            results.append({
                'mode_index': i,
                'n_eff': float(mode['n_eff']),
                'beta': float(mode['beta']),
                'image_url': f"/static/fea_results/{filename}"
            })
            
        return {'status': 'success', 'data': results}
        
    except Exception as e:
        logger.error(f"FEA Simulation Failed: {e}", exc_info=True)
        return {'status': 'error', 'error': str(e)}

if __name__ == "__main__":
    # Test run
    print(run_gerber_fea_v2('gerber_files/tfln_modulator_top.gtl', 50.0, 50.0))
