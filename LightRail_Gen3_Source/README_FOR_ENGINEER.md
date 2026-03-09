# LightRail Gen3 TFLN NIC — Engineer README

## How to Open These Files

1. **Install KiCad 7.0+** from https://kicad.org  
2. Open `LightRail_Gen3.kicad_pro` in KiCad's Project Manager  
3. Click **Schematic Editor** to open `LightRail_Gen3.kicad_sch`  
4. Click **PCB Editor** to open `LightRail_Gen3.kicad_pcb`  

## Stackup Summary (15 Layers)

| Layer | Name | Role |
|-------|------|------|
| 1 | F.Cu | Top Signal |
| 2 | In1.Cu | GND Plane |
| 3 | In2.Cu | 3V3 Power Plane |
| 4-12 | In3–In11.Cu | Signal/RF Routing |
| 13 | In12.Cu | General Routing |
| 14 | In13.Cu | GND Return Plane |
| 15 | In14.Cu | 1V8 Core Power |
| 16 | B.Cu | Bottom Signal |

Material: **ISOLA 370HR** (High-Tg FR4, εr=4.1, tan δ=0.016)  
Total Thickness: **2.0 mm**  

## Key Impedances

| Net | Target | Layer | Style |
|-----|--------|-------|-------|
| RF TX PAM4 | 50 Ω | In3/In4.Cu | Microstrip |
| PCIe Gen5 | 85 Ω | F.Cu | Differential pair |
| RX Optical | 85 Ω | In5.Cu | Differential pair |
| I2C/SPI | unterminated | B.Cu | Any |

## Simulation Notes

For LVS verification use **NetGen**, parasitic extraction via **Magic**,  
and final simulation in **NGSPICE** as recommended by the engineering team.
