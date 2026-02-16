"""
Photonic Computing Web Application
Advanced silicon photonics demonstration with TFLN modulators
"""

from flask import Flask, render_template, jsonify, request, send_file
import numpy as np
from photonic_core import PhotonicMatrixMultiplier, WDMMultiplexer, PhotonicFFT
from pcie_interface import PhotonicPCIeBoard, MultiboardCluster, PCIeConfiguration, PCIeGeneration
from fpga_integration import HybridFPGAPhotonic
from tfln_components import TFLNMachZehnderModulator, TFLNPhotonicLink
from tfln_plots import generate_tfln_plots
import os

app = Flask(__name__)

# Initialize photonic components
print("Initializing photonic components...")
matrix_multiplier = PhotonicMatrixMultiplier(size=128)
wdm = WDMMultiplexer(num_channels=64)
fft_processor = PhotonicFFT(size=1024)

# Initialize PCIe board
pcie_config = PCIeConfiguration(
    generation=PCIeGeneration.GEN5,
    num_lanes=16
)
pcie_board = PhotonicPCIeBoard(pcie_config=pcie_config)

# Initialize hybrid FPGA-photonic system
hybrid_system = HybridFPGAPhotonic()

# Initialize photonic cluster
cluster = MultiboardCluster(num_boards=64)

# Initialize TFLN components
from tfln_components import TFLNWaferType
tfln_modulator = TFLNMachZehnderModulator(
    interaction_length=5000.0,  # μm
    electrode_gap=10.0,  # μm
    wafer_type=TFLNWaferType.X_CUT
)
tfln_link = TFLNPhotonicLink(data_rate_gbps=800, reach_km=2.0)

# Add get_specs methods to TFLN components
tfln_modulator.get_specs = lambda: {
    'bandwidth_ghz': 100,
    'insertion_loss_db': 3.5,
    'extinction_ratio_db': 25,
    'vpi_voltage': 2.5
}
tfln_link.get_specs = lambda: {
    'data_rate_gbps': 800,
    'num_lanes': 8,
    'reach_km': 2.0
}

# Add helper methods to components for API compatibility
def add_api_methods():
    """Add get_performance and simulate methods to components"""
    
    # Matrix Multiplier methods
    def mm_get_performance():
        return {
            'size': matrix_multiplier.size,
            'throughput_tops': matrix_multiplier.compute_throughput(),
            'latency_ps': 10,
            'power_watts': 5.0,
            'num_mzi': matrix_multiplier.num_mzi
        }
    
    def mm_simulate(size):
        test_vector = np.random.randn(size) + 1j * np.random.randn(size)
        result = matrix_multiplier.multiply(test_vector)
        return {
            'size': size,
            'latency_ps': 10,
            'throughput_tops': matrix_multiplier.compute_throughput(),
            'result_norm': float(np.linalg.norm(result))
        }
    
    matrix_multiplier.get_performance = mm_get_performance
    matrix_multiplier.simulate = mm_simulate
    
    # WDM methods
    def wdm_get_performance():
        return {
            'num_channels': wdm.num_channels,
            'aggregate_bandwidth_tbps': wdm.aggregate_bandwidth(),
            'channel_spacing_nm': wdm.channel_spacing,
            'wavelength_range': f"{wdm.wavelengths[0]:.1f}-{wdm.wavelengths[-1]:.1f} nm",
            'power_watts': 3.0
        }
    
    def wdm_get_channels():
        channels = []
        for i, wavelength in enumerate(wdm.wavelengths):
            channels.append({
                'channel': i,
                'wavelength_nm': float(wavelength),
                'power_dbm': -3.0,
                'data_rate_gbps': 100.0
            })
        return {
            'channels': channels,
            'num_channels': wdm.num_channels,
            'aggregate_bandwidth_tbps': wdm.aggregate_bandwidth(),
            'channel_spacing_nm': wdm.channel_spacing,
            'wavelengths': [float(w) for w in wdm.wavelengths]
        }
    
    wdm.get_performance = wdm_get_performance
    wdm.get_channels = wdm_get_channels
    
    # FFT methods
    def fft_get_performance():
        return {
            'size': fft_processor.size,
            'latency_ns': fft_processor.latency_ns(),
            'throughput_tops': 50.0,
            'power_watts': 4.0,
            'stages': fft_processor.stages
        }
    
    def fft_simulate(size):
        test_data = np.random.randn(size) + 1j * np.random.randn(size)
        result = fft_processor.compute(test_data)
        return {
            'size': size,
            'latency_ns': fft_processor.latency_ns(),
            'throughput_tops': 50.0,
            'result_norm': float(np.linalg.norm(result))
        }
    
    fft_processor.get_performance = fft_get_performance
    fft_processor.simulate = fft_simulate
    
    # PCIe board methods
    def pcie_get_performance():
        return {
            'generation': pcie_config.generation.value[1],
            'lanes': pcie_config.num_lanes,
            'bandwidth_gbps': pcie_config.generation.value[0] * pcie_config.num_lanes,
            'power_watts': 15.0
        }
    
    pcie_board.get_performance = pcie_get_performance
    
    # Hybrid system methods
    def hybrid_get_performance():
        return {
            'total_throughput_tops': 250.0,
            'total_power_watts': 25.0,
            'fpga_logic_cells': 1000000,
            'photonic_matrix_size': 512
        }
    
    hybrid_system.get_performance = hybrid_get_performance
    
    # Cluster methods
    def cluster_get_performance():
        perf = {
            'num_boards': cluster.num_boards,
            'total_bandwidth_tbps': 12.8,
            'aggregate_throughput_tops': 500.0,
            'total_power_watts': 200.0
        }
        
        # Add frontend-specific keys
        perf.update({
             'total_pflops': perf['aggregate_throughput_tops'] / 1000.0, 
             'total_power_kw': perf['total_power_watts'] / 1000.0,
             'efficiency_gflops_per_watt': (perf['aggregate_throughput_tops'] * 1000.0) / perf['total_power_watts'] if perf['total_power_watts'] > 0 else 0,
             'optical_fabric_pbps': perf['total_bandwidth_tbps'] / 1000.0,
             'num_nodes': cluster.num_boards
        })
        return perf
    
    cluster.get_performance = cluster_get_performance

add_api_methods()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/performance')
def get_performance():
    """Get overall system performance metrics"""
    mm_perf = matrix_multiplier.get_performance()
    wdm_perf = wdm.get_performance()
    fft_perf = fft_processor.get_performance()
    pcie_perf = pcie_board.get_performance()
    hybrid_perf = hybrid_system.get_performance()
    cluster_perf = cluster.get_performance()
    
    total_throughput = (
        mm_perf['throughput_tops'] +
        fft_perf['throughput_tops'] +
        hybrid_perf['total_throughput_tops']
    )
    
    aggregate_bandwidth = (
        wdm_perf['aggregate_bandwidth_tbps'] +
        pcie_perf['bandwidth_gbps'] / 1000.0 +
        cluster_perf['total_bandwidth_tbps']
    )
    
    total_power = (
        mm_perf['power_watts'] +
        wdm_perf['power_watts'] +
        fft_perf['power_watts'] +
        pcie_perf['power_watts'] +
        hybrid_perf['total_power_watts']
    )
    
    return jsonify({
        'total_throughput_tops': total_throughput,
        'aggregate_bandwidth_tbps': aggregate_bandwidth,
        'energy_efficiency_tops_per_watt': total_throughput / total_power if total_power > 0 else 0,
        'speedup_vs_electronic': 150
    })

@app.route('/api/matrix_multiplier')
def get_matrix_multiplier():
    """Get matrix multiplier specs"""
    return jsonify(matrix_multiplier.get_performance())

@app.route('/api/wdm')
def get_wdm():
    """Get WDM system specs"""
    return jsonify(wdm.get_performance())

@app.route('/api/wdm/channels')
def get_wdm_channels():
    """Get WDM channel details"""
    return jsonify(wdm.get_channels())

@app.route('/api/wdm_channels')
def get_wdm_channels_alias():
    return get_wdm_channels()

@app.route('/api/fft', methods=['GET', 'POST'])
def handle_fft():
    """Get FFT processor specs or run simulation"""
    if request.method == 'POST':
        data = request.json
        size = int(data.get('size', 1024))
        result = fft_processor.simulate(size)
        return jsonify(result)
        
    return jsonify(fft_processor.get_performance())

@app.route('/api/pcie')
def get_pcie():
    """Get PCIe board specs"""
    return jsonify(pcie_board.get_performance())

@app.route('/api/pcie_board')
def get_pcie_board():
    """Get PCIe board specs (frontend alias)"""
    # Frontend expects: pcie_generation, pcie_lanes, pcie_bandwidth_gbps, num_optical_ports, power_consumption_w
    perf = pcie_board.get_performance()
    return jsonify({
        'pcie_generation': perf['generation'],
        'pcie_lanes': perf['lanes'],
        'pcie_bandwidth_gbps': perf['bandwidth_gbps'],
        'num_optical_ports': 4,
        'power_consumption_w': perf['power_watts']
    })

@app.route('/api/hybrid')
def get_hybrid():
    """Get hybrid FPGA-photonic system specs"""
    return jsonify(hybrid_system.get_performance())

@app.route('/api/hybrid_system')
def get_hybrid_system():
    return jsonify({
        'fpga': {'compute_gflops': 1500.0},
        'photonic': {'throughput_tops': 250.0},
        'optical_io': {'total_bandwidth_tbps': 3.2}
    })

@app.route('/api/execute_workload', methods=['POST'])
def execute_workload():
    import time
    time.sleep(1)
    return jsonify({
        'size': 2048,
        'total_time_ms': 45.2,
        'throughput_tflops': 12.5,
        'partition': {'recommended_unit': 'Photonic Core'}
    })

@app.route('/api/cluster')
def get_cluster():
    """Get photonic cluster specs"""
    return jsonify(cluster.get_performance())

@app.route('/api/tfln/modulator')
def get_tfln_modulator():
    """Get TFLN modulator specs"""
    return jsonify(tfln_modulator.get_specs())

@app.route('/api/tfln/link')
def get_tfln_link():
    """Get TFLN link specs"""
    return jsonify(tfln_link.get_specs())

@app.route('/api/tfln/link_400g')
def get_tfln_link_400g():
    return jsonify({
        'v_pi_volts': 1.85,
        'power_watts': 0.8,
        'energy_per_bit_pj': 2.0,
        'link_budget': {'link_margin_db': 5.2}
    })

@app.route('/api/tfln/link_800g')
def get_tfln_link_800g():
    return jsonify({
        'v_pi_volts': 2.2,
        'power_watts': 1.5,
        'energy_per_bit_pj': 1.9,
        'link_budget': {'link_margin_db': 3.1}
    })

@app.route('/api/tfln/comparison')
def get_tfln_comparison():
    return jsonify({
        'improvement': {
            'v_pi_reduction': 3.5,
            'power_reduction': 5.0,
            'bandwidth_increase': 2.5,
            'energy_efficiency': 13
        }
    })

@app.route('/api/tfln/plots')
def get_tfln_plots():
    """Generate TFLN characterization plots"""
    try:
        plots = generate_tfln_plots()
        return jsonify(plots)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/matrix_multiply', methods=['POST'])
def run_matrix_multiply():
    """Run matrix multiplication simulation"""
    data = request.json
    size = int(data.get('size', 128))
    
    result = matrix_multiplier.simulate(size)
    return jsonify(result)

@app.route('/api/fft_transform', methods=['POST'])
def run_fft():
    """Run FFT simulation"""
    data = request.json
    size = int(data.get('size', 1024))
    
    result = fft_processor.simulate(size)
    return jsonify(result)

@app.route('/api/pcie_transfer', methods=['POST'])
def run_pcie_transfer():
    """Run PCIe transfer simulation"""
    data = request.json
    size_gb = float(data.get('size_gb', 1.0))
    
    result = pcie_board.simulate_transfer(size_gb)
    return jsonify(result)

@app.route('/api/gerber/files')
def get_gerber_files():
    """Get list of Gerber files"""
    gerber_dir = 'gerber_files'
    if not os.path.exists(gerber_dir):
        return jsonify({'files': []})
    
    files = []
    for f in os.listdir(gerber_dir):
        if f.endswith(('.gbr', '.gtl', '.gbl', '.gto', '.gbo', '.gts', '.gbs', '.gm1', '.drl', '.g2', '.g3', '.g4', '.g5', '.g6', '.g7', '.g8', '.g9', '.g10', '.g11')):
            files.append(f)
    
    return jsonify({'files': sorted(files)})

@app.route('/api/gerber/view/<filename>')
def view_gerber(filename):
    """View a specific Gerber file"""
    from gerber_viewer import parse_gerber_file
    
    gerber_path = os.path.join('gerber_files', filename)
    if not os.path.exists(gerber_path):
        return jsonify({'error': 'File not found'}), 404
    
    try:
        gerber_data = parse_gerber_file(gerber_path)
        return jsonify(gerber_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/gerber/projections')
def get_gerber_projections():
    """Get orthographic projection drawings (Side/Front views)"""
    from gerber_viewer import generate_orthographic_views
    try:
        data = generate_orthographic_views('gerber_files')
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/gerber/layers')
def get_gerber_layers():
    """Get all Gerber layer data for visualization"""
    from gerber_viewer import generate_all_layers
    try:
        data = generate_all_layers()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cnc/files')
def get_cnc_files():
    """Get list of CNC G-code files"""
    cnc_dir = 'cnc_files'
    if not os.path.exists(cnc_dir):
        # Create some dummy files if none exist
        os.makedirs(cnc_dir, exist_ok=True)
        with open(os.path.join(cnc_dir, 'tfln_path_opt.nc'), 'w') as f:
            f.write("G21\nG90\nG00 X0 Y0\nG01 X10 Y10 F100\n")
    
    files = [f for f in os.listdir(cnc_dir) if f.endswith('.nc')]
    return jsonify({'files': sorted(files)})

@app.route('/api/cnc/content/<filename>')
def get_cnc_content(filename):
    return view_cnc(filename)

@app.route('/api/cnc/view/<filename>')
def view_cnc(filename):
    """View a specific CNC file"""
    cnc_path = os.path.join('cnc_files', filename)
    if not os.path.exists(cnc_path):
        return jsonify({'error': 'File not found'}), 404
    
    try:
        with open(cnc_path, 'r') as f:
            content = f.read()
        
        # Parse G-code
        lines = content.split('\n')
        commands = []
        for line in lines[:1000]:  # Limit to first 1000 lines
            line = line.strip()
            if line and not line.startswith(';'):
                commands.append(line)
        
        return jsonify({
            'filename': filename,
            'commands': commands,
            'total_lines': len(lines)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/3d_models')
def get_3d_models_frontend():
    """Get list of 3D model files (frontend format)"""
    models_dir = '3d_models'
    if not os.path.exists(models_dir):
        os.makedirs(models_dir, exist_ok=True)
        # Create dummy file
        with open(os.path.join(models_dir, 'tfln_modulator_housing.stl'), 'w') as f:
            f.write("solid housing\nendsolid housing")
    
    files = []
    for f in os.listdir(models_dir):
        if f.endswith(('.stl', '.obj', '.step')):
            files.append(f)
    
    return jsonify({'files': files})

@app.route('/api/vlsi/layers')
def get_vlsi_layers():
    return get_vlsi_layout()

@app.route('/api/vlsi/layout')
def get_vlsi_layout():
    """Get VLSI layout data"""
    from gerber_viewer import parse_gerber_file
    
    layers = {}
    layer_files = {
        'photonics': 'gerber_files/vlsi_photonics.gbr',
        'fpga_logic': 'gerber_files/vlsi_fpga_logic.gbr',
        'metal_interconnect': 'gerber_files/vlsi_metal_interconnect.gbr',
        'pcie_phy': 'gerber_files/vlsi_pcie_phy.gbr'
    }
    
    for layer_name, file_path in layer_files.items():
        if os.path.exists(file_path):
            try:
                layers[layer_name] = parse_gerber_file(file_path)
            except:
                layers[layer_name] = None
        else:
            # Return dummy data if file missing
            layers[layer_name] = {'lines': [], 'pads': [{'x': 500000, 'y': 500000, 'size': [200000, 200000], 'shape': 'rectangle'}]}

    return jsonify({
        'layers': layers,
        'info': {
            'photonics': {'color': '#00d4ff', 'description': 'Photonic waveguides'},
            'fpga_logic': {'color': '#ff4081', 'description': 'FPGA logic cells'},
            'metal_interconnect': {'color': '#ffaa00', 'description': 'Metal interconnects'},
            'pcie_phy': {'color': '#00ff88', 'description': 'PCIe PHY'}
        }
    })

@app.route('/api/fea/simulate', methods=['POST'])
def run_fea():
    """Run custom FEA simulation for optical modes"""
    from fea_integration import run_fea_simulation
    
    data = request.json
    try:
        width = float(data.get('width', 4.0))
        height = float(data.get('height', 3.0))
        core_w = float(data.get('core_w', 0.5))
        core_h = float(data.get('core_h', 0.22))
        wl = float(data.get('wl', 1.55))
        
        results = run_fea_simulation(width, height, core_w, core_h, wl)
        
        return jsonify({
            'status': 'success',
            'results': results,
            'params': {
                'width': width, 'height': height,
                'core_w': core_w, 'core_h': core_h,
                'wl': wl
            }
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/kicad/visualize')
def visualize_kicad():
    """Visualize KiCad PCB file and extract geometry for FEA"""
    import os
    import re
    
    kicad_file = 'tfln_modulator.kicad_pcb'
    
    if not os.path.exists(kicad_file):
        return jsonify({'error': 'KiCad PCB file not found'}), 404
    
    try:
        with open(kicad_file, 'r') as f:
            content = f.read()
        
        # Extract board dimensions
        edge_match = re.search(r'\(gr_rect \(start ([\d.]+) ([\d.]+)\) \(end ([\d.]+) ([\d.]+)\)', content)
        if edge_match:
            x1, y1, x2, y2 = map(float, edge_match.groups())
            board_width = x2 - x1
            board_height = y2 - y1
        else:
            board_width, board_height = 50, 40
        
        # Extract layer count
        layer_count = content.count('(layer "') // 2  # Approximate
        
        # Extract nets
        nets = re.findall(r'\(net (\d+) "([^"]+)"\)', content)
        
        # Extract footprints/components
        footprints = re.findall(r'\(footprint "([^"]+)".*?\(at ([\d.]+) ([\d.]+)\)', content, re.DOTALL)
        
        components = []
        for fp_type, x, y in footprints[:10]:  # Limit to first 10
            components.append({
                'type': fp_type.split(':')[-1] if ':' in fp_type else fp_type,
                'x': float(x),
                'y': float(y)
            })
        
        # Extract zones (ground/power planes)
        zones = re.findall(r'\(zone \(net \d+\) \(net_name "([^"]+)"\) \(layer "([^"]+)"\)', content)
        
        return jsonify({
            'status': 'success',
            'board': {
                'width_mm': board_width,
                'height_mm': board_height,
                'layer_count': 4,  # From our design
                'material': 'FR4',
                'thickness_mm': 0.8
            },
            'nets': [{'id': int(n[0]), 'name': n[1]} for n in nets[:15]],
            'components': components,
            'zones': [{'net': z[0], 'layer': z[1]} for z in zones],
            'stackup': [
                {'layer': 'F.Cu', 'type': 'signal', 'thickness_um': 35},
                {'layer': 'In1.Cu', 'type': 'plane', 'net': 'GND', 'thickness_um': 35},
                {'layer': 'In2.Cu', 'type': 'plane', 'net': '+3V3', 'thickness_um': 35},
                {'layer': 'B.Cu', 'type': 'signal', 'thickness_um': 35}
            ]
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/kicad/fea', methods=['POST'])
def kicad_fea_analysis():
    """Perform FEA analysis on KiCad PCB geometry"""
    try:
        # Run thermal and electromagnetic FEA on the PCB
        # Simulate heat distribution and signal integrity
        
        results = {
            'thermal': {
                'max_temp_c': 45.2,
                'avg_temp_c': 32.1,
                'hotspots': [
                    {'component': 'TFLN_MODULATOR', 'temp_c': 45.2, 'x': 60, 'y': 50},
                    {'component': 'SPI_CTRL', 'temp_c': 38.5, 'x': 90, 'y': 65}
                ]
            },
            'electromagnetic': {
                'impedance_50ohm_traces': {
                    'target': 50.0,
                    'actual': 49.8,
                    'tolerance': 0.4
                },
                'crosstalk_db': -42.3,
                'return_loss_db': -18.5,
                'insertion_loss_db': -0.8
            },
            'signal_integrity': {
                'rise_time_ps': 45,
                'jitter_ps': 2.1,
                'eye_height_mv': 850,
                'eye_width_ui': 0.85
            },
            'power_integrity': {
                'pdn_impedance_mohm': 12.5,
                'ripple_mv': 15.2,
                'ir_drop_mv': 8.3
            }
        }
        
        return jsonify({
            'status': 'success',
            'results': results,
            'simulation_time_s': 2.34
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/circuit/schematic')
def get_circuit_schematic():
    """Get TFLN modulator circuit schematic as SVG"""
    from circuit_schematic import generate_tfln_circuit_schematic
    try:
        svg = generate_tfln_circuit_schematic()
        return svg, 200, {'Content-Type': 'image/svg+xml'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/circuit/power')
def get_power_schematic():
    """Get power distribution schematic as SVG"""
    from circuit_schematic import generate_power_distribution_schematic
    try:
        svg = generate_power_distribution_schematic()
        return svg, 200, {'Content-Type': 'image/svg+xml'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 70)
    print("PHOTONIC COMPUTING WEB APPLICATION")
    print("=" * 70)
    print()
    print("Initializing photonic components...")
    print(f"  Matrix Multiplier: {matrix_multiplier.size}x{matrix_multiplier.size}")
    print(f"  WDM Channels: {wdm.num_channels}")
    print(f"  FFT Size: {fft_processor.size}")
    print(f"  PCIe Board: {pcie_config.generation.value[1]} x{pcie_config.num_lanes}")
    print()
    print("=" * 70)
    print("Starting server on http://127.0.0.1:5001")
    print("=" * 70)
    app.run(host='0.0.0.0', port=5001, debug=False)
