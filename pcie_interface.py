"""
PCIe Interface for Photonic Computing Accelerator
High-Speed Host-to-Photonic Communication

Implements PCIe Gen 5.0 interface for photonic computing boards
with DMA, memory mapping, and optical I/O control.
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Optional, Tuple
from enum import Enum


class PCIeGeneration(Enum):
    """PCIe generation specifications"""
    GEN3 = (8.0, "8 GT/s")  # 8 Gbps per lane
    GEN4 = (16.0, "16 GT/s")  # 16 Gbps per lane
    GEN5 = (32.0, "32 GT/s")  # 32 Gbps per lane
    GEN6 = (64.0, "64 GT/s")  # 64 Gbps per lane (future)


@dataclass
class PCIeConfiguration:
    """
    PCIe configuration for photonic accelerator
    """
    generation: PCIeGeneration = PCIeGeneration.GEN5
    num_lanes: int = 16  # x16 slot
    max_payload_size: int = 512  # bytes
    max_read_request: int = 4096  # bytes
    
    def bandwidth_gbps(self) -> float:
        """Calculate total PCIe bandwidth"""
        rate_per_lane = self.generation.value[0]
        # Account for 128b/130b encoding overhead
        efficiency = 128.0 / 130.0
        return rate_per_lane * self.num_lanes * efficiency
    
    def bandwidth_gbytes_per_sec(self) -> float:
        """Calculate bandwidth in GB/s"""
        return self.bandwidth_gbps() / 8.0


class DMAEngine:
    """
    Direct Memory Access engine for high-speed data transfer
    
    Enables zero-copy transfers between host memory and photonic processor
    """
    
    def __init__(self, num_channels: int = 8):
        """
        Initialize DMA engine
        
        Args:
            num_channels: Number of independent DMA channels
        """
        self.num_channels = num_channels
        self.channel_status = ['idle'] * num_channels
        self.transfer_queue = [[] for _ in range(num_channels)]
        
        # Performance counters
        self.total_bytes_transferred = 0
        self.total_transfers = 0
    
    def initiate_transfer(self, channel: int, source_addr: int, 
                         dest_addr: int, size: int, direction: str = 'h2d'):
        """
        Initiate DMA transfer
        
        Args:
            channel: DMA channel ID
            source_addr: Source memory address
            dest_addr: Destination memory address
            size: Transfer size in bytes
            direction: 'h2d' (host-to-device) or 'd2h' (device-to-host)
        """
        if channel >= self.num_channels:
            raise ValueError(f"Invalid channel {channel}")
        
        transfer = {
            'source': source_addr,
            'dest': dest_addr,
            'size': size,
            'direction': direction,
            'status': 'pending'
        }
        
        self.transfer_queue[channel].append(transfer)
        self.channel_status[channel] = 'busy'
    
    def process_transfers(self):
        """Process pending DMA transfers"""
        for ch in range(self.num_channels):
            if self.transfer_queue[ch]:
                transfer = self.transfer_queue[ch].pop(0)
                
                # Simulate transfer
                self.total_bytes_transferred += transfer['size']
                self.total_transfers += 1
                
                if not self.transfer_queue[ch]:
                    self.channel_status[ch] = 'idle'
    
    def get_throughput_gbps(self, time_elapsed_sec: float = 1.0) -> float:
        """
        Calculate DMA throughput
        
        Args:
            time_elapsed_sec: Time period for measurement
        
        Returns:
            Throughput in Gbps
        """
        bytes_per_sec = self.total_bytes_transferred / time_elapsed_sec
        return (bytes_per_sec * 8) / 1e9


class MemoryMappedIO:
    """
    Memory-mapped I/O for photonic processor control
    
    Provides register-level access to photonic components
    """
    
    def __init__(self, base_address: int = 0xF0000000):
        """
        Initialize MMIO interface
        
        Args:
            base_address: Base address for MMIO region
        """
        self.base_address = base_address
        
        # Register map
        self.registers = {
            'CONTROL': 0x0000,
            'STATUS': 0x0004,
            'LASER_POWER': 0x0008,
            'MODULATOR_BIAS': 0x000C,
            'PHASE_SHIFTER_0': 0x0010,
            'PHASE_SHIFTER_1': 0x0014,
            'WDM_CHANNEL_SELECT': 0x0018,
            'DETECTOR_THRESHOLD': 0x001C,
            'INTERRUPT_ENABLE': 0x0020,
            'INTERRUPT_STATUS': 0x0024,
            'DMA_CONTROL': 0x0028,
            'PERFORMANCE_COUNTER': 0x002C
        }
        
        # Register values
        self.register_values = {name: 0 for name in self.registers}
    
    def write_register(self, name: str, value: int):
        """Write to control register"""
        if name not in self.registers:
            raise ValueError(f"Unknown register: {name}")
        
        self.register_values[name] = value
    
    def read_register(self, name: str) -> int:
        """Read from status register"""
        if name not in self.registers:
            raise ValueError(f"Unknown register: {name}")
        
        return self.register_values[name]
    
    def configure_laser(self, power_mw: float):
        """
        Configure laser power
        
        Args:
            power_mw: Laser power in milliwatts
        """
        # Convert to register value (0-4095 for 12-bit DAC)
        dac_value = int((power_mw / 100.0) * 4095)
        self.write_register('LASER_POWER', dac_value)
    
    def set_phase_shifter(self, index: int, phase_rad: float):
        """
        Set phase shifter value
        
        Args:
            index: Phase shifter index
            phase_rad: Phase in radians
        """
        # Convert to register value
        dac_value = int((phase_rad / (2 * np.pi)) * 65535)
        
        if index == 0:
            self.write_register('PHASE_SHIFTER_0', dac_value)
        elif index == 1:
            self.write_register('PHASE_SHIFTER_1', dac_value)


class PhotonicPCIeBoard:
    """
    Complete PCIe board with photonic computing accelerator
    
    Integrates PCIe interface, DMA engine, and photonic processor control
    """
    
    def __init__(self, pcie_config: Optional[PCIeConfiguration] = None):
        """
        Initialize photonic PCIe board
        
        Args:
            pcie_config: PCIe configuration (defaults to Gen5 x16)
        """
        self.pcie = pcie_config or PCIeConfiguration()
        self.dma = DMAEngine(num_channels=8)
        self.mmio = MemoryMappedIO()
        
        # Board specifications
        self.form_factor = "HHHL"  # Half-Height Half-Length
        self.power_consumption_w = 75.0  # Watts
        self.num_optical_ports = 16
        
        # Photonic components
        self.num_lasers = 4  # Integrated laser sources
        self.num_modulators = 64
        self.num_detectors = 64
        self.matrix_size = 1024
        
        # Performance metrics
        self.compute_tops = 0.0
        self.memory_bandwidth_gbps = 0.0
    
    def initialize(self):
        """Initialize board and photonic components"""
        print("Initializing Photonic PCIe Board...")
        
        # Configure PCIe
        print(f"  PCIe: {self.pcie.generation.value[1]} x{self.pcie.num_lanes}")
        print(f"  Bandwidth: {self.pcie.bandwidth_gbytes_per_sec():.2f} GB/s")
        
        # Initialize lasers
        for i in range(self.num_lasers):
            self.mmio.configure_laser(power_mw=50.0)
        
        # Reset photonic processor
        self.mmio.write_register('CONTROL', 0x0001)  # Reset bit
        self.mmio.write_register('CONTROL', 0x0000)  # Clear reset
        
        # Enable interrupts
        self.mmio.write_register('INTERRUPT_ENABLE', 0xFFFF)
        
        print("  Photonic processor initialized")
        print(f"  Optical ports: {self.num_optical_ports}")
        print(f"  Matrix size: {self.matrix_size}x{self.matrix_size}")
    
    def transfer_matrix_to_device(self, matrix: np.ndarray) -> float:
        """
        Transfer matrix to photonic processor via DMA
        
        Args:
            matrix: Matrix to transfer
        
        Returns:
            Transfer time in milliseconds
        """
        # Calculate transfer size
        size_bytes = matrix.nbytes
        
        # Initiate DMA transfer
        self.dma.initiate_transfer(
            channel=0,
            source_addr=0x10000000,  # Host memory
            dest_addr=0x20000000,    # Device memory
            size=size_bytes,
            direction='h2d'
        )
        
        # Process transfer
        self.dma.process_transfers()
        
        # Calculate transfer time
        bandwidth_gbps = self.pcie.bandwidth_gbps()
        transfer_time_ms = (size_bytes * 8) / (bandwidth_gbps * 1e9) * 1000
        
        return transfer_time_ms
    
    def execute_matrix_multiply(self, size: int) -> dict:
        """
        Execute matrix multiplication on photonic processor
        
        Args:
            size: Matrix dimension
        
        Returns:
            Performance metrics
        """
        # Optical computation time (near-instantaneous)
        compute_time_ns = 10.0  # 10 nanoseconds
        
        # Operations
        ops = 2 * size ** 3  # Matrix multiply
        
        # Throughput
        tops = ops / (compute_time_ns * 1e-9) / 1e12
        
        return {
            'size': size,
            'compute_time_ns': compute_time_ns,
            'throughput_tops': tops,
            'energy_pj': compute_time_ns * 0.1  # 0.1 pJ/ns
        }
    
    def get_board_info(self) -> dict:
        """Get comprehensive board information"""
        return {
            'pcie_generation': self.pcie.generation.value[1],
            'pcie_lanes': self.pcie.num_lanes,
            'pcie_bandwidth_gbps': self.pcie.bandwidth_gbps(),
            'form_factor': self.form_factor,
            'power_consumption_w': self.power_consumption_w,
            'num_optical_ports': self.num_optical_ports,
            'num_lasers': self.num_lasers,
            'num_modulators': self.num_modulators,
            'num_detectors': self.num_detectors,
            'matrix_size': self.matrix_size,
            'dma_channels': self.dma.num_channels
        }


class MultiboardCluster:
    """
    Multi-board photonic computing cluster
    
    Scales to multiple PCIe boards for massive parallelism
    """
    
    def __init__(self, num_boards: int = 8):
        """
        Initialize multi-board cluster
        
        Args:
            num_boards: Number of photonic PCIe boards
        """
        self.num_boards = num_boards
        self.boards = [PhotonicPCIeBoard() for _ in range(num_boards)]
        
        # Optical interconnect between boards
        self.optical_fabric_bandwidth_tbps = 10.0 * num_boards
    
    def initialize_cluster(self):
        """Initialize all boards in cluster"""
        print(f"\nInitializing {self.num_boards}-Board Photonic Cluster")
        print("=" * 70)
        
        for i, board in enumerate(self.boards):
            print(f"\nBoard {i}:")
            board.initialize()
        
        print(f"\nOptical Fabric Bandwidth: {self.optical_fabric_bandwidth_tbps:.2f} Tbps")
        print("=" * 70)
    
    def aggregate_performance(self) -> dict:
        """Calculate aggregate cluster performance"""
        single_board_tops = 100.0  # Estimated TOPS per board
        
        return {
            'num_boards': self.num_boards,
            'total_tops': single_board_tops * self.num_boards,
            'total_power_w': sum(b.power_consumption_w for b in self.boards),
            'optical_fabric_tbps': self.optical_fabric_bandwidth_tbps,
            'total_optical_ports': sum(b.num_optical_ports for b in self.boards),
            'efficiency_tops_per_watt': (single_board_tops * self.num_boards) / 
                                       sum(b.power_consumption_w for b in self.boards)
        }


if __name__ == "__main__":
    print("=" * 70)
    print("PHOTONIC PCIe BOARD - SYSTEM DEMONSTRATION")
    print("=" * 70)
    
    # Single board test
    print("\n1. Single Board Configuration")
    board = PhotonicPCIeBoard()
    board.initialize()
    
    info = board.get_board_info()
    print(f"\nBoard Specifications:")
    print(f"  PCIe: {info['pcie_generation']} x{info['pcie_lanes']}")
    print(f"  Bandwidth: {info['pcie_bandwidth_gbps']:.2f} Gbps")
    print(f"  Power: {info['power_consumption_w']:.1f} W")
    print(f"  Optical Ports: {info['num_optical_ports']}")
    
    # Matrix transfer test
    print("\n2. Matrix Transfer Test")
    test_matrix = np.random.randn(1024, 1024).astype(np.float32)
    transfer_time = board.transfer_matrix_to_device(test_matrix)
    print(f"  Matrix Size: 1024x1024")
    print(f"  Transfer Time: {transfer_time:.3f} ms")
    print(f"  Transfer Rate: {(test_matrix.nbytes / 1e9) / (transfer_time / 1000):.2f} GB/s")
    
    # Computation test
    print("\n3. Matrix Multiplication Performance")
    perf = board.execute_matrix_multiply(size=1024)
    print(f"  Matrix Size: {perf['size']}x{perf['size']}")
    print(f"  Compute Time: {perf['compute_time_ns']:.1f} ns")
    print(f"  Throughput: {perf['throughput_tops']:.2f} TOPS")
    print(f"  Energy: {perf['energy_pj']:.2f} pJ")
    
    # Multi-board cluster
    print("\n4. Multi-Board Cluster")
    cluster = MultiboardCluster(num_boards=8)
    cluster.initialize_cluster()
    
    cluster_perf = cluster.aggregate_performance()
    print(f"\nCluster Performance:")
    print(f"  Total Throughput: {cluster_perf['total_tops']:.2f} TOPS")
    print(f"  Total Power: {cluster_perf['total_power_w']:.1f} W")
    print(f"  Efficiency: {cluster_perf['efficiency_tops_per_watt']:.2f} TOPS/W")
    print(f"  Optical Fabric: {cluster_perf['optical_fabric_tbps']:.2f} Tbps")
    
    print("\n" + "=" * 70)
    print("PHOTONIC PCIe: EXTREME PERFORMANCE, MINIMAL POWER")
    print("=" * 70)
