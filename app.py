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

app = Flask(__name__)

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
    wavelengths = wdm_system.resonance_wavelengths(center=1550.0, num=64)
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
