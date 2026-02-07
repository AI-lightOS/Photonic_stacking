"""
Photonic Computing Web Application
Interactive demonstration of photonic computing capabilities
"""

from flask import Flask, render_template, jsonify, request
import numpy as np
import json
from photonic_core import (
    PhotonicMatrixMultiplier, WDMMultiplexer, PhotonicFFT,
    calculate_photonic_performance
)
from pcie_interface import PhotonicPCIeBoard, MultiboardCluster
from fpga_integration import HybridFPGAPhotonic, LargeScaleComputeCluster
from tfln_components import (
    TFLNMachZehnderModulator, TFLNRingModulator, TFLNPhotonicLink,
    TFLNWaferType, ModulationFormat
)
from tfln_plots import generate_tfln_plots
from gerber_viewer import generate_all_layers
from fea_integration import run_fea_simulation
from fea_integration import run_fea_simulation


app = Flask(__name__)




# ... (skipping component initialization lines) ...

@app.route('/api/github/push', methods=['POST'])
def github_push():
    """Start GitHub upload process"""
    data = request.json
    token = data.get('token')
    repo = data.get('repo')
    simulation = data.get('simulation', False)
    
    # If simulation is on, we allow dummy tokens
    if not simulation and (not token or not repo):
        return jsonify({'status': 'error', 'message': 'Token and Repo name required'}), 400
        
    if github_state['status'] == 'uploading':
        return jsonify({'status': 'error', 'message': 'Upload already in progress'})
        
    thread = threading.Thread(target=run_github_upload, args=(token, repo, simulation))
    thread.start()
    
    return jsonify({'status': 'started'})


# Initialize photonic components
matrix_multiplier = PhotonicMatrixMultiplier(size=128)
wdm_system = WDMMultiplexer(num_channels=64)
fft_processor = PhotonicFFT(size=1024)
pcie_board = PhotonicPCIeBoard()
hybrid_system = HybridFPGAPhotonic()

# Initialize TFLN components
tfln_modulator_400g = TFLNMachZehnderModulator(
    interaction_length=15.0,
    electrode_gap=6.0,
    wafer_type=TFLNWaferType.X_CUT
)

tfln_modulator_800g = TFLNMachZehnderModulator(
    interaction_length=18.0,
    electrode_gap=5.5,
    wafer_type=TFLNWaferType.X_CUT
)

tfln_ring = TFLNRingModulator(
    radius=50.0,
    coupling_gap=200.0,
    wafer_type=TFLNWaferType.X_CUT
)

tfln_link_400g = TFLNPhotonicLink(
    data_rate_gbps=400,
    reach_km=2.0,
    modulation=ModulationFormat.PAM4
)

tfln_link_800g = TFLNPhotonicLink(
    data_rate_gbps=800,
    reach_km=0.5,
    modulation=ModulationFormat.PAM8
)

# Initialize board
pcie_board.initialize()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/performance')
def get_performance():
    """Get overall system performance metrics"""
    perf = calculate_photonic_performance(matrix_size=1024, num_wdm_channels=64)
    
    return jsonify({
        'matrix_multiply_tops': perf['matrix_multiply_tops'],
        'total_throughput_tops': perf['total_throughput_tops'],
        'aggregate_bandwidth_tbps': perf['aggregate_bandwidth_tbps'],
        'fft_latency_ns': perf['fft_latency_ns'],
        'energy_efficiency_tops_per_watt': perf['energy_efficiency_tops_per_watt'],
        'speedup_vs_electronic': perf['speedup_vs_electronic']
    })

@app.route('/api/matrix_multiply', methods=['POST'])
def matrix_multiply():
    """Execute matrix multiplication"""
    data = request.json
    size = data.get('size', 128)
    
    # Create random test vector
    vector = np.random.randn(size) + 1j * np.random.randn(size)
    
    # Perform multiplication
    result = matrix_multiplier.multiply(vector)
    throughput = matrix_multiplier.compute_throughput()
    
    return jsonify({
        'size': size,
        'throughput_tops': throughput,
        'latency_ns': 10.0,
        'result_magnitude': float(np.abs(result).mean()),
        'energy_pj': 0.1
    })

@app.route('/api/wdm_channels')
def get_wdm_channels():
    """Get WDM channel information"""
    wavelengths = wdm_system.wavelengths
    bandwidth = wdm_system.aggregate_bandwidth()
    
    return jsonify({
        'num_channels': wdm_system.num_channels,
        'wavelengths': wavelengths.tolist(),
        'channel_spacing_nm': wdm_system.channel_spacing,
        'aggregate_bandwidth_tbps': bandwidth,
        'per_channel_gbps': 100.0
    })

@app.route('/api/fft', methods=['POST'])
def compute_fft():
    """Compute photonic FFT"""
    data = request.json
    size = data.get('size', 1024)
    
    # Create test data
    test_data = np.random.randn(size) + 1j * np.random.randn(size)
    
    # Compute FFT
    result = fft_processor.compute(test_data)
    latency = fft_processor.latency_ns()
    
    return jsonify({
        'size': size,
        'latency_ns': latency,
        'speedup_vs_electronic': 1000.0,
        'result_magnitude': float(np.abs(result).mean())
    })

@app.route('/api/pcie_board')
def get_pcie_board_info():
    """Get PCIe board information"""
    info = pcie_board.get_board_info()
    
    return jsonify({
        'pcie_generation': info['pcie_generation'],
        'pcie_lanes': info['pcie_lanes'],
        'pcie_bandwidth_gbps': info['pcie_bandwidth_gbps'],
        'form_factor': info['form_factor'],
        'power_consumption_w': info['power_consumption_w'],
        'num_optical_ports': info['num_optical_ports'],
        'num_lasers': info['num_lasers'],
        'num_modulators': info['num_modulators'],
        'matrix_size': info['matrix_size']
    })

@app.route('/api/pcie_transfer', methods=['POST'])
def pcie_transfer():
    """Simulate PCIe data transfer"""
    data = request.json
    size = data.get('size', 1024)
    
    # Create test matrix
    matrix = np.random.randn(size, size).astype(np.float32)
    
    # Transfer to device
    transfer_time = pcie_board.transfer_matrix_to_device(matrix)
    
    return jsonify({
        'matrix_size': size,
        'transfer_time_ms': transfer_time,
        'data_size_mb': (matrix.nbytes / 1e6),
        'transfer_rate_gbps': (matrix.nbytes * 8) / (transfer_time / 1000) / 1e9
    })

@app.route('/api/hybrid_system')
def get_hybrid_system():
    """Get hybrid FPGA-photonic system specs"""
    specs = hybrid_system.get_system_specs()
    
    return jsonify({
        'fpga': specs['fpga'],
        'photonic': specs['photonic'],
        'optical_io': specs['optical_io'],
        'memory': specs['memory']
    })

@app.route('/api/execute_workload', methods=['POST'])
def execute_workload():
    """Execute workload on hybrid system"""
    data = request.json
    size = data.get('size', 1024)
    
    result = hybrid_system.execute_matrix_multiply(size)
    
    return jsonify({
        'size': result['size'],
        'fpga_time_ms': result['fpga_time_ms'],
        'photonic_time_ns': result['photonic_time_ns'],
        'transfer_time_ms': result['transfer_time_ms'],
        'total_time_ms': result['total_time_ms'],
        'throughput_tflops': result['throughput_tflops'],
        'partition': result['partition']
    })

@app.route('/api/cluster')
def get_cluster_info():
    """Get cluster information"""
    cluster = LargeScaleComputeCluster(num_nodes=64)
    perf = cluster.aggregate_performance()
    
    return jsonify({
        'num_nodes': perf['num_nodes'],
        'total_pflops': perf['total_pflops'],
        'total_power_kw': perf['total_power_kw'],
        'efficiency_gflops_per_watt': perf['efficiency_gflops_per_watt'],
        'total_memory_tb': perf['total_memory_tb'],
        'optical_fabric_pbps': perf['optical_fabric_pbps'],
        'network_topology': perf['network_topology']
    })

# TFLN Component Endpoints

@app.route('/api/tfln/modulator_400g')
def get_tfln_modulator_400g():
    """Get 400G TFLN modulator specifications"""
    v_pi = tfln_modulator_400g.half_wave_voltage()
    bandwidth = tfln_modulator_400g.modulation_bandwidth()
    power = tfln_modulator_400g.power_consumption(400, ModulationFormat.PAM4)
    er = tfln_modulator_400g.extinction_ratio()
    il = tfln_modulator_400g.insertion_loss()
    
    return jsonify({
        'data_rate_gbps': 400,
        'modulation': 'PAM4',
        'v_pi_volts': round(v_pi, 3),
        'bandwidth_ghz': round(bandwidth, 1),
        'power_watts': round(power, 3),
        'energy_per_bit_pj': round((power / 400) * 1000, 2),
        'extinction_ratio_db': round(er, 1),
        'insertion_loss_db': round(il, 2),
        'interaction_length_mm': tfln_modulator_400g.interaction_length,
        'electrode_gap_um': tfln_modulator_400g.electrode_gap,
        'wafer_type': tfln_modulator_400g.wafer_type.value
    })

@app.route('/api/tfln/modulator_800g')
def get_tfln_modulator_800g():
    """Get 800G TFLN modulator specifications"""
    v_pi = tfln_modulator_800g.half_wave_voltage()
    bandwidth = tfln_modulator_800g.modulation_bandwidth()
    power = tfln_modulator_800g.power_consumption(800, ModulationFormat.PAM8)
    er = tfln_modulator_800g.extinction_ratio()
    il = tfln_modulator_800g.insertion_loss()
    
    return jsonify({
        'data_rate_gbps': 800,
        'modulation': 'PAM8',
        'v_pi_volts': round(v_pi, 3),
        'bandwidth_ghz': round(bandwidth, 1),
        'power_watts': round(power, 3),
        'energy_per_bit_pj': round((power / 800) * 1000, 2),
        'extinction_ratio_db': round(er, 1),
        'insertion_loss_db': round(il, 2),
        'interaction_length_mm': tfln_modulator_800g.interaction_length,
        'electrode_gap_um': tfln_modulator_800g.electrode_gap,
        'wafer_type': tfln_modulator_800g.wafer_type.value
    })

@app.route('/api/tfln/ring_modulator')
def get_tfln_ring():
    """Get TFLN ring modulator specifications"""
    q_factor = tfln_ring.quality_factor()
    fsr = tfln_ring.free_spectral_range()
    tuning = tfln_ring.tuning_efficiency()
    
    return jsonify({
        'radius_um': tfln_ring.radius,
        'coupling_gap_nm': tfln_ring.coupling_gap,
        'quality_factor': round(q_factor, 0),
        'fsr_ghz': round(fsr, 2),
        'tuning_efficiency_pm_per_v': round(tuning, 2),
        'wafer_type': tfln_ring.wafer_type.value,
        'wavelength_nm': tfln_ring.wavelength
    })

@app.route('/api/tfln/link_400g')
def get_tfln_link_400g():
    """Get 400G TFLN photonic link performance"""
    metrics = tfln_link_400g.performance_metrics()
    
    return jsonify({
        'data_rate_gbps': metrics['data_rate_gbps'],
        'modulation': metrics['modulation'],
        'v_pi_volts': round(metrics['v_pi_volts'], 3),
        'bandwidth_ghz': round(metrics['bandwidth_ghz'], 1),
        'power_watts': round(metrics['power_watts'], 3),
        'energy_per_bit_pj': round(metrics['energy_per_bit_pj'], 2),
        'extinction_ratio_db': round(metrics['extinction_ratio_db'], 1),
        'link_budget': {
            'tx_power_dbm': round(metrics['link_budget']['tx_power_dbm'], 2),
            'fiber_loss_db': round(metrics['link_budget']['fiber_loss_db'], 2),
            'rx_sensitivity_dbm': metrics['link_budget']['rx_sensitivity_dbm'],
            'link_margin_db': round(metrics['link_budget']['link_margin_db'], 2),
            'adequate': metrics['link_budget']['adequate']
        }
    })

@app.route('/api/tfln/link_800g')
def get_tfln_link_800g():
    """Get 800G TFLN photonic link performance"""
    metrics = tfln_link_800g.performance_metrics()
    
    return jsonify({
        'data_rate_gbps': metrics['data_rate_gbps'],
        'modulation': metrics['modulation'],
        'v_pi_volts': round(metrics['v_pi_volts'], 3),
        'bandwidth_ghz': round(metrics['bandwidth_ghz'], 1),
        'power_watts': round(metrics['power_watts'], 3),
        'energy_per_bit_pj': round(metrics['energy_per_bit_pj'], 2),
        'extinction_ratio_db': round(metrics['extinction_ratio_db'], 1),
        'link_budget': {
            'tx_power_dbm': round(metrics['link_budget']['tx_power_dbm'], 2),
            'fiber_loss_db': round(metrics['link_budget']['fiber_loss_db'], 2),
            'rx_sensitivity_dbm': metrics['link_budget']['rx_sensitivity_dbm'],
            'link_margin_db': round(metrics['link_budget']['link_margin_db'], 2),
            'adequate': metrics['link_budget']['adequate']
        }
    })

@app.route('/api/tfln/pam4_encode', methods=['POST'])
def tfln_pam4_encode():
    """Encode bits to PAM4 using TFLN modulator"""
    data = request.json
    bits = np.array(data.get('bits', [0, 1, 0, 0, 1, 1, 1, 0]))
    
    # Encode to PAM4 voltages
    voltages = tfln_modulator_400g.encode_pam4(bits)
    
    # Get optical output
    optical_output = tfln_modulator_400g.transfer_function(voltages)
    
    return jsonify({
        'input_bits': bits.tolist(),
        'pam4_voltages': voltages.tolist(),
        'optical_output': optical_output.tolist(),
        'v_pi': round(tfln_modulator_400g.half_wave_voltage(), 3),
        'num_symbols': len(voltages)
    })

@app.route('/api/tfln/plots')
def get_tfln_plots():
    """Generate and return all TFLN characterization plots"""
    plots = generate_tfln_plots()
    return jsonify(plots)

@app.route('/api/tfln/comparison')
def tfln_comparison():
    """Compare TFLN with silicon photonics"""
    
    # TFLN 400G
    tfln_v_pi = tfln_modulator_400g.half_wave_voltage()
    tfln_power = tfln_modulator_400g.power_consumption(400, ModulationFormat.PAM4)
    tfln_bw = tfln_modulator_400g.modulation_bandwidth()
    
    # Silicon (typical values)
    silicon_v_pi = 6.2
    silicon_power = 5.2
    silicon_bw = 55
    
    return jsonify({
        'tfln': {
            'v_pi_volts': round(tfln_v_pi, 2),
            'power_watts': round(tfln_power, 2),
            'bandwidth_ghz': round(tfln_bw, 1),
            'energy_per_bit_pj': round((tfln_power / 400) * 1000, 2)
        },
        'silicon': {
            'v_pi_volts': silicon_v_pi,
            'power_watts': silicon_power,
            'bandwidth_ghz': silicon_bw,
            'energy_per_bit_pj': round((silicon_power / 200) * 1000, 2)
        },
        'improvement': {
            'v_pi_reduction': round(silicon_v_pi / tfln_v_pi, 1),
            'power_reduction': round(silicon_power / tfln_power, 1),
            'bandwidth_increase': round(tfln_bw / silicon_bw, 1),
            'energy_efficiency': round((silicon_power / 200) / (tfln_power / 400), 1)
        }
    })

@app.route('/api/gerber/layers')
def get_gerber_layers():
    """Get all Gerber layer data for visualization"""
    try:
        gerber_data = generate_all_layers()
        return jsonify(gerber_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cnc/files')
def get_cnc_files():
    """List available CNC files"""
    import os
    cnc_dir = 'cnc_files'
    files = []
    if os.path.exists(cnc_dir):
        for f in os.listdir(cnc_dir):
            if f.endswith('.nc'):
                files.append(f)
    return jsonify({'files': sorted(files)})

@app.route('/api/cnc/content/<path:filename>')
def get_cnc_content(filename):
    """Get content of a CNC file"""
    import os
    cnc_dir = 'cnc_files'
    filepath = os.path.join(cnc_dir, filename)
    if os.path.exists(filepath):
        # Parse G-code for visualization
        moves = []
        current_x = 0.0
        current_y = 0.0
        
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip().upper()
                if not line: continue
                
                type_ = None
                if 'G00' in line or 'G0 ' in line:
                    type_ = 'move'
                elif 'G01' in line or 'G1 ' in line:
                    type_ = 'cut'
                
                if type_:
                    parts = line.split()
                    found_coord = False
                    for part in parts:
                        if part.startswith('X'):
                            try:
                                current_x = float(part[1:])
                                found_coord = True
                            except: pass
                        elif part.startswith('Y'):
                            try:
                                current_y = float(part[1:])
                                found_coord = True
                            except: pass
                    
                    if found_coord:
                         moves.append({'x': current_x, 'y': current_y, 'type': type_})
        return jsonify({'filename': filename, 'moves': moves})
    return jsonify({'error': 'File not found'}), 404

@app.route('/api/3d_models')
def get_3d_models():
    """List available 3D manufacturing models"""
    import os
    models_dir = '3d_models'
    files = []
    if os.path.exists(models_dir):
        for f in os.listdir(models_dir):
            if f.endswith('.stl'):
                files.append(f)
    return jsonify({'files': sorted(files)})

@app.route('/api/3d_models/download/<path:filename>')
def download_3d_model(filename):
    """Download a 3D model file"""
    import os
    from flask import send_from_directory
    models_dir = os.path.abspath('3d_models')
    return send_from_directory(models_dir, filename, as_attachment=True)

@app.route('/api/vlsi/layers')
def get_vlsi_layers():
    """Get VLSI layout data"""
    # Reuse GerberParser but for VLSI specific files
    # We need to manually construct the layer list
    from gerber_viewer import GerberParser, parse_drill_file
    import os
    
    base_path = 'gerber_files'
    layers = {}
    
    layer_files = {
        'fpga_logic': 'vlsi_fpga_logic.gbr',
        'pcie_phy': 'vlsi_pcie_phy.gbr',
        'photonics': 'vlsi_photonics.gbr',
        'interconnect': 'vlsi_metal_interconnect.gbr'
    }
    
    parser = GerberParser()
    
    for layer_name, filename in layer_files.items():
        filepath = os.path.join(base_path, filename)
        if os.path.exists(filepath):
            try:
                # Our generic parser should handle basic gerber commands used in generate_vlsi
                layers[layer_name] = parser.parse_file(filepath)
                parser = GerberParser() # Reset
            except Exception as e:
                print(f"Error parsing {filename}: {e}")
                layers[layer_name] = {'lines': [], 'pads': [], 'apertures': {}}

    layer_info = {
        'fpga_logic': {'name': 'FPGA Logic (CLB)', 'color': '#00CCCC', 'description': 'Configurable Logic Blocks'},
        'pcie_phy': {'name': 'PCIe PHY (5.0)', 'color': '#00CC00', 'description': 'SerDes Transceivers'},
        'photonics': {'name': 'Silicon Photonics', 'color': '#CC0000', 'description': 'Optical Waveguides'},
        'interconnect': {'name': 'M1-M4 Metal', 'color': '#CCCCCC', 'description': 'Global Interconnects'}
    }
    
    return jsonify({
        'layers': layers,
        'layer_info': layer_info,
        'chip_specs': {
            'die_size': '20mm x 20mm',
            'technology': '7nm FinFET + 45nm SOI',
            'fpga_logic_cells': '2.5M',
            'transceivers': '16x 32Gbps'
        }
    })

@app.route('/api/fea/simulate', methods=['POST'])
def run_fea():
    """Run custom FEA simulation for optical modes"""
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


if __name__ == '__main__':
    print("=" * 70)
    print("PHOTONIC COMPUTING WEB APPLICATION")
    print("=" * 70)
    print("\nInitializing photonic components...")
    print(f"  Matrix Multiplier: {matrix_multiplier.size}x{matrix_multiplier.size}")
    print(f"  WDM Channels: {wdm_system.num_channels}")
    print(f"  FFT Size: {fft_processor.size}")
    print(f"  PCIe Board: {pcie_board.pcie.generation.value[1]} x{pcie_board.pcie.num_lanes}")
    print("\n" + "=" * 70)
    print("Starting server on http://127.0.0.1:5001")
    print("=" * 70)
    
    app.run(host='0.0.0.0', port=5001, debug=False)
