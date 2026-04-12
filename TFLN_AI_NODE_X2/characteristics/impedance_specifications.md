# Impedance Control Specifications

## Controlled Impedance Requirements

All impedance values must be controlled to +/- 10% unless otherwise noted.

### Single-Ended Traces
| Net Class | Z0 (ohm) | Width (mm) | Layer | Reference Plane |
|-----------|----------|------------|-------|-----------------|
| Default | 50 | 0.20 | Any signal | Adjacent GND |
| DDR5_DQ | 40 | 0.10 | L6/L16 | Adjacent GND |

### Differential Pairs
| Net Class | Zdiff (ohm) | Width (mm) | Gap (mm) | Layer | Reference |
|-----------|-------------|------------|----------|-------|-----------|
| PCIe_Gen6 | 85 | 0.12 | 0.18 | L4 | L5 GND |
| DDR5_DQ | 80 | 0.10 | 0.15 | L6/L16 | Adjacent GND |
| TFLN_RF | 100 | 0.15 | 0.25 | L1 | L2 GND |

### Via Impedance (Back-Drill Required)
| Via Type | Z0 (ohm) | Drill (mm) | Pad (mm) | Anti-pad (mm) | Stub Max |
|----------|----------|------------|----------|---------------|----------|
| PCIe Signal | 85 | 0.25 | 0.50 | 0.80 | 5 mil |
| DDR5 Signal | 80 | 0.25 | 0.50 | 0.80 | 8 mil |
| TFLN RF | 100 | 0.25 | 0.50 | 1.00 | NOT USED |

## Test Coupon Requirements

### Coupon Structures (3 per panel)
1. Single-ended 50 ohm microstrip (L1 ref L2)
2. Single-ended 50 ohm stripline (L4 ref L3/L5)
3. Differential 85 ohm edge-coupled stripline (L4 ref L3/L5)
4. Differential 100 ohm microstrip (L1 ref L2)
5. Differential 80 ohm stripline (L6 ref L5/L7)

### Measurement Method
- TDR (Time Domain Reflectometry)
- Equipment: 20 GHz TDR with <20 ps rise time
- Probe: Differential, 200 um pitch

## Length Matching Requirements

| Signal Group | Max Skew (mm) | Constraint |
|--------------|---------------|------------|
| TFLN_RF P/N pair | 0.05 | Within each pair |
| PCIe_Gen6 P/N pair | 0.10 | Within each pair |
| PCIe_Gen6 lane-to-lane | 2.0 | Within x16 link |
| DDR5_DQ byte lane | 2.5 | Within 8-bit group |
| DDR5_DQ to DQS | 0.5 | Data to strobe |
| DDR5_CA group | 5.0 | Address/command |
| DDR5_CK | 0.25 | Clock pair match |
