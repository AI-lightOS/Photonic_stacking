# LIGHTRAILAI PRODUCTION TEST PLAN

**Device**: LightRailAI CPO NIC (15nd Layer Hybrid Stack)
**Objective**: Post-Fab Validation and Neural Diagnostic

---

### Step 1: Impedance & Rail Check (Unpowered)
*Goal: Ensure no solder bridges or shorts on critical high-speed rails.*

*   **3.3V_Rail (Main Power)**: Measure resistance to GND. 
    *   Target: **>1kΩ**
*   **1.8V_LDO (LDO Output)**: Measure resistance to GND.
    *   Target: **>500Ω**
*   **Fail Condition**: Short circuit (<10Ω) indicates reflow bridge under the SerDes BGA (U9).

---

### Step 2: Optical Power Up
*Goal: Verify optical source and fiber coupling integrity.*

1.  Enable Laser Driver (U5) via I2C interface.
2.  Set Laser Current to **50mA**.
3.  **Verification**: 
    *   Connect Optical Power Meter at J2 (Output Fiber).
    *   Target: **>5 dBm**
    *   Note: If power <0 dBm, the fiber coupling (OPT1) alignment has drifted.

---

### Step 3: Neuron Diagnostic
*Goal: Verify photonic compute path and PAM4 eye symmetry.*

1.  Run script: `python photonic_ai_control.py`
2.  **Input**: Sweep Phase Shifter Voltage from **0.5V to 3.0V**.
3.  **Output**:
    *   Verify PAM4 eye diagram on SMA connectors (J4-J7).
    *   Check for "Symmetric Eye" spec: **Vπ ≈ 1.8V**.
    *   Verify threshold response matches neuron sensitivity curve.

---

### Pass/Fail Summary
| Test Phase | Metric | Status |
|---|---|---|
| Step 1 | 3.3V >1kΩ, 1.8V >500Ω | [ ] Pass / [ ] Fail |
| Step 2 | Optical Out > 5 dBm | [ ] Pass / [ ] Fail |
| Step 3 | PAM4 Eye Open (Vπ ≈ 1.8V) | [ ] Pass / [ ] Fail |

---
**Engineering Support**: Refer to `lightrailai_config.py` for design constants.
