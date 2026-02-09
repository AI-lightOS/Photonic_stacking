#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# PHOTONIC AI CHIP - USB CONTROL SOFTWARE
# ═══════════════════════════════════════════════════════════════════════════════
#
# Purpose: Control the photonic neural processor via FT2232H USB interface
# Features:
#   - Set phase shifter tuning voltages (0-3.3V, 12-bit resolution)
#   - Read spike data from 8 neurons in real-time
#   - Data logging and analysis
#   - Simple command-line interface
#
# Requirements: pyftdi, numpy, matplotlib (optional for plotting)
#
# Installation:
#   pip install pyftdi numpy matplotlib
#
# ═══════════════════════════════════════════════════════════════════════════════

import sys
import time
import struct
import numpy as np
from datetime import datetime
from collections import deque

try:
    from pyftdi.ftdi import Ftdi
    from pyftdi.usbtools import UsbTools
except ImportError:
    print("ERROR: pyftdi not installed. Install with: pip install pyftdi")
    sys.exit(1)

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Warning: matplotlib not available. Plotting disabled.")

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

# FT2232H USB device configuration
FTDI_VENDOR_ID = 0x0403
FTDI_PRODUCT_ID = 0x6010
DEVICE_URL = "ftdi://ftdi:2232h/1"  # Interface A (SPI for DAC)

# SPI Configuration (for AD5684 DAC)
SPI_FREQUENCY = 10e6  # 10 MHz SPI clock
DAC_REFERENCE_VOLTAGE = 3.3  # 3.3V DAC reference

# AD5684 DAC Configuration
DAC_RESOLUTION = 12  # bits
DAC_CHANNELS = 4  # quad DAC (need 2x for 8 neurons)
DAC_MAX_CODE = (1 << DAC_RESOLUTION) - 1  # 4095

# Photodiode & comparator configuration
NUM_NEURONS = 8
COMPARATOR_THRESHOLD = 1.65  # volts (TIA output threshold for spike)

# ═══════════════════════════════════════════════════════════════════════════════
# CLASS: PhotonicAIChip
# ═══════════════════════════════════════════════════════════════════════════════

class PhotonicAIChip:
    """
    Interface to the Photonic AI Chip via USB (FT2232H)
    
    Methods:
        - connect(): Establish USB connection
        - disconnect(): Close USB connection
        - set_threshold(neuron_id, voltage): Set phase shifter voltage
        - read_spikes(): Poll for spike events
        - sweep_threshold(): Sweep threshold to find sensitivity
        - record_spikes(duration): Record spike data for analysis
    """
    
    def __init__(self, verbose=True):
        """Initialize USB interface"""
        self.ftdi = None
        self.verbose = verbose
        self.connected = False
        
        # Data buffers
        self.spike_buffer = deque(maxlen=10000)  # Last 10k spikes
        self.threshold_values = np.zeros(NUM_NEURONS)  # Current DAC settings
        
        if verbose:
            print("[PhotonicAI] Initializing USB interface...")
    
    def connect(self):
        """Establish USB connection to FT2232H"""
        try:
            self.ftdi = Ftdi()
            self.ftdi.open(FTDI_VENDOR_ID, FTDI_PRODUCT_ID, interface=1)  # Interface A
            
            # Configure SPI parameters
            self.ftdi.set_bitmode(0xFF, Ftdi.BITMODE_MPSSE)
            self.ftdi.set_frequency(SPI_FREQUENCY)
            
            self.connected = True
            if self.verbose:
                print("[✓] USB connection established")
                print(f"    Device: FT2232H")
                print(f"    SPI frequency: {SPI_FREQUENCY/1e6} MHz")
            
            return True
        
        except Exception as e:
            print(f"[✗] Failed to connect: {e}")
            print("\nAvailable USB devices:")
            try:
                devices = UsbTools.find_all([(FTDI_VENDOR_ID, FTDI_PRODUCT_ID)])
                for dev in devices:
                    print(f"  - {dev}")
            except:
                print("  (none found)")
            return False
    
    def disconnect(self):
        """Close USB connection"""
        if self.ftdi:
            self.ftdi.close()
            self.connected = False
            if self.verbose:
                print("[✓] USB disconnected")
    
    def _dac_command(self, dac_id, channel, voltage):
        """
        Generate AD5684 SPI command word
        
        AD5684 command format (24-bit):
        Bits [23:20] = Command (0: Write to input register)
        Bits [19:16] = Address (0-3 for channel select, 15 for all)
        Bits [15:0]  = Data (12-bit DAC code in upper 12 bits)
        
        Args:
            dac_id: DAC number (0-1, we have 2 DACs for 8 channels)
            channel: Channel on DAC (0-3)
            voltage: Output voltage (0.0 to 3.3V)
        
        Returns:
            24-bit command word
        """
        
        # Convert voltage (0-3.3V) to 12-bit code (0-4095)
        code = int((voltage / DAC_REFERENCE_VOLTAGE) * DAC_MAX_CODE)
        code = max(0, min(code, DAC_MAX_CODE))  # Clamp to valid range
        
        # AD5684 command bits
        command = 0x0  # Write to input register
        address = channel & 0xF
        data = (code & 0xFFF) << 4  # 12-bit code in upper 12 bits
        
        # Assemble 24-bit word
        cmd_word = (command << 20) | (address << 16) | data
        
        return cmd_word
    
    def _spi_write(self, cmd_word):
        """
        Send 24-bit command to DAC via SPI
        
        Args:
            cmd_word: 24-bit DAC command
        
        Returns:
            True if successful
        """
        if not self.connected:
            print("[✗] Not connected to device")
            return False
        
        try:
            # Convert to 3 bytes (MSB first)
            cmd_bytes = [
                (cmd_word >> 16) & 0xFF,
                (cmd_word >> 8) & 0xFF,
                cmd_word & 0xFF
            ]
            
            # Send via SPI (no chip select handling in this simplified version)
            self.ftdi.write(cmd_bytes)
            time.sleep(0.001)  # Small delay for DAC settling
            
            return True
        
        except Exception as e:
            print(f"[✗] SPI write failed: {e}")
            return False
    
    def set_phase_shifter(self, neuron_id, voltage):
        """
        Set phase shifter tuning voltage for a single neuron
        
        The phase shifter voltage controls the threshold of the neuron.
        Higher voltage = higher threshold = less likely to spike
        
        Args:
            neuron_id: Neuron number (0-7)
            voltage: Tuning voltage (0.0 to 3.3V)
        
        Returns:
            True if successful
        """
        if not 0 <= neuron_id < NUM_NEURONS:
            print(f"[✗] Invalid neuron ID: {neuron_id} (0-{NUM_NEURONS-1})")
            return False
        
        if not 0.0 <= voltage <= DAC_REFERENCE_VOLTAGE:
            print(f"[✗] Invalid voltage: {voltage} (0.0-{DAC_REFERENCE_VOLTAGE}V)")
            return False
        
        # Map neuron ID to DAC and channel
        dac_id = neuron_id // 4  # DAC 0 for neurons 0-3, DAC 1 for 4-7
        channel = neuron_id % 4  # Channel within DAC
        
        # Generate and send SPI command
        cmd_word = self._dac_command(dac_id, channel, voltage)
        
        if self._spi_write(cmd_word):
            self.threshold_values[neuron_id] = voltage
            if self.verbose:
                print(f"[✓] Neuron {neuron_id}: {voltage:.3f}V")
            return True
        else:
            return False
    
    def set_all_thresholds(self, voltage_array):
        """
        Set all 8 neuron thresholds at once
        
        Args:
            voltage_array: List of 8 voltages (0.0-3.3V)
        
        Returns:
            True if all successful
        """
        if len(voltage_array) != NUM_NEURONS:
            print(f"[✗] Expected {NUM_NEURONS} voltages, got {len(voltage_array)}")
            return False
        
        print("[→] Setting all thresholds...")
        success = True
        for neuron_id, voltage in enumerate(voltage_array):
            if not self.set_phase_shifter(neuron_id, voltage):
                success = False
        
        return success
    
    def get_current_thresholds(self):
        """Return current threshold settings"""
        return self.threshold_values.copy()
    
    def read_spikes_uart(self, timeout_ms=1000):
        """
        Read spike data from comparator outputs via UART
        
        (Simplified mock implementation - actual implementation requires
         configuring FT2232H Channel B as UART)
        
        This is where you would:
        1. Read data from UART interface (FT2232H Channel B)
        2. Decode spike messages (which neurons fired)
        3. Return timestamped spike data
        
        Args:
            timeout_ms: Timeout for reading (milliseconds)
        
        Returns:
            List of spike events: [(neuron_id, timestamp_us), ...]
        """
        
        # TODO: Implement actual UART reading from FT2232H Channel B
        # For now, return mock data
        spikes = []
        
        # In real implementation:
        # 1. Read from self.ftdi.read() on UART channel
        # 2. Parse protocol (e.g., 1 byte = spike bitmask for all 8 neurons)
        # 3. Timestamped based on USB packet timing
        
        return spikes
    
    def poll_spikes(self, duration_ms=100, poll_interval_ms=10):
        """
        Poll for spike events over a duration
        
        Args:
            duration_ms: How long to monitor (milliseconds)
            poll_interval_ms: Poll interval (milliseconds)
        
        Returns:
            Dictionary: {neuron_id: spike_count}
        """
        spike_counts = {i: 0 for i in range(NUM_NEURONS)}
        
        start_time = time.time()
        
        while (time.time() - start_time) * 1000 < duration_ms:
            spikes = self.read_spikes_uart(timeout_ms=poll_interval_ms)
            
            for neuron_id, _ in spikes:
                spike_counts[neuron_id] += 1
            
            time.sleep(poll_interval_ms / 1000.0)
        
        return spike_counts
    
    def sweep_threshold(self, neuron_id, start_v=0.5, stop_v=3.0, step_v=0.1, 
                       measurement_time_ms=100):
        """
        Sweep phase shifter voltage to characterize neuron sensitivity
        
        This helps understand how each neuron responds to threshold changes.
        
        Args:
            neuron_id: Which neuron to test (0-7)
            start_v: Starting voltage (volts)
            stop_v: Ending voltage (volts)
            step_v: Voltage step size (volts)
            measurement_time_ms: Time to measure spikes at each voltage
        
        Returns:
            Tuple: (voltage_list, spike_count_list)
        """
        
        if not 0 <= neuron_id < NUM_NEURONS:
            print(f"[✗] Invalid neuron ID")
            return None, None
        
        voltages = np.arange(start_v, stop_v + step_v, step_v)
        spike_counts = []
        
        print(f"\n[→] Threshold sweep: Neuron {neuron_id}")
        print(f"    Range: {start_v:.2f}V to {stop_v:.2f}V, Step: {step_v:.2f}V")
        print(f"    Measurement time: {measurement_time_ms}ms per point\n")
        
        for voltage in voltages:
            # Set threshold
            self.set_phase_shifter(neuron_id, voltage)
            
            # Measure spikes at this voltage
            spike_dict = self.poll_spikes(duration_ms=measurement_time_ms)
            count = spike_dict.get(neuron_id, 0)
            spike_counts.append(count)
            
            print(f"    {voltage:.2f}V: {count:4d} spikes")
        
        print()
        return voltages, np.array(spike_counts)
    
    def record_spikes(self, duration_seconds=10, save_file=None):
        """
        Record spike data for long-duration analysis
        
        Args:
            duration_seconds: Recording duration
            save_file: Optional filename to save data (CSV format)
        
        Returns:
            Spike data: List of (timestamp, neuron_id) tuples
        """
        
        print(f"[→] Recording spikes for {duration_seconds} seconds...")
        start_time = time.time()
        spike_data = []
        
        while (time.time() - start_time) < duration_seconds:
            spikes = self.read_spikes_uart(timeout_ms=100)
            spike_data.extend(spikes)
        
        print(f"[✓] Recorded {len(spike_data)} spike events")
        
        # Optional: Save to file
        if save_file:
            with open(save_file, 'w') as f:
                f.write("timestamp_us, neuron_id\n")
                for timestamp, neuron_id in spike_data:
                    f.write(f"{timestamp}, {neuron_id}\n")
            print(f"[✓] Data saved to {save_file}")
        
        return spike_data
    
    def plot_threshold_curve(self, voltages, spike_counts):
        """
        Plot neuron sensitivity (threshold sweep result)
        
        Args:
            voltages: Array of voltage settings
            spike_counts: Array of spike counts at each voltage
        """
        
        if not MATPLOTLIB_AVAILABLE:
            print("[✗] matplotlib not available for plotting")
            return
        
        plt.figure(figsize=(10, 6))
        plt.plot(voltages, spike_counts, 'o-', linewidth=2, markersize=8)
        plt.xlabel('Phase Shifter Voltage (V)', fontsize=12)
        plt.ylabel('Spike Count (100ms window)', fontsize=12)
        plt.title('Neuron Sensitivity Curve', fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()


# ═══════════════════════════════════════════════════════════════════════════════
# COMMAND-LINE INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Interactive command-line interface"""
    
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║         PHOTONIC AI CHIP - USB CONTROL SOFTWARE               ║")
    print("║                 8-Neuron Optical Processor                    ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")
    
    # Initialize device
    chip = PhotonicAIChip(verbose=True)
    
    if not chip.connect():
        print("\n[✗] Failed to connect to device. Exiting.")
        sys.exit(1)
    
    print("\nAvailable commands:")
    print("  set <neuron> <voltage>  - Set phase shifter (e.g., 'set 0 1.5')")
    print("  all <voltage>           - Set all neurons to same voltage")
    print("  sweep <neuron>          - Sweep threshold to characterize neuron")
    print("  read <time_ms>          - Read spikes for duration")
    print("  status                  - Show current settings")
    print("  help                    - Show this help")
    print("  quit                    - Exit\n")
    
    while True:
        try:
            cmd = input("chip> ").strip()
            
            if not cmd:
                continue
            
            parts = cmd.split()
            command = parts[0].lower()
            
            if command == "quit" or command == "exit":
                print("[→] Disconnecting...")
                chip.disconnect()
                print("Goodbye!")
                break
            
            elif command == "set":
                if len(parts) < 3:
                    print("[✗] Usage: set <neuron> <voltage>")
                    continue
                neuron_id = int(parts[1])
                voltage = float(parts[2])
                chip.set_phase_shifter(neuron_id, voltage)
            
            elif command == "all":
                if len(parts) < 2:
                    print("[✗] Usage: all <voltage>")
                    continue
                voltage = float(parts[1])
                voltages = [voltage] * NUM_NEURONS
                chip.set_all_thresholds(voltages)
            
            elif command == "sweep":
                if len(parts) < 2:
                    print("[✗] Usage: sweep <neuron>")
                    continue
                neuron_id = int(parts[1])
                voltages, counts = chip.sweep_threshold(neuron_id)
                if voltages is not None:
                    chip.plot_threshold_curve(voltages, counts)
            
            elif command == "read":
                if len(parts) < 2:
                    duration_ms = 1000
                else:
                    duration_ms = int(parts[1])
                spike_dict = chip.poll_spikes(duration_ms=duration_ms)
                print("\nSpike counts:")
                for neuron_id in range(NUM_NEURONS):
                    print(f"  Neuron {neuron_id}: {spike_dict[neuron_id]} spikes")
            
            elif command == "status":
                print("\nCurrent phase shifter settings:")
                for neuron_id, voltage in enumerate(chip.get_current_thresholds()):
                    print(f"  Neuron {neuron_id}: {voltage:.3f}V")
            
            elif command == "help":
                print("See commands listed above")
            
            else:
                print(f"[✗] Unknown command: {command}")
        
        except ValueError as e:
            print(f"[✗] Invalid value: {e}")
        except KeyboardInterrupt:
            print("\n[→] Interrupted by user")
            chip.disconnect()
            break
        except Exception as e:
            print(f"[✗] Error: {e}")


if __name__ == "__main__":
    main()

# ═══════════════════════════════════════════════════════════════════════════════
# END OF PHOTONIC AI CONTROL SOFTWARE
# ═══════════════════════════════════════════════════════════════════════════════
