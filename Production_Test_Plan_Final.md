# Production Test Plan: LightRail AI Pluggable Interconnect

## Step 1: Impedance & Rail Check (Unpowered)
- **Measure Resistance to GND on 3.3V_Rail**: Target > 1kΩ.
- **Measure Resistance to GND on 1.8V_LDO**: Target > 500Ω.
- **Fail Condition**: Short circuit (< 10Ω) indicates reflow bridge under SerDes BGA (U9).

## Step 2: Optical Power Up (Phase 3)
1. Enable Laser Driver (U5) via I2C interface.
2. Set Laser Current (I_bias) to 50mA.
3. **Verification**: Optical Power Meter at J2 (Output Fiber) must read > 5 dBm.
4. **Note**: If power < 0 dBm, fiber coupling (OPT1) alignment has drifted.

## Step 3: Neuron Diagnostic (Phase 4)
- **Execution**: Run `photonic_ai_control.py`.
- **Input**: Sweep Phase Shifter Voltage (V_ps) from 0.5V to 3.0V.
- **Output**: Verify PAM4 eye diagram on SMA connectors (J4-J7).
- **Spec**: Matches "Symmetric Eye" profile with Vπ ≈ 1.8V.

## Step 4: System Integration Test
- **PCIe Recognition**: Verify card is detected as "LightRail AI CPO Interconnect" (Vendor ID: 0xLR15).
- **Throughput Test**: Run 8x 400G loopback test. Target 3.2 Tbps aggregate.
