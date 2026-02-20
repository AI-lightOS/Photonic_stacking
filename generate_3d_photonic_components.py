import os
import math

class STLWriter:
    """Simple ASCII STL writer"""
    def __init__(self, filename):
        self.filename = filename
        self.facets = []

    def add_triangle(self, v1, v2, v3):
        # Calculate normal
        ux, uy, uz = v2[0]-v1[0], v2[1]-v1[1], v2[2]-v1[2]
        vx, vy, vz = v3[0]-v1[0], v3[1]-v1[1], v3[2]-v1[2]
        nx = uy*vz - uz*vy
        ny = uz*vx - ux*vz
        nz = ux*vy - uy*vx
        length = math.sqrt(nx*nx + ny*ny + nz*nz)
        if length > 0:
            normal = (nx/length, ny/length, nz/length)
        else:
            normal = (0, 0, 0)
        
        self.facets.append((normal, v1, v2, v3))

    def add_quad(self, v1, v2, v3, v4):
        """Add two triangles to make a quad (v1, v2, v3, v4 in counter-clockwise order)"""
        self.add_triangle(v1, v2, v3)
        self.add_triangle(v1, v3, v4)

    def add_block(self, x, y, z, width, length, height):
        """Add a rectangular block"""
        # Vertices
        v0 = (x, y, z)
        v1 = (x + width, y, z)
        v2 = (x + width, y + length, z)
        v3 = (x, y + length, z)
        v4 = (x, y, z + height)
        v5 = (x + width, y, z + height)
        v6 = (x + width, y + length, z + height)
        v7 = (x, y + length, z + height)

        # Bottom
        self.add_quad(v0, v3, v2, v1)
        # Top
        self.add_quad(v4, v5, v6, v7)
        # Front
        self.add_quad(v0, v1, v5, v4)
        # Back
        self.add_quad(v3, v7, v6, v2)
        # Left
        self.add_quad(v0, v4, v7, v3)
        # Right
        self.add_quad(v1, v2, v6, v5)

    def write(self):
        with open(self.filename, 'w') as f:
            f.write(f"solid {os.path.basename(self.filename)}\n")
            for normal, v1, v2, v3 in self.facets:
                f.write(f"facet normal {normal[0]:.6f} {normal[1]:.6f} {normal[2]:.6f}\n")
                f.write("outer loop\n")
                f.write(f"vertex {v1[0]:.6f} {v1[1]:.6f} {v1[2]:.6f}\n")
                f.write(f"vertex {v2[0]:.6f} {v2[1]:.6f} {v2[2]:.6f}\n")
                f.write(f"vertex {v3[0]:.6f} {v3[1]:.6f} {v3[2]:.6f}\n")
                f.write("endloop\n")
                f.write("endfacet\n")
            f.write(f"endsolid {os.path.basename(self.filename)}\n")
        print(f"Generated {self.filename}")

class PhotonicComponentGeneator:
    def __init__(self, output_dir="3d_models"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_substrate(self):
        """Generate base PCB substrate"""
        filename = os.path.join(self.output_dir, "tfln_substrate.stl")
        stl = STLWriter(filename)
        # Dimensions in mm
        width = 106.68
        length = 111.15
        thickness = 1.6
        stl.add_block(0, 0, 0, width, length, thickness)
        stl.write()

    def generate_waveguide_core(self):
        """Generate TFLN waveguide core geometry"""
        filename = os.path.join(self.output_dir, "tfln_waveguide_core.stl")
        stl = STLWriter(filename)
        
        # Simple Mach-Zehnder structure
        # Start input
        y_start = 10
        y_split = 30
        y_combine = 80
        y_end = 100
        
        width = 2.0 # Exaggerated for visibility (microns usually, but scaled for mm print)
        height = 1.0
        z = 1.6 # On top of substrate
        
        # Input waveguide center at x=50
        x_center = 50
        
        # Input segment
        stl.add_block(x_center - width/2, y_start, z, width, y_split - y_start, height)
        
        # Arms (Split) - Simplified as straight blocks for this demo
        arm_spacing = 10
        # Left Arm
        stl.add_block(x_center - arm_spacing - width/2, y_split, z, width, y_combine - y_split, height)
        # Right Arm
        stl.add_block(x_center + arm_spacing - width/2, y_split, z, width, y_combine - y_split, height)
        
        # Connectors (input to arms) - simple blocks for connectivity
        stl.add_block(x_center - arm_spacing + width/2, y_split, z, arm_spacing, width, height) # Bridge left
        stl.add_block(x_center - width/2, y_split, z, arm_spacing, width, height) # Bridge right? overlapping is fine for STL slicers usually
        
        # Output segment
        stl.add_block(x_center - width/2, y_combine, z, width, y_end - y_combine, height)
        
        stl.write()

    def generate_electrodes(self):
        """Generate Gold Electrodes for SLS printing or metal casting"""
        filename = os.path.join(self.output_dir, "tfln_electrodes.stl")
        stl = STLWriter(filename)
        
        x_center = 50
        arm_spacing = 10
        y_start = 35
        y_end = 75
        z = 1.6
        
        # Ground-Signal-Ground (GSG) configuration
        # Signal electrode on top of waveguide (simplified)
        e_width = 4.0
        e_height = 2.0
        
        # Left Arm Electrodes
        stl.add_block(x_center - arm_spacing - e_width/2 - 5, y_start, z, e_width, y_end - y_start, e_height) # G
        stl.add_block(x_center - arm_spacing - e_width/2, y_start, z, e_width, y_end - y_start, e_height)     # S
        stl.add_block(x_center - arm_spacing - e_width/2 + 5, y_start, z, e_width, y_end - y_start, e_height) # G
        
        # Right Arm Electrodes
        stl.add_block(x_center + arm_spacing - e_width/2 - 5, y_start, z, e_width, y_end - y_start, e_height) # G
        stl.add_block(x_center + arm_spacing - e_width/2, y_start, z, e_width, y_end - y_start, e_height)     # S
        stl.add_block(x_center + arm_spacing - e_width/2 + 5, y_start, z, e_width, y_end - y_start, e_height) # G

        stl.write()

    def generate_housing(self):
        """Generate packaging housing for 3D printing (SLS)"""
        filename = os.path.join(self.output_dir, "tfln_package_housing.stl")
        stl = STLWriter(filename)
        
        # Box around the substrate
        width = 106.68 + 4
        length = 111.15 + 4
        height = 10
        wall_thick = 2
        
        # Bottom plate
        stl.add_block(-2, -2, -2, width, length, 2)
        
        # Walls
        stl.add_block(-2, -2, -2, width, wall_thick, height) # Bottom wall
        stl.add_block(-2, length - 2 - 2, -2, width, wall_thick, height) # Top wall
        stl.add_block(-2, -2, -2, wall_thick, length, height) # Left wall
        stl.add_block(width - 2 - 2, -2, -2, wall_thick, length, height) # Right wall
        
        stl.write()

    def run(self):
        print("Generating 3D Manufacturing Models for TFLN Photonic Circuits...")
        self.generate_substrate()
        self.generate_waveguide_core()
        self.generate_electrodes()
        self.generate_housing()
        print(f"All models saved to {self.output_dir}/")

if __name__ == "__main__":
    generator = PhotonicComponentGeneator()
    generator.run()
