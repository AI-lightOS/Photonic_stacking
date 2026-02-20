"""
Thin-Film Lithium Niobate (TFLN) Photonic Components
Advanced electro-optic modulators and integrated photonic devices
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Optional
from enum import Enum


class TFLNWaferType(Enum):
    """TFLN wafer types"""
    X_CUT = "X-cut"
    Y_CUT = "Y-cut"
    Z_CUT = "Z-cut"


class ModulationFormat(Enum):
    """Modulation formats"""
    OOK = "On-Off Keying"
    PAM4 = "4-level PAM"
    PAM8 = "8-level PAM"
    QAM16 = "16-QAM"
    QAM64 = "64-QAM"


@dataclass
class TFLNMaterialProperties:
    """Material properties of thin-film lithium niobate"""
    
    # Refractive indices at 1550nm
    n_ordinary: float = 2.211
    n_extraordinary: float = 2.138
    
    # Electro-optic coefficients (pm/V)
    r33: float = 30.8  # Largest coefficient
    r13: float = 8.6
    r22: float = 3.4
    
    # Thermo-optic coefficient (1/K)
    dn_dt: float = 3.0e-5
    
    # Propagation loss (dB/cm)
    loss_te: float = 0.27
    loss_tm: float = 0.30
    
    # Nonlinear coefficients
    chi2: float = 27.0  # pm/V (second-order)
    chi3: float = 2.5e-22  # m²/V² (third-order)
    
    def get_pockels_coefficient(self, wafer_type: TFLNWaferType) -> float:
        """Get effective Pockels coefficient based on wafer cut"""
        if wafer_type == TFLNWaferType.X_CUT:
            return self.r33
        elif wafer_type == TFLNWaferType.Y_CUT:
            return self.r22
        else:  # Z-cut
            return self.r13


@dataclass
class TFLNWaveguide:
    """Thin-film lithium niobate waveguide"""
    
    width: float  # μm
    height: float  # μm (film thickness)
    length: float  # mm
    wafer_type: TFLNWaferType
    wavelength: float = 1550.0  # nm
    
    def __post_init__(self):
        self.material = TFLNMaterialProperties()
    
    def effective_index(self, polarization: str = 'TE') -> float:
        """Calculate effective refractive index"""
        # Simplified effective index using Marcatili's method
        n_core = self.material.n_extraordinary if polarization == 'TE' else self.material.n_ordinary
        n_clad = 1.45  # SiO2 cladding
        
        # Confinement factor approximation
        V = (2 * np.pi / (self.wavelength * 1e-3)) * self.width * np.sqrt(n_core**2 - n_clad**2)
        
        if V < 2.405:  # Single mode
            b = (V / 2.405)**2
        else:
            b = 1 - (2.405 / V)**2
        
        n_eff = n_clad + (n_core - n_clad) * b
        return n_eff
    
    def propagation_loss(self, polarization: str = 'TE') -> float:
        """Calculate propagation loss in dB"""
        loss_per_cm = self.material.loss_te if polarization == 'TE' else self.material.loss_tm
        return loss_per_cm * (self.length / 10)  # Convert mm to cm
    
    def group_velocity(self, polarization: str = 'TE') -> float:
        """Calculate group velocity (m/s)"""
        n_eff = self.effective_index(polarization)
        c = 3e8  # Speed of light
        n_g = n_eff * 1.05  # Group index approximation
        return c / n_g
    
    def dispersion(self) -> float:
        """Calculate chromatic dispersion (ps/nm/km)"""
        # TFLN has low dispersion in C-band
        return -2.5  # ps/nm/km


@dataclass
class TFLNMachZehnderModulator:
    """High-performance TFLN Mach-Zehnder modulator"""
    
    interaction_length: float  # mm
    electrode_gap: float  # μm
    wafer_type: TFLNWaferType
    wavelength: float = 1550.0  # nm
    
    def __post_init__(self):
        self.material = TFLNMaterialProperties()
        self.waveguide = TFLNWaveguide(
            width=1.5,
            height=0.6,
            length=self.interaction_length,
            wafer_type=self.wafer_type,
            wavelength=self.wavelength
        )
    
    def half_wave_voltage(self, overlap_factor: float = 0.8) -> float:
        """Calculate Vπ (half-wave voltage)"""
        r_eff = self.material.get_pockels_coefficient(self.wafer_type)
        n_eff = self.waveguide.effective_index('TE')
        
        # Vπ = λ·d / (n³·r·Γ·L)
        wavelength_m = self.wavelength * 1e-9
        gap_m = self.electrode_gap * 1e-6
        length_m = self.interaction_length * 1e-3
        
        v_pi = (wavelength_m * gap_m) / (n_eff**3 * r_eff * 1e-12 * overlap_factor * length_m)
        return v_pi
    
    def modulation_bandwidth(self) -> float:
        """Calculate 3-dB modulation bandwidth (GHz)"""
        # Limited by velocity mismatch and electrode loss
        v_optical = self.waveguide.group_velocity('TE')
        v_rf = 1.2e8  # RF velocity in traveling wave electrode (m/s)
        
        # Velocity mismatch limited bandwidth
        delta_v = abs(v_optical - v_rf)
        length_m = self.interaction_length * 1e-3
        
        f_3db_velocity = 0.44 * v_optical / (delta_v * length_m) / 1e9  # GHz
        
        # Electrode loss limited bandwidth (typically higher)
        f_3db_loss = 120  # GHz for well-designed TFLN
        
        # Take minimum
        return min(f_3db_velocity, f_3db_loss)
    
    def extinction_ratio(self, phase_imbalance: float = 0.01) -> float:
        """Calculate extinction ratio (dB)"""
        # ER limited by phase imbalance between arms
        er = -10 * np.log10((np.pi * phase_imbalance)**2)
        return min(er, 45)  # Practical limit ~45 dB
    
    def insertion_loss(self) -> float:
        """Calculate insertion loss (dB)"""
        # Waveguide loss + splitting loss + coupling loss
        wg_loss = self.waveguide.propagation_loss('TE')
        split_loss = 0.1  # Y-junction loss
        coupling_loss = 0.5  # Fiber-chip coupling
        
        return wg_loss + split_loss + coupling_loss
    
    def power_consumption(self, data_rate_gbps: float, modulation: ModulationFormat) -> float:
        """Calculate power consumption (W)"""
        v_pi = self.half_wave_voltage()
        
        # Drive voltage depends on modulation format
        if modulation == ModulationFormat.OOK:
            v_drive = v_pi
        elif modulation == ModulationFormat.PAM4:
            v_drive = v_pi
        elif modulation == ModulationFormat.PAM8:
            v_drive = 1.2 * v_pi
        else:
            v_drive = 1.5 * v_pi
        
        # Capacitance of traveling wave electrode
        length_m = self.interaction_length * 1e-3
        capacitance = 0.15e-12 * length_m  # F/m typical for TFLN
        
        # Dynamic power: P = C·V²·f
        symbol_rate = data_rate_gbps / np.log2(4 if modulation == ModulationFormat.PAM4 else 2)
        power = capacitance * v_drive**2 * symbol_rate * 1e9
        
        # Add driver power (typically 0.3-0.5W)
        driver_power = 0.4
        
        return power + driver_power
    
    def transfer_function(self, voltage: np.ndarray) -> np.ndarray:
        """Calculate optical transfer function"""
        v_pi = self.half_wave_voltage()
        # T(V) = 0.5 * [1 + cos(π·V/Vπ)]
        return 0.5 * (1 + np.cos(np.pi * voltage / v_pi))
    
    def encode_pam4(self, bits: np.ndarray) -> np.ndarray:
        """Encode bits to PAM4 voltage levels"""
        v_pi = self.half_wave_voltage()
        
        # PAM4 levels: 00, 01, 10, 11
        levels = {
            0: 0.0,           # 00
            1: v_pi / 3,      # 01
            2: 2 * v_pi / 3,  # 10
            3: v_pi           # 11
        }
        
        # Group bits into 2-bit symbols
        symbols = []
        for i in range(0, len(bits), 2):
            if i + 1 < len(bits):
                symbol = bits[i] * 2 + bits[i+1]
                symbols.append(levels[symbol])
        
        return np.array(symbols)


@dataclass
class TFLNRingModulator:
    """TFLN ring resonator modulator for compact footprint"""
    
    radius: float  # μm
    coupling_gap: float  # nm
    wafer_type: TFLNWaferType
    wavelength: float = 1550.0  # nm
    
    def __post_init__(self):
        self.material = TFLNMaterialProperties()
        circumference = 2 * np.pi * self.radius
        self.waveguide = TFLNWaveguide(
            width=1.2,
            height=0.6,
            length=circumference / 1000,  # Convert to mm
            wafer_type=self.wafer_type,
            wavelength=self.wavelength
        )
    
    def quality_factor(self) -> float:
        """Calculate loaded quality factor"""
        n_eff = self.waveguide.effective_index('TE')
        circumference = 2 * np.pi * self.radius * 1e-6  # meters
        
        # Loss per round trip
        loss_per_cm = self.material.loss_te
        loss_per_rt = loss_per_cm * (circumference * 100)  # dB
        alpha = loss_per_rt / (10 * np.log10(np.e))  # Nepers
        
        # Q = 2π·n_eff·L / (λ·α)
        Q = (2 * np.pi * n_eff * circumference) / (self.wavelength * 1e-9 * alpha)
        
        # Account for coupling (loaded Q is lower)
        Q_loaded = Q / 2
        return Q_loaded
    
    def free_spectral_range(self) -> float:
        """Calculate FSR (GHz)"""
        n_eff = self.waveguide.effective_index('TE')
        circumference = 2 * np.pi * self.radius * 1e-6  # meters
        c = 3e8
        
        fsr = c / (n_eff * circumference) / 1e9  # GHz
        return fsr
    
    def tuning_efficiency(self) -> float:
        """Calculate electro-optic tuning efficiency (pm/V)"""
        r_eff = self.material.get_pockels_coefficient(self.wafer_type)
        n_eff = self.waveguide.effective_index('TE')
        
        # Δλ/ΔV = λ·n³·r / (2·d)
        gap_m = 5e-6  # 5 μm typical gap
        tuning = (self.wavelength * n_eff**3 * r_eff * 1e-12) / (2 * gap_m)
        return tuning * 1e12  # pm/V
    
    def modulation_depth(self, voltage: float) -> float:
        """Calculate modulation depth"""
        Q = self.quality_factor()
        tuning = self.tuning_efficiency()
        
        # Wavelength shift
        delta_lambda = tuning * voltage  # pm
        
        # Modulation depth depends on detuning
        fsr = self.free_spectral_range() * 1e3  # pm
        linewidth = fsr / Q  # pm
        
        # Lorentzian response
        detuning = delta_lambda / linewidth
        depth = 1 / (1 + detuning**2)
        
        return depth


@dataclass
class TFLNFrequencyDoubler:
    """TFLN second-harmonic generation for frequency conversion"""
    
    length: float  # mm
    poling_period: float  # μm (for quasi-phase matching)
    wavelength_pump: float = 1550.0  # nm
    
    def __post_init__(self):
        self.material = TFLNMaterialProperties()
        self.wavelength_shg = self.wavelength_pump / 2  # Second harmonic
    
    def phase_matching_period(self) -> float:
        """Calculate optimal poling period for QPM"""
        # Λ = λ / (2·Δn)
        n_pump = self.material.n_extraordinary
        n_shg = 2.25  # Approximate at 775nm
        
        delta_n = n_shg - n_pump
        period = self.wavelength_pump * 1e-3 / (2 * delta_n)  # μm
        return period
    
    def conversion_efficiency(self, pump_power_w: float) -> float:
        """Calculate SHG conversion efficiency"""
        # η = (2·ω²·d_eff²·L²·P_pump) / (ε₀·c³·n_pump²·n_shg·A)
        
        d_eff = self.material.chi2 * 1e-12  # m/V
        length_m = self.length * 1e-3
        
        # Effective mode area (μm²)
        area = 2.0 * 1e-12  # m²
        
        omega = 2 * np.pi * 3e8 / (self.wavelength_pump * 1e-9)
        epsilon_0 = 8.854e-12
        c = 3e8
        
        n_pump = self.material.n_extraordinary
        n_shg = 2.25
        
        eta = (2 * omega**2 * d_eff**2 * length_m**2 * pump_power_w) / \
              (epsilon_0 * c**3 * n_pump**2 * n_shg * area)
        
        return min(eta, 0.95)  # Practical limit


@dataclass
class TFLNElectroOpticSwitch:
    """TFLN 2x2 electro-optic switch"""
    
    interaction_length: float  # mm
    wafer_type: TFLNWaferType
    wavelength: float = 1550.0  # nm
    
    def __post_init__(self):
        self.material = TFLNMaterialProperties()
        self.mzm = TFLNMachZehnderModulator(
            interaction_length=self.interaction_length,
            electrode_gap=6.0,
            wafer_type=self.wafer_type,
            wavelength=self.wavelength
        )
    
    def switching_voltage(self) -> float:
        """Voltage required for switching"""
        return self.mzm.half_wave_voltage()
    
    def switching_time(self) -> float:
        """Switching time (ns)"""
        # Limited by RC time constant and transit time
        capacitance = 0.15e-12 * self.interaction_length * 1e-3  # F
        resistance = 50  # Ω (matched impedance)
        
        rc_time = resistance * capacitance * 1e9  # ns
        
        # Transit time
        v_rf = 1.2e8  # m/s
        transit_time = (self.interaction_length * 1e-3) / v_rf * 1e9  # ns
        
        return max(rc_time, transit_time)
    
    def crosstalk(self) -> float:
        """Crosstalk between ports (dB)"""
        er = self.mzm.extinction_ratio()
        return -er  # Crosstalk is negative of ER


class TFLNPhotonicLink:
    """Complete TFLN photonic link"""
    
    def __init__(self, data_rate_gbps: float, reach_km: float, 
                 modulation: ModulationFormat = ModulationFormat.PAM4):
        self.data_rate = data_rate_gbps
        self.reach = reach_km
        self.modulation = modulation
        
        # Components
        self.modulator = TFLNMachZehnderModulator(
            interaction_length=15.0,  # mm
            electrode_gap=6.0,  # μm
            wafer_type=TFLNWaferType.X_CUT
        )
    
    def link_budget(self) -> dict:
        """Calculate complete link budget"""
        # Transmitter
        laser_power = 3.0  # dBm
        modulator_loss = self.modulator.insertion_loss()
        tx_power = laser_power - modulator_loss
        
        # Fiber
        fiber_loss = 0.2 * self.reach  # dB/km
        
        # Receiver
        rx_sensitivity = -15.0  # dBm for PAM4 at BER 1e-15
        
        # Margin
        margin = tx_power - fiber_loss - rx_sensitivity
        
        return {
            'tx_power_dbm': tx_power,
            'fiber_loss_db': fiber_loss,
            'rx_sensitivity_dbm': rx_sensitivity,
            'link_margin_db': margin,
            'adequate': margin > 3.0
        }
    
    def performance_metrics(self) -> dict:
        """Get complete performance metrics"""
        v_pi = self.modulator.half_wave_voltage()
        bandwidth = self.modulator.modulation_bandwidth()
        power = self.modulator.power_consumption(self.data_rate, self.modulation)
        
        return {
            'data_rate_gbps': self.data_rate,
            'modulation': self.modulation.value,
            'v_pi_volts': v_pi,
            'bandwidth_ghz': bandwidth,
            'power_watts': power,
            'energy_per_bit_pj': (power / self.data_rate) * 1000,
            'extinction_ratio_db': self.modulator.extinction_ratio(),
            'link_budget': self.link_budget()
        }


def demonstrate_tfln_components():
    """Demonstrate TFLN component capabilities"""
    
    print("=" * 70)
    print("THIN-FILM LITHIUM NIOBATE (TFLN) PHOTONIC COMPONENTS")
    print("=" * 70)
    
    # 1. Mach-Zehnder Modulator
    print("\n1. TFLN Mach-Zehnder Modulator (400G PAM4)")
    mzm = TFLNMachZehnderModulator(
        interaction_length=15.0,
        electrode_gap=6.0,
        wafer_type=TFLNWaferType.X_CUT
    )
    
    print(f"   Half-Wave Voltage (Vπ): {mzm.half_wave_voltage():.2f} V")
    print(f"   Modulation Bandwidth: {mzm.modulation_bandwidth():.1f} GHz")
    print(f"   Extinction Ratio: {mzm.extinction_ratio():.1f} dB")
    print(f"   Insertion Loss: {mzm.insertion_loss():.2f} dB")
    print(f"   Power (400G PAM4): {mzm.power_consumption(400, ModulationFormat.PAM4):.2f} W")
    
    # 2. Ring Modulator
    print("\n2. TFLN Ring Resonator Modulator")
    ring = TFLNRingModulator(
        radius=50.0,
        coupling_gap=200.0,
        wafer_type=TFLNWaferType.X_CUT
    )
    
    print(f"   Quality Factor: {ring.quality_factor():.0f}")
    print(f"   Free Spectral Range: {ring.free_spectral_range():.2f} GHz")
    print(f"   Tuning Efficiency: {ring.tuning_efficiency():.2f} pm/V")
    
    # 3. Photonic Link
    print("\n3. Complete 400G TFLN Photonic Link")
    link = TFLNPhotonicLink(
        data_rate_gbps=400,
        reach_km=2.0,
        modulation=ModulationFormat.PAM4
    )
    
    metrics = link.performance_metrics()
    print(f"   Data Rate: {metrics['data_rate_gbps']} Gbps")
    print(f"   Vπ: {metrics['v_pi_volts']:.2f} V")
    print(f"   Bandwidth: {metrics['bandwidth_ghz']:.1f} GHz")
    print(f"   Power: {metrics['power_watts']:.2f} W")
    print(f"   Energy/Bit: {metrics['energy_per_bit_pj']:.2f} pJ")
    print(f"   Link Margin: {metrics['link_budget']['link_margin_db']:.2f} dB")
    
    # 4. 800G PAM8 Link
    print("\n4. Advanced 800G TFLN Link (PAM8)")
    link_800g = TFLNPhotonicLink(
        data_rate_gbps=800,
        reach_km=0.5,
        modulation=ModulationFormat.PAM8
    )
    
    metrics_800g = link_800g.performance_metrics()
    print(f"   Data Rate: {metrics_800g['data_rate_gbps']} Gbps")
    print(f"   Power: {metrics_800g['power_watts']:.2f} W")
    print(f"   Energy/Bit: {metrics_800g['energy_per_bit_pj']:.2f} pJ")
    
    print("\n" + "=" * 70)
    print("TFLN ADVANTAGES:")
    print("  • Ultra-low Vπ (<2V) - 3x better than silicon")
    print("  • High bandwidth (>100 GHz) - Native 400G-800G")
    print("  • Low power (<1W per 400G) - 5x more efficient")
    print("  • Linear modulation - Perfect PAM4/PAM8 eyes")
    print("  • Thermal stability - No active cooling needed")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate_tfln_components()
