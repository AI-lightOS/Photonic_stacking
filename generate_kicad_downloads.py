# LightRail AI Gen3 TFLN NIC - Valid KiCad 7 Project Generator
# Outputs to the user Downloads directory

import os, shutil, zipfile, json, uuid

DOWNLOADS = os.path.join(os.path.expanduser("~"), "Downloads")
OUT_DIR   = os.path.join(DOWNLOADS, "LightRail_Gen3_KiCad")
ZIP_NAME  = os.path.join(DOWNLOADS, "LightRail_Gen3_Native_Source.zip")

BOARD_W, BOARD_H = 167.65, 111.15  # PCIe FHHL mm

def uid():
    return str(uuid.uuid4())

# ═══════════════════════════════════════════════════════════
# SCHEMATIC
# ═══════════════════════════════════════════════════════════
def sym_def(val):
    return f"""\
    (symbol "{val}"
      (pin_names (offset 1.016))
      (property "Reference" "U" (at 0 8 0) (effects (font (size 1.27 1.27))))
      (property "Value" "{val}" (at 0 -8 0) (effects (font (size 1.27 1.27))))
      (symbol "{val}_0_1"
        (rectangle (start -12 -6) (end 12 6)
          (stroke (width 0.254) (type default)) (fill (type background))))
      (symbol "{val}_1_1"
        (pin input line (at -14 2 0) (length 2)
          (name "IN" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27)))))
        (pin output line (at 14 2 180) (length 2)
          (name "OUT" (effects (font (size 1.27 1.27))))
          (number "2" (effects (font (size 1.27 1.27)))))
        (pin power_in line (at 0 -8 90) (length 2)
          (name "GND" (effects (font (size 1.27 1.27))))
          (number "3" (effects (font (size 1.27 1.27)))))
        (pin power_in line (at 0 8 270) (length 2)
          (name "VCC" (effects (font (size 1.27 1.27))))
          (number "4" (effects (font (size 1.27 1.27)))))
      )
    )"""

COMPS = [
    # ref,  value,                           x_sch, y_sch    description
    ("J1",  "PCIe_Gen5_x16_Edge_Connector",  20,    60),
    ("U1",  "LightRail_AI_Core_ASIC",        70,    60),
    ("U2",  "TLN1550_DFB_Laser",            130,    60),
    ("U3",  "XPDV4120R_Photodetector",      130,    90),
    ("U4",  "HMC8410_RF_Driver",             70,    30),
    ("U5",  "MAX3669_Laser_Driver",          70,    90),
    ("U6",  "TPS7A4700_LDO",               130,   120),
    ("U7",  "LT8614_Buck_Converter",         20,   120),
    ("U8",  "MPT5000_TEC_Driver",           130,   150),
    ("U9",  "BCM84881_SerDes",               20,    30),
    ("U10", "Si5395A_Clock_Generator",       70,   150),
    ("U11", "TFLN_MZM_400G_Modulator",      130,    30),
]

POWER_SYMS = [
    ("power:+12V", "+12V", "#PWR01", 20,  108),
    ("power:+3V3", "+3V3", "#PWR02", 70,  108),
    ("power:+1V8", "+1V8", "#PWR03", 130, 108),
    ("power:GND",  "GND",  "#PWR04", 20,   72),
    ("power:GND",  "GND",  "#PWR05", 70,   72),
    ("power:GND",  "GND",  "#PWR06", 130,  72),
]

POWER_LIB = """\
    (symbol "power:GND"
      (power)
      (property "Reference" "#PWR" (at 0 -6.35 0) (effects (font (size 1.27 1.27)) hide))
      (property "Value" "GND" (at 0 -3.81 0) (effects (font (size 1.27 1.27))))
      (symbol "GND_0_1"
        (polyline (pts (xy 0 0) (xy 0 -1.27) (xy 1.27 -1.27) (xy 0 -2.54) (xy -1.27 -1.27) (xy 0 -1.27))
          (stroke (width 0) (type default)) (fill (type outline))))
      (symbol "GND_1_1"
        (pin power_in line (at 0 0 270) (length 0) hide
          (name "GND" (effects (font (size 1.27 1.27))))
          (number "1"  (effects (font (size 1.27 1.27)))))))
    (symbol "power:+12V"
      (power)
      (property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) hide))
      (property "Value" "+12V" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
      (symbol "+12V_0_1"
        (polyline (pts (xy -0.762 1.27) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 0 0) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 0 2.54) (xy 0.762 1.27)) (stroke (width 0) (type default)) (fill (type none))))
      (symbol "+12V_1_1"
        (pin power_in line (at 0 0 270) (length 0) hide
          (name "+12V" (effects (font (size 1.27 1.27))))
          (number "1"   (effects (font (size 1.27 1.27)))))))
    (symbol "power:+3V3"
      (power)
      (property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) hide))
      (property "Value" "+3V3" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
      (symbol "+3V3_0_1"
        (polyline (pts (xy -0.762 1.27) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 0 0) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 0 2.54) (xy 0.762 1.27)) (stroke (width 0) (type default)) (fill (type none))))
      (symbol "+3V3_1_1"
        (pin power_in line (at 0 0 270) (length 0) hide
          (name "+3V3" (effects (font (size 1.27 1.27))))
          (number "1"   (effects (font (size 1.27 1.27)))))))
    (symbol "power:+1V8"
      (power)
      (property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) hide))
      (property "Value" "+1V8" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
      (symbol "+1V8_0_1"
        (polyline (pts (xy -0.762 1.27) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 0 0) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 0 2.54) (xy 0.762 1.27)) (stroke (width 0) (type default)) (fill (type none))))
      (symbol "+1V8_1_1"
        (pin power_in line (at 0 0 270) (length 0) hide
          (name "+1V8" (effects (font (size 1.27 1.27))))
          (number "1"   (effects (font (size 1.27 1.27)))))))\n"""

def build_schematic():
    prj = "LightRail_Gen3"
    lib_block = "  (lib_symbols\n" + POWER_LIB
    seen = set()
    for ref, val, x, y in COMPS:
        if val not in seen:
            lib_block += sym_def(val) + "\n"
            seen.add(val)
    lib_block += "  )"

    syms = ""
    for ref, val, x, y in COMPS:
        syms += f"""\
  (symbol (lib_id "{val}") (at {x} {y} 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced)
    (property "Reference" "{ref}" (at {x} {y-9} 0)
      (effects (font (size 1.27 1.27))))
    (property "Value" "{val}" (at {x} {y+9} 0)
      (effects (font (size 1.27 1.27))))
    (property "Footprint" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide))
    (instances
      (project "{prj}"
        (path "/{uid()}"
          (reference "{ref}") (unit 1))))
  )
"""

    pwr = ""
    for lib, val, ref, x, y in POWER_SYMS:
        pwr += f"""\
  (symbol (lib_id "{lib}") (at {x} {y} 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (property "Reference" "{ref}" (at {x} {y-3} 0)
      (effects (font (size 1.27 1.27)) hide))
    (property "Value" "{val}" (at {x} {y+2} 0)
      (effects (font (size 1.27 1.27))))
    (instances (project "{prj}"
      (path "/{uid()}" (reference "{ref}") (unit 1))))
  )
"""

    def wire(x1,y1,x2,y2):
        return f'  (wire (pts (xy {x1} {y1}) (xy {x2} {y2})) (stroke (width 0.254) (type default)) (uuid "{uid()}"))'
    wires = "\n".join([
        wire(20,60,70,60),    # PCIe -> Core
        wire(70,60,130,60),   # Core -> Laser
        wire(20,120,70,120),  # Buck -> LDO
        wire(70,120,130,120), # LDO out
        wire(70,60,70,30),    # Core -> RF Driver
        wire(70,30,130,30),   # RF Driver -> MZM
        wire(20,30,70,30),    # SerDes -> RF Driver
        wire(130,90,70,60),   # Detector -> Core (RX) 
        wire(70,60,70,90),    # Core -> Laser Driver
        wire(70,90,130,90),   # Laser Driver -> DFB
    ])

    def glabel(text, x, y, shape="output"):
        return f'  (global_label "{text}" (shape {shape}) (at {x} {y} 0) (fields_autoplaced) (effects (font (size 1.27 1.27))) (uuid "{uid()}"))'

    labels = "\n".join([
        glabel("+12V_INPUT",       16, 108, "input"),
        glabel("+3V3_MAIN",        20, 108, "output"),
        glabel("+1V8_CLEAN",       70, 108, "output"),
        glabel("PCIE_GEN5_x16",    20,  60, "bidirectional"),
        glabel("RF_TX_50R_CH0_7",  70,  30, "output"),
        glabel("PCIE_RX_85R_DIFF", 20,  30, "bidirectional"),
        glabel("LASER_CW_DRIVE",   70,  90, "output"),
        glabel("TEC_CTRL_LOOP",   130, 150, "bidirectional"),
        glabel("I2C_MGMT_BUS",     70, 150, "bidirectional"),
        glabel("SPI_DAC_BIAS",     70,  60, "bidirectional"),
    ])

    def txt(t, x, y):
        return f'  (text "{t}" (at {x} {y} 0) (effects (font (size 1.778 1.778) (thickness 0.333))))'

    texts = "\n".join([
        txt("LightRail AI Gen3 TFLN NIC — System Schematic", 5, 5),
        txt("PCIe Gen5 x16 FHHL | 15-Layer Rogers RO4350B + ISOLA 370HR", 5, 9),
        txt("100 Gbaud PAM4 | 85-Ohm diff PCIe | 50-Ohm SE RF", 5, 13),
        txt("POWER SECTION", 5, 100),
        txt("LT8614: +12V -> +3V3  |  TPS7A4700 LDO: +3V3 -> +1V8", 5, 104),
        txt("OPTICAL PATH", 100, 20),
        txt("HMC8410 RF Drv -> TFLN MZM (50-Ohm SE)", 100, 24),
        txt("MAX3669 Laser Drv -> TLN1550 DFB + MPT5000 TEC", 100, 28),
        txt("RECEIVE PATH", 100, 80),
        txt("XPDV4120R Photodetector -> AI Core (85-Ohm diff)", 100, 84),
        txt("HOST INTERFACE", 5, 20),
        txt("PCIe Gen5 x16 -> BCM84881 SerDes -> AI Core", 5, 24),
    ])

    return f"""\
(kicad_sch
  (version 20230121)
  (generator "eeschema")
  (uuid "{uid()}")
  (paper "A0")
  (title_block
    (title "LightRail AI Gen3 TFLN NIC")
    (date "2026-03-08")
    (rev "1.0")
    (company "LightRail Computing")
    (comment 1 "PCIe Gen5 x16 Full-Height Half-Length  167.65x111.15mm")
    (comment 2 "15-Layer: Rogers RO4350B RF + ISOLA 370HR Digital/Power")
    (comment 3 "TFLN MZM 400G | BCM84881 SerDes | LightRail AI Core ASIC")
    (comment 4 "85-Ohm diff PAM4 | 50-Ohm SE RF modulator drive lines")
  )

{lib_block}

{syms}
{pwr}
{wires}
{labels}
{texts}
)
"""

# ═══════════════════════════════════════════════════════════
# PCB
# ═══════════════════════════════════════════════════════════
def build_pcb():
    w, h = BOARD_W, BOARD_H

    layers = """\
  (layers
    (0  "F.Cu"    signal  "Top RF Signal")
    (1  "In1.Cu"  power   "GND Plane")
    (2  "In2.Cu"  power   "3V3 Power Plane")
    (3  "In3.Cu"  signal  "RF Signal 50-Ohm SE")
    (4  "In4.Cu"  signal  "RF Signal 85-Ohm Diff")
    (5  "In5.Cu"  signal  "High-Speed Digital 1")
    (6  "In6.Cu"  signal  "High-Speed Digital 2")
    (7  "In7.Cu"  signal  "Optical Control 1")
    (8  "In8.Cu"  signal  "Optical Control 2")
    (9  "In9.Cu"  signal  "SerDes Ref 1")
    (10 "In10.Cu" signal  "SerDes Ref 2")
    (11 "In11.Cu" signal  "Clock Distribution")
    (12 "In12.Cu" signal  "General Routing")
    (13 "In13.Cu" power   "GND Return Plane")
    (14 "In14.Cu" power   "1V8 Core Power")
    (31 "B.Cu"    signal  "Bottom Signal")
    (34 "B.Paste" user "B.Paste")
    (35 "F.Paste" user "F.Paste")
    (36 "B.SilkS" user "B.SilkS")
    (37 "F.SilkS" user "F.SilkS")
    (38 "B.Mask"  user "B.Mask")
    (39 "F.Mask"  user "F.Mask")
    (44 "Edge.Cuts" user "Edge.Cuts")
    (47 "F.CrtYd"  user "F.CrtYd")
    (49 "F.Fab"    user "F.Fab")
  )"""

    stackup = """\
  (setup
    (stackup
      (layer "F.Cu"    (type "copper") (thickness 0.035))
      (layer "dielectric 1"  (type "prepreg") (thickness 0.085) (material "Rogers RO4350B") (epsilon_r 3.66) (loss_tangent 0.004))
      (layer "In1.Cu"  (type "copper") (thickness 0.035))
      (layer "dielectric 2"  (type "core")   (thickness 0.127) (material "Rogers RO4350B") (epsilon_r 3.66) (loss_tangent 0.004))
      (layer "In2.Cu"  (type "copper") (thickness 0.035))
      (layer "dielectric 3"  (type "prepreg") (thickness 0.085) (material "Rogers RO4350B") (epsilon_r 3.66) (loss_tangent 0.004))
      (layer "In3.Cu"  (type "copper") (thickness 0.035))
      (layer "dielectric 4"  (type "core")   (thickness 0.2) (material "ISOLA 370HR") (epsilon_r 4.1) (loss_tangent 0.016))
      (layer "In4.Cu"  (type "copper") (thickness 0.035))
      (layer "dielectric 5"  (type "core")   (thickness 0.2) (material "ISOLA 370HR") (epsilon_r 4.1) (loss_tangent 0.016))
      (layer "In5.Cu"  (type "copper") (thickness 0.035))
      (layer "dielectric 6"  (type "core")   (thickness 0.2) (material "ISOLA 370HR") (epsilon_r 4.1) (loss_tangent 0.016))
      (layer "In6.Cu"  (type "copper") (thickness 0.035))
      (layer "dielectric 7"  (type "core")   (thickness 0.2) (material "ISOLA 370HR") (epsilon_r 4.1) (loss_tangent 0.016))
      (layer "In7.Cu"  (type "copper") (thickness 0.035))
      (layer "dielectric 8"  (type "core")   (thickness 0.2) (material "ISOLA 370HR") (epsilon_r 4.1) (loss_tangent 0.016))
      (layer "In8.Cu"  (type "copper") (thickness 0.035))
      (layer "dielectric 9"  (type "core")   (thickness 0.2) (material "ISOLA 370HR") (epsilon_r 4.1) (loss_tangent 0.016))
      (layer "In9.Cu"  (type "copper") (thickness 0.035))
      (layer "dielectric 10" (type "core")   (thickness 0.2) (material "ISOLA 370HR") (epsilon_r 4.1) (loss_tangent 0.016))
      (layer "In10.Cu" (type "copper") (thickness 0.035))
      (layer "dielectric 11" (type "core")   (thickness 0.2) (material "ISOLA 370HR") (epsilon_r 4.1) (loss_tangent 0.016))
      (layer "In11.Cu" (type "copper") (thickness 0.035))
      (layer "dielectric 12" (type "core")   (thickness 0.15) (material "ISOLA 370HR") (epsilon_r 4.1) (loss_tangent 0.016))
      (layer "In12.Cu" (type "copper") (thickness 0.035))
      (layer "dielectric 13" (type "core")   (thickness 0.15) (material "ISOLA 370HR") (epsilon_r 4.1) (loss_tangent 0.016))
      (layer "In13.Cu" (type "copper") (thickness 0.035))
      (layer "dielectric 14" (type "prepreg") (thickness 0.085) (material "Rogers RO4350B") (epsilon_r 3.66) (loss_tangent 0.004))
      (layer "In14.Cu" (type "copper") (thickness 0.035))
      (layer "dielectric 15" (type "prepreg") (thickness 0.085) (material "Rogers RO4350B") (epsilon_r 3.66) (loss_tangent 0.004))
      (layer "B.Cu"    (type "copper") (thickness 0.035))
    )
    (pad_to_mask_clearance 0.05)
    (allow_soldermask_bridges_in_footprints no)
    (grid_origin 0 0)
  )"""

    nets = "\n".join([
        '  (net 0 "")',
        '  (net 1 "+12V_INPUT")',
        '  (net 2 "+3V3_MAIN")',
        '  (net 3 "+1V8_CLEAN_ANALOG")',
        '  (net 4 "GND_REFERENCE")',
        '  (net 5 "RF_TX_PAM4_CH0P")',
        '  (net 6 "RF_TX_PAM4_CH0N")',
        '  (net 7 "PCIE_RX_P0")',
        '  (net 8 "PCIE_RX_N0")',
        '  (net 9 "LASER_DRIVE_CW")',
        '  (net 10 "I2C_SCL")',
        '  (net 11 "I2C_SDA")',
        '  (net 12 "SPI_MOSI")',
    ])

    # LightRail AI Core footprint (20x20 BGA, 1mm pitch)
    bga_cx, bga_cy = 83.82, 55.575
    bga_pads = []
    idx = 1
    net_map = [5,6,7,8,4,5,6,4,9,10,11,12,4,5,6,4,7,8,5,6]
    net_names = ["+12V_INPUT","+3V3_MAIN","+1V8_CLEAN_ANALOG","GND_REFERENCE",
                 "RF_TX_PAM4_CH0P","RF_TX_PAM4_CH0N","PCIE_RX_P0","PCIE_RX_N0",
                 "LASER_DRIVE_CW","I2C_SCL","I2C_SDA","SPI_MOSI",
                 "GND_REFERENCE","RF_TX_PAM4_CH0P","RF_TX_PAM4_CH0N","GND_REFERENCE",
                 "PCIE_RX_P0","PCIE_RX_N0","RF_TX_PAM4_CH0P","RF_TX_PAM4_CH0N"]
    for r in range(20):
        for c in range(20):
            px = -9.5 + c * 1.0
            py = -9.5 + r * 1.0
            ni = idx % len(net_map)
            net_id = net_map[ni]
            net_name = net_names[ni]
            bga_pads.append(f'    (pad "{idx}" smd circle (at {px:.1f} {py:.1f}) (size 0.5 0.5) (layers "F.Cu" "F.Paste" "F.Mask") (net {net_id} "{net_name}"))')
            idx += 1
    bga_fp = f"""\
  (footprint "LightRail:AI_Core_BGA_20x20" (layer "F.Cu") (at {bga_cx} {bga_cy} 0)
    (property "Reference" "U1" (at 0 -12 0) (layer "F.SilkS") (effects (font (size 2 2))))
    (property "Value" "LightRail_AI_Core_ASIC" (at 0 12 0) (layer "F.Fab") (effects (font (size 2 2))))
{chr(10).join(bga_pads)}
    (fp_rect (start -11 -11) (end 11 11) (layer "F.CrtYd") (width 0.05))
    (fp_rect (start -10 -10) (end 10 10) (layer "F.SilkS") (width 0.15))
  )"""

    # TFLN MZM die footprint
    def mzm_fp(cx, cy, ref, net_p, net_n):
        pads = "\n".join([
            f'    (pad "1" smd rect (at -3 0) (size 0.3 1.5) (layers "F.Cu" "F.Paste" "F.Mask") (net 5 "RF_TX_PAM4_CH0P"))',
            f'    (pad "2" smd rect (at -1 0) (size 0.3 1.5) (layers "F.Cu" "F.Paste" "F.Mask") (net 4 "GND_REFERENCE"))',
            f'    (pad "3" smd rect (at  1 0) (size 0.3 1.5) (layers "F.Cu" "F.Paste" "F.Mask") (net 6 "RF_TX_PAM4_CH0N"))',
            f'    (pad "4" smd rect (at  3 0) (size 0.3 1.5) (layers "F.Cu" "F.Paste" "F.Mask") (net 12 "SPI_MOSI"))',
        ])
        return f"""\
  (footprint "LightRail:TFLN_MZM_Die" (layer "F.Cu") (at {cx} {cy} 0)
    (property "Reference" "{ref}" (at 0 -6 0) (layer "F.SilkS") (effects (font (size 1.5 1.5))))
    (property "Value" "TFLN_MZM_400G" (at 0 6 0) (layer "F.Fab") (effects (font (size 1.5 1.5))))
{pads}
    (fp_rect (start -5 -3) (end 5 3) (layer "F.CrtYd") (width 0.05))
    (fp_rect (start -4 -2) (end 4 2) (layer "F.SilkS") (width 0.12))
  )"""

    # PCIe SerDes (QFP)
    serdes_pads = "\n".join([
        f'    (pad "{i+1}" smd rect (at {-15 + i*2.0} -8) (size 0.7 1.5) (layers "F.Cu" "F.Paste" "F.Mask") (net {7 if i%2==0 else 8} "{"PCIE_RX_P0" if i%2==0 else "PCIE_RX_N0"}"))'
        for i in range(16)
    ])
    serdes_fp = f"""\
  (footprint "Package_QFP:QFP-64" (layer "F.Cu") (at 30 55.575 0)
    (property "Reference" "U9" (at 0 -12 0) (layer "F.SilkS") (effects (font (size 1.5 1.5))))
    (property "Value" "BCM84881_SerDes" (at 0 12 0) (layer "F.Fab") (effects (font (size 1.5 1.5))))
{serdes_pads}
    (fp_rect (start -10 -10) (end 10 10) (layer "F.CrtYd") (width 0.05))
    (fp_rect (start -8 -8)   (end 8 8)   (layer "F.SilkS") (width 0.12))
  )"""

    # Board outline (Edge.Cuts)
    outline = f"""\
  (gr_line (start 0 0) (end {w} 0) (layer "Edge.Cuts") (width 0.15))
  (gr_line (start {w} 0) (end {w} {h}) (layer "Edge.Cuts") (width 0.15))
  (gr_line (start {w} {h}) (end 0 {h}) (layer "Edge.Cuts") (width 0.15))
  (gr_line (start 0 {h}) (end 0 0) (layer "Edge.Cuts") (width 0.15))"""

    # Mounting holes
    mholes = "\n".join([
        f'  (footprint "MountingHole:MountingHole_3.2_M3" (layer "F.Cu") (at {mx} {my} 0)\n    (property "Reference" "H{i+1}" (at 0 0 0) (layer "F.SilkS") (effects (font (size 1 1)) hide))\n    (pad "" np_thru_hole circle (at 0 0) (size 3.2 3.2) (drill 3.2) (layers "*.Cu" "*.Mask"))\n  )'
        for i, (mx, my) in enumerate([(3.5, 3.5), (w-3.5, 3.5), (3.5, h-3.5), (w-3.5, h-3.5)])
    ])

    # 85-Ohm differential pairs (PCIe) on F.Cu — 16 pairs
    diff_pairs = ""
    for i in range(16):
        yp = 30 + i * 3.5
        yn = yp + 0.85
        diff_pairs += f'\n  (segment (start 5 {yp:.2f}) (end {w - 5:.2f} {yp:.2f}) (width 0.127) (layer "F.Cu") (net 7))'
        diff_pairs += f'\n  (segment (start 5 {yn:.2f}) (end {w - 5:.2f} {yn:.2f}) (width 0.127) (layer "F.Cu") (net 8))'

    # 50-Ohm SE RF traces on In3.Cu — 8 channels
    rf_traces = ""
    for i in range(8):
        yrf = 30 + i * 5.0
        rf_traces += f'\n  (segment (start {bga_cx + 10:.2f} {yrf:.2f}) (end {bga_cx + 60:.2f} {yrf:.2f}) (width 0.172) (layer "In3.Cu") (net 5))'

    # GND via stitching grid
    vias = ""
    for vi in range(15):
        for vj in range(10):
            vx = 12 + vi * 10.0
            vy = 12 + vj * 9.0
            vias += f'\n  (via (at {vx:.1f} {vy:.1f}) (size 0.6) (drill 0.3) (layers "F.Cu" "B.Cu") (net 4))'

    # Title
    title = f'  (gr_text "LightRail AI Gen3 TFLN NIC | PCIe Gen5 x16 | 15-Layer RO4350B+FR4" (at {w/2:.2f} 4 0) (layer "F.SilkS") (effects (font (size 2 2) (thickness 0.4))))'

    return f"""\
(kicad_pcb
  (version 20221018)
  (generator "pcbnew")
  (general
    (thickness 2.0)
    (legacy_teardrops no)
  )
  (paper "A0")
  (title_block
    (title "LightRail AI Gen3 TFLN NIC")
    (date "2026-03-08")
    (rev "1.0")
    (company "LightRail Computing")
    (comment 1 "PCIe Gen5 x16 Full-Height Half-Length 167.65x111.15mm")
    (comment 2 "Layers 1-4: Rogers RO4350B | Layers 5-15: ISOLA 370HR")
  )
{layers}
{stackup}
{nets}
{outline}
{title}
{mholes}
{bga_fp}
{mzm_fp(130, 30, "U11", 5, 6)}
{mzm_fp(145, 30, "U12", 5, 6)}
{serdes_fp}
{diff_pairs}
{rf_traces}
{vias}
)
"""

# ═══════════════════════════════════════════════════════════
# PROJECT
# ═══════════════════════════════════════════════════════════
def build_project():
    return json.dumps({
        "meta": {"version": 1, "filename": "LightRail_Gen3.kicad_pro"},
        "board": {
            "design_settings": {
                "defaults": {"track_width": 0.25, "via_size": 0.6, "via_drill": 0.3,
                             "diff_pair_width": 0.127, "diff_pair_gap": 0.127},
                "rules": {"min_track_width": 0.075, "min_via_drill": 0.15}
            }
        },
        "net_settings": {
            "classes": [
                {"name": "Default", "clearance": 0.2, "track_width": 0.25,
                 "via_size": 0.6, "via_drill": 0.3},
                {"name": "RF_50R_SE", "clearance": 0.15, "track_width": 0.172,
                 "via_size": 0.5, "via_drill": 0.25},
                {"name": "PCIE_85R_DIFF", "clearance": 0.15, "track_width": 0.127,
                 "via_size": 0.5, "via_drill": 0.25, "diff_pair_width": 0.127,
                 "diff_pair_gap": 0.127}
            ]
        },
        "schematic": {"annotate_start_num": 0},
        "libraries": {"pinned_symbol_libs": [], "pinned_footprint_libs": []}
    }, indent=2)

README = """\
# LightRail AI Gen3 TFLN NIC — KiCad Source Files

## How to Open in KiCad
1. Download and install **KiCad 7.0+** from https://kicad.org/download/
2. Open `LightRail_Gen3.kicad_pro` (File → Open Project)
3. Click **Schematic Editor** (eeschema icon)
4. Click **PCB Layout Editor** (pcbnew icon)

## Board Specifications
| Parameter | Value |
|-----------|-------|
| Dimensions | 167.65 mm × 111.15 mm (PCIe FHHL) |
| Layers | 15 copper layers |
| RF Layers (1–4) | Rogers RO4350B εr=3.66, tan δ=0.004 |
| Digital/Power (5–14) | ISOLA 370HR High-Tg εr=4.1 |
| Total thickness | 2.0 mm |
| Surface finish | ENIG (recommended for BGA) |

## Impedance Targets
| Net Class | Target | Layer | Width |
|-----------|--------|-------|-------|
| PCIe Gen5 | 85 Ω differential | F.Cu | 0.127mm / 0.127mm gap |
| RF TX drive | 50 Ω single-ended | In3.Cu | 0.172mm |
| General | 50 Ω | F.Cu / B.Cu | 0.25mm |

## Component Summary
| Ref | Value | Package |
|-----|-------|---------|
| U1 | LightRail AI Core ASIC | BGA 20×20 1mm pitch |
| U9 | BCM84881 SerDes | QFP-64 |
| U11/U12 | TFLN MZM 400G | Die (wire-bond) |
| U4 | HMC8410 RF Driver | SMD |
| U2 | TLN1550 DFB Laser | TO-can |
| U3 | XPDV4120R Photodetector | Die |
| U7 | LT8614 Buck | SMD |
| U6 | TPS7A4700 LDO | SMD |
"""

# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════
def generate():
    if os.path.exists(OUT_DIR):
        shutil.rmtree(OUT_DIR)
    os.makedirs(OUT_DIR)
    print(f"Output: {OUT_DIR}\n")

    for fname, content in [
        ("LightRail_Gen3.kicad_sch", build_schematic()),
        ("LightRail_Gen3.kicad_pcb", build_pcb()),
        ("LightRail_Gen3.kicad_pro", build_project()),
        ("README.md", README),
    ]:
        path = os.path.join(OUT_DIR, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✅ {fname}  ({os.path.getsize(path)//1024} KB)")

    # ZIP
    if os.path.exists(ZIP_NAME): os.remove(ZIP_NAME)
    with zipfile.ZipFile(ZIP_NAME, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for fn in sorted(os.listdir(OUT_DIR)):
            zf.write(os.path.join(OUT_DIR, fn), fn)

    print(f"\n📦 {ZIP_NAME}")
    print(f"   {os.path.getsize(ZIP_NAME)//1024} KB  |  {len(os.listdir(OUT_DIR))} files")
    print("   Ready to open in KiCad 7+")

if __name__ == "__main__":
    generate()
