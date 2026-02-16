# 🚀 LIGHTRAIL AI - PRODUCTION TEST PLAN
## TFLN Photonic Intelligence Interconnect (15-Layer)

**Manufacturing Partner**: Seeed Fusion PCBA Service  
**Project**: LightRail AI - Generation 3 TFLN Modulator  
**Date**: February 10, 2026

---

### 1. Hardware Context & Test Points
This board utilizes a **15-layer Rogers RO4350B** stackup with 2,095 components. High-value ICs must be verified for correct placement and soldering integrity before final packaging.

#### Critical Rail Impedance Check (Unpowered)
Before applying power, measure resistance to GND on the following rails:
- **12V Input (J1/Power Pin)**: >10 kΩ
- **3.3V Rail (U7 Output)**: >500 Ω
- **1.8V Rail (U6 Output)**: >200 Ω

---

### 2. Functional Testing Phases

#### Phase 1: Power Sequencing (Powered)
Apply **12V DC (max 2A limit)** to the power input.
1. **Verify Buck Converter (U7)**: Measure **3.3V ± 2%** at `TP_3V3`.
2. **Verify LDO (U6)**: Measure **1.8V ± 1%** at `TP_1V8`.
3. **Verify Reference (U2/U5)**: Measure **2.5V ± 5%** at `TP_LASER_VCC`.

#### Phase 2: Communication & Digital Diagnostic
Connect the **FT2232H USB interface (J1/Edge)** to a test PC. Correct enumeration confirms FTDI soldering.
1. **I2C Enumeration**: Scan I2C bus via FTDI Interface B.  
   - Expect **Si5395A (U10)** at address `0x6B`.
2. **SPI Loopback / DAC Init**: Send SPI command to **AD5684 (U11, U12)**.
   - Command: `0x000F0FFF` (Write all channels to Full Scale).
   - Verify: Measure **3.25V - 3.3V** on Phase Shifter bias lines.

#### Phase 3: Photonic Control Subsystem
1. **TEC Stabilization (U8/MPT5000)**: Initialize TEC controller via I2C.  
   - Setpoint: 25°C. 
   - Observe: Monitor `TEC_ILIMIT` pin. Current should ramp then stabilize. Status LED `D1` should turn ON (Temp Locked).
2. **Laser Threshold Check**: Enable **DFB Laser (U2)** via **MAX3669 (U5)**.
   - Sweep bias current to 50mA.
   - Verify: Optical Power Meter at `J2 (LC/APC)` should read **>5dBm**.

#### Phase 4: Neuron Intelligence Diagnostic
Verify the 8-Neuron spiking logic through a threshold sweep.
1. **Threshold Sweep**: Use `photonic_ai_control.py` to sweep the Phase Shifter voltage on **Neuron 0-7**.
   - Input: 0.5V to 3.0V.
   - Output: Verify SPI responses from the comparator stage match the DAC setting.

---

### 3. Production Pass/Fail Checklist
| Step | ID | Requirement | Result |
|---|---|---|---|
| 1.1 | P1 | 3.3V Rail is 3.3V ±0.06V | [ ] Pass |
| 1.2 | P2 | 1.8V Rail is 1.8V ±0.02V | [ ] Pass |
| 2.1 | D1 | Si5395A I2C Ack @ 0x6B | [ ] Pass |
| 2.2 | D2 | Phase Shifter Bias (DAC) = 3.3V | [ ] Pass |
| 3.1 | T1 | TEC Locked (D1 Green) | [ ] Pass |
| 3.2 | L1 | Laser Emission >5dBm | [ ] Pass |
| 4.1 | N1 | 8-Neuron Control Path Verified | [ ] Pass |

**NOTE**: If any test in Phase 1 or 2 fails, STOP immediately to prevent damage to **U1 (TFLN Modulator, $12,500 replacement cost)**.

---

### 4. Technical Support
For questions regarding the `photonic_ai_control.py` script or custom test jigs, contact **LightRail AI Engineering**.
