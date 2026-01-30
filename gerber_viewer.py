"""
TFLN Gerber File Viewer
Parses and visualizes Gerber files for TFLN photonic modulator PCB
"""

import re
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Dict
import json

@dataclass
class GerberAperture:
    """Represents a Gerber aperture definition"""
    code: int
    shape: str  # 'C' for circle, 'R' for rectangle
    size: List[float]  # [diameter] for circle, [width, height] for rectangle

@dataclass
class GerberElement:
    """Represents a drawing element"""
    element_type: str  # 'line', 'flash', 'arc'
    aperture: int
    start: Tuple[float, float]
    end: Tuple[float, float]
    interpolation: str = 'linear'  # 'linear' or 'arc'

class GerberParser:
    """Parse Gerber RS-274X files"""
    
    def __init__(self):
        self.apertures: Dict[int, GerberAperture] = {}
        self.elements: List[GerberElement] = []
        self.current_aperture = None
        self.current_pos = (0.0, 0.0)
        self.unit_scale = 1.0  # mm
        self.format_spec = (3, 6)  # Default format
        
    def parse_file(self, filepath: str) -> Dict:
        """Parse a Gerber file and return visualization data"""
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Parse format specification
        format_match = re.search(r'%FSLAX(\d)(\d)Y(\d)(\d)\*%', content)
        if format_match:
            self.format_spec = (int(format_match.group(1)), int(format_match.group(2)))
        
        # Parse unit (MOIN = inches, MOMM = mm)
        if '%MOIN*%' in content:
            self.unit_scale = 25.4  # Convert inches to mm
        else:
            self.unit_scale = 1.0
        
        # Parse aperture definitions
        aperture_pattern = r'%ADD(\d+)([CR]),([0-9.]+)(?:X([0-9.]+))?\*%'
        for match in re.finditer(aperture_pattern, content):
            code = int(match.group(1))
            shape = match.group(2)
            size1 = float(match.group(3)) * self.unit_scale
            size2 = float(match.group(4)) * self.unit_scale if match.group(4) else size1
            
            if shape == 'C':
                self.apertures[code] = GerberAperture(code, 'circle', [size1])
            else:  # Rectangle
                self.apertures[code] = GerberAperture(code, 'rectangle', [size1, size2])
        
        # Parse drawing commands
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            
            # Select aperture
            if line.startswith('D') and line.endswith('*'):
                try:
                    d_code = int(line[1:-1])
                    if d_code >= 10:  # Aperture selection
                        self.current_aperture = d_code
                except ValueError:
                    pass
            
            # Move/Draw commands
            coord_match = re.match(r'X(-?\d+)Y(-?\d+)D(\d+)\*', line)
            if coord_match:
                x = self._parse_coordinate(coord_match.group(1))
                y = self._parse_coordinate(coord_match.group(2))
                d_code = int(coord_match.group(3))
                
                if d_code == 1:  # Draw (interpolate)
                    if self.current_aperture:
                        self.elements.append(GerberElement(
                            'line',
                            self.current_aperture,
                            self.current_pos,
                            (x, y)
                        ))
                elif d_code == 2:  # Move
                    pass
                elif d_code == 3:  # Flash
                    if self.current_aperture:
                        self.elements.append(GerberElement(
                            'flash',
                            self.current_aperture,
                            (x, y),
                            (x, y)
                        ))
                
                self.current_pos = (x, y)
        
        return self._generate_visualization_data()
    
    def _parse_coordinate(self, coord_str: str) -> float:
        """Parse coordinate string based on format specification"""
        coord_int = int(coord_str)
        divisor = 10 ** self.format_spec[1]
        return (coord_int / divisor) * self.unit_scale
    
    def _generate_visualization_data(self) -> Dict:
        """Generate data structure for visualization"""
        lines = []
        pads = []
        
        for element in self.elements:
            aperture = self.apertures.get(element.aperture)
            if not aperture:
                continue
            
            if element.element_type == 'line':
                lines.append({
                    'x1': element.start[0],
                    'y1': element.start[1],
                    'x2': element.end[0],
                    'y2': element.end[1],
                    'width': aperture.size[0]
                })
            elif element.element_type == 'flash':
                pads.append({
                    'x': element.start[0],
                    'y': element.start[1],
                    'shape': aperture.shape,
                    'size': aperture.size
                })
        
        return {
            'lines': lines,
            'pads': pads,
            'apertures': {k: {'shape': v.shape, 'size': v.size} 
                         for k, v in self.apertures.items()}
        }

def parse_drill_file(filepath: str) -> Dict:
    """Parse Excellon drill file"""
    tools = {}
    holes = []
    current_tool = None
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            
            # Tool definition
            tool_match = re.match(r'T(\d+)C([0-9.]+)', line)
            if tool_match:
                tool_num = int(tool_match.group(1))
                diameter = float(tool_match.group(2)) * 25.4  # inches to mm
                tools[tool_num] = diameter
            
            # Tool selection
            if line.startswith('T') and not 'C' in line:
                try:
                    current_tool = int(line[1:])
                except ValueError:
                    pass
            
            # Hole coordinates
            coord_match = re.match(r'X(-?[0-9.]+)Y(-?[0-9.]+)', line)
            if coord_match and current_tool:
                x = float(coord_match.group(1))
                y = float(coord_match.group(2))
                holes.append({
                    'x': x,
                    'y': y,
                    'diameter': tools.get(current_tool, 0.3)
                })
    
    return {'holes': holes, 'tools': tools}

def generate_all_layers(gerber_dir: str = 'gerber_files') -> Dict:
    """Generate visualization data for all Gerber layers"""
    import os
    
    base_path = gerber_dir
    layers = {}
    
    layer_files = {
        'top': 'tfln_modulator_top.gtl',
        'bottom': 'tfln_modulator_bottom.gbl',
        'l2': 'tfln_modulator_l2.g2',
        'l3': 'tfln_modulator_l3.g3',
        'top_mask': 'tfln_modulator_top_mask.gts',
        'bottom_mask': 'tfln_modulator_bottom_mask.gbs',
        'silk': 'tfln_modulator_top_silk.gto',
        'outline': 'tfln_modulator_outline.gm1',
        'drill': 'tfln_modulator.drl'
    }
    
    parser = GerberParser()
    
    for layer_name, filename in layer_files.items():
        filepath = os.path.join(base_path, filename)
        if os.path.exists(filepath):
            try:
                if layer_name == 'drill':
                    layers[layer_name] = parse_drill_file(filepath)
                else:
                    layers[layer_name] = parser.parse_file(filepath)
                    parser = GerberParser()  # Reset for next file
            except Exception as e:
                print(f"Error parsing {filename}: {e}")
                layers[layer_name] = {'lines': [], 'pads': [], 'apertures': {}}
    
    # Add layer metadata
    layer_info = {
        'top': {'name': 'L1 - Top Signal', 'color': '#CC0000', 'description': 'RF traces, TFLN electrodes'},
        'l2': {'name': 'L2 - Signal', 'color': '#0000CC', 'description': 'High-speed differential pairs'},
        'l3': {'name': 'L3 - Power', 'color': '#CC6600', 'description': '+3.3V plane'},
        'bottom': {'name': 'L8 - Bottom Ground', 'color': '#006600', 'description': 'Ground plane'},
        'top_mask': {'name': 'Top Solder Mask', 'color': '#00AA00', 'description': 'Solder mask openings'},
        'bottom_mask': {'name': 'Bottom Solder Mask', 'color': '#00AA00', 'description': 'Solder mask openings'},
        'silk': {'name': 'Top Silkscreen', 'color': '#FFFFFF', 'description': 'Component labels'},
        'outline': {'name': 'Board Outline', 'color': '#FFFF00', 'description': 'PCB edge'},
        'drill': {'name': 'Drill Holes', 'color': '#888888', 'description': 'Through-hole vias and pads'}
    }
    
    return {
        'layers': layers,
        'layer_info': layer_info,
        'board_specs': {
            'width': 106.68,
            'height': 111.15,
            'layer_count': 8,
            'material': 'Rogers RO4350B',
            'copper_weight': '1 oz (35 μm)',
            'min_trace_space': '6/6 mil',
            'impedance': '50 Ω single-ended, 100 Ω differential'
        }
    }

if __name__ == '__main__':
    # Test the parser
    data = generate_all_layers()
    print(json.dumps(data, indent=2))
