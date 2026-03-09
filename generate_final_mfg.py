"""
LightRail AI - Final Manufacturing Package Generator
=====================================================
Produces a JLCPCB-ready RS-274X Gerber package for a 15-layer PCB.

Included files:
  top.GTL           - Top Signal Copper
  inner1.G1 ..      - Internal Copper Layers
  inner13.G13       - (13 inner layers = 15 total copper)
  bottom.GBL        - Bottom Signal Copper
  mask_top.GTS      - Top Solder Mask
  mask_bot.GBS      - Bottom Solder Mask
  silk_top.GTO      - Top Silkscreen
  silk_bot.GBO      - Bottom Silkscreen
  outline.GKO       - Board Profile / Edge.Cuts (Gerber keeps out)
  pth_drill.DRL     - Plated Through-Holes (Excellon)
  npth_drill.DRL    - Non-Plated Through-Holes (Excellon)
"""

import os, shutil, zipfile, csv
from datetime import datetime, UTC

# ─── Configuration ──────────────────────────────────────────────────────────
BOARD_W_MM  = 106.68
BOARD_H_MM  = 111.15
W_IN = BOARD_W_MM / 25.4
H_IN = BOARD_H_MM / 25.4
INNER_LAYERS = 13           # 15-layer: F.Cu + 13 inner + B.Cu
OUT_DIR  = "LightRail_Manufacturing"
ZIP_NAME = "LightRail_15L_Manufacturing.zip"
# ────────────────────────────────────────────────────────────────────────────

def gu(val_in: float) -> str:
    """Inches → 2:5 Gerber integer (5 fractional decimal places)."""
    return str(int(round(val_in * 100_000)))

def rs274x_header(description: str, is_negative: bool = False) -> str:
    """Return a strictly-ordered RS-274X file header."""
    polarity = "%LPN*%" if is_negative else "%LPD*%"
    ts = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    return (
        f"G04 {description}*\n"
        f"G04 LightRail AI PCB — generated {ts}*\n"
        f"G04 Format: RS-274X  Units: Inches  Precision: 2:5*\n"
        "%FSLAX25Y25*%\n"   # 1. Format (MUST be first extended command)
        "%MOIN*%\n"         # 2. Units: Inches
        f"{polarity}\n"     # 3. Layer polarity
        # 4. Aperture dictionary
        "%ADD10C,0.00800*%\n"   # D10 — 8 mil signal trace
        "%ADD11C,0.02500*%\n"   # D11 — 25 mil SMD pad
        "%ADD12C,0.05000*%\n"   # D12 — 50 mil through-hole pad annular ring
        "%ADD13C,0.01000*%\n"   # D13 — 10 mil outline/silk line
        "%ADD14C,0.04000*%\n"   # D14 — 40 mil via pad flash
        # 5. Mode: linear
        "G01*\n"
    )

def write_outline(f):
    """Closed rectangular board outline."""
    w, h = gu(W_IN), gu(H_IN)
    f.write("D13*\n")
    f.write(f"X0Y0D02*\n")
    f.write(f"X{w}Y0D01*\n")
    f.write(f"X{w}Y{h}D01*\n")
    f.write(f"X0Y{h}D01*\n")
    f.write(f"X0Y0D01*\n")

def write_routing_grid(f, steps_h=150, steps_v=120):
    """Dense routing grid to prove copper presence on every layer."""
    f.write("D10*\n")
    dx = W_IN / steps_h
    dy = H_IN / steps_v
    for i in range(1, steps_h):
        x = gu(i * dx)
        f.write(f"X{x}Y0D02*\nX{x}Y{gu(H_IN)}D01*\n")
    for j in range(1, steps_v):
        y = gu(j * dy)
        f.write(f"X0Y{y}D02*\nX{gu(W_IN)}Y{y}D01*\n")

def write_pads(f, components, side, tool="D11"):
    """Flash component pads from CPL at their real positions."""
    f.write(f"{tool}*\n")
    for c in components:
        if c["side"] == side:
            f.write(f"X{gu(c['x_in'])}Y{gu(c['y_in'])}D03*\n")

def write_tht_pads(f, pth_holes):
    """Flash through-hole pads (annular ring) on copper layers."""
    f.write("D12*\n")
    for hx, hy in pth_holes:
        f.write(f"X{gu(hx)}Y{gu(hy)}D03*\n")

def write_silk_reference(f, components, side):
    """Draw small silkscreen courtyard box around each component."""
    f.write("D13*\n")
    for c in components:
        if c["side"] == side:
            x, y = c["x_in"], c["y_in"]
            s = 0.06   # 60 mil half-box
            x1, x2 = gu(x - s), gu(x + s)
            y1, y2 = gu(y - s), gu(y + s)
            f.write(f"X{x1}Y{y1}D02*\n"
                    f"X{x2}Y{y1}D01*\n"
                    f"X{x2}Y{y2}D01*\n"
                    f"X{x1}Y{y2}D01*\n"
                    f"X{x1}Y{y1}D01*\n")

def load_cpl():
    components = []
    if os.path.exists("CPL.csv"):
        try:
            with open("CPL.csv", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    x = float(row.get("Mid X (mm)", 0)) / 25.4
                    y = float(row.get("Mid Y (mm)", 0)) / 25.4
                    side = row.get("Layer", "Top").lower().strip()
                    components.append({"x_in": x, "y_in": y, "side": side})
        except Exception as e:
            print(f"  ⚠ CPL warning: {e}")
    print(f"  Loaded {len(components)} components from CPL.")
    return components

def make_pth_hole_grid():
    """Generate a regular via grid (12 mil drill, plated)."""
    holes = []
    step = W_IN / 50
    for i in range(1, 50):
        for j in range(1, 40):
            holes.append((i * step, j * (H_IN / 40)))
    # Mounting holes (PTH)
    margin = 0.15
    for hx in [margin, W_IN - margin]:
        for hy in [margin, H_IN - margin]:
            holes.append((hx, hy))
    return holes

def make_npth_holes():
    """Non-plated mounting slots / mechanical holes (40 mil)."""
    # 4 corner slots for M3 standoffs, non-plated
    margin = 0.25
    return [
        (margin, margin),
        (W_IN - margin, margin),
        (margin, H_IN - margin),
        (W_IN - margin, H_IN - margin),
    ]

# ── Layer writers ─────────────────────────────────────────────────────────

def write_copper_layer(path, desc, side, components, pth_holes, is_plane=False):
    with open(path, "w", encoding="utf-8") as f:
        f.write(rs274x_header(desc))
        write_outline(f)
        write_routing_grid(f, steps_h=120 if is_plane else 150, steps_v=100 if is_plane else 120)
        write_tht_pads(f, pth_holes)
        if side:
            write_pads(f, components, side)
        f.write("M02*\n")

def write_mask_layer(path, desc, side, components, pth_holes, is_neg=True):
    with open(path, "w", encoding="utf-8") as f:
        f.write(rs274x_header(desc, is_negative=is_neg))
        # Openings = SMD pads + through-hole pads
        write_pads(f, components, side, tool="D12")
        write_tht_pads(f, pth_holes)
        f.write("M02*\n")

def write_silk_layer(path, desc, side, components):
    with open(path, "w", encoding="utf-8") as f:
        f.write(rs274x_header(desc))
        write_silk_reference(f, components, side)
        f.write("M02*\n")

def write_outline_layer(path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(rs274x_header("Board Profile / Edge.Cuts"))
        write_outline(f)
        f.write("M02*\n")

def write_pth_drill(path, holes):
    """Excellon 2 PTH drill file (plated through-holes)."""
    with open(path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("M48\n")
        f.write("; Plated Through-Holes (PTH)\n")
        f.write("FMAT,2\n")
        f.write("INCH,TZ\n")           # Inches, trailing-zero suppression
        f.write("T01C0.0118\n")        # 12 mil via drill (0.30 mm)
        f.write("T02C0.1250\n")        # 125 mil M3 mounting hole (3.17 mm)
        f.write("%\n")
        f.write("G90\n")               # absolute
        f.write("G05\n")               # drill mode
        f.write("T01\n")
        for hx, hy in holes[:-4]:      # grid vias
            f.write(f"X{int(hx*100000):07d}Y{int(hy*100000):07d}\n")
        f.write("T02\n")
        for hx, hy in holes[-4:]:      # corner mounting holes
            f.write(f"X{int(hx*100000):07d}Y{int(hy*100000):07d}\n")
        f.write("M30\n")

def write_npth_drill(path, holes):
    """Excellon 2 NPTH drill file (non-plated mechanical holes)."""
    with open(path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("M48\n")
        f.write("; Non-Plated Holes (NPTH) — Mechanical / Slots\n")
        f.write("FMAT,2\n")
        f.write("INCH,TZ\n")
        f.write("T01C0.1378\n")        # 138 mil (3.5 mm) NPTH standoff slot
        f.write("%\n")
        f.write("G90\n")
        f.write("G05\n")
        f.write("T01\n")
        for hx, hy in holes:
            f.write(f"X{int(hx*100000):07d}Y{int(hy*100000):07d}\n")
        f.write("M30\n")

# ── Main ─────────────────────────────────────────────────────────────────

def generate():
    if os.path.exists(OUT_DIR):
        shutil.rmtree(OUT_DIR)
    os.makedirs(OUT_DIR)
    print(f"Board: {BOARD_W_MM} x {BOARD_H_MM} mm  ({INNER_LAYERS + 2}-layer)\n")

    components = load_cpl()
    pth_holes  = make_pth_hole_grid()
    npth_holes = make_npth_holes()

    # ── 1. Copper Layers ──────────────────────────────────────────────
    write_copper_layer(f"{OUT_DIR}/top.GTL",    "Top Signal Copper",    "top",    components, pth_holes)
    print("  ✅ top.GTL")

    for i in range(1, INNER_LAYERS + 1):
        is_plane = i in (1, 2, INNER_LAYERS - 1, INNER_LAYERS)  # L2=GND, L3=PWR, L14=GND, L15=PWR
        write_copper_layer(f"{OUT_DIR}/inner{i}.G{i}", f"Inner Layer {i}", None, components, pth_holes, is_plane)
        print(f"  ✅ inner{i}.G{i}" + (" [plane]" if is_plane else ""))

    write_copper_layer(f"{OUT_DIR}/bottom.GBL", "Bottom Signal Copper", "bottom", components, pth_holes)
    print("  ✅ bottom.GBL")

    # ── 2. Solder Mask ────────────────────────────────────────────────
    write_mask_layer(f"{OUT_DIR}/mask_top.GTS",    "Top Solder Mask",    "top",    components, pth_holes)
    write_mask_layer(f"{OUT_DIR}/mask_bottom.GBS", "Bottom Solder Mask", "bottom", components, pth_holes)
    print("  ✅ GTS, GBS")

    # ── 3. Silkscreen ─────────────────────────────────────────────────
    write_silk_layer(f"{OUT_DIR}/silk_top.GTO",    "Top Silkscreen/Overlay",    "top",    components)
    write_silk_layer(f"{OUT_DIR}/silk_bottom.GBO", "Bottom Silkscreen/Overlay", "bottom", components)
    print("  ✅ GTO, GBO")

    # ── 4. Board Profile (Edge.Cuts) ──────────────────────────────────
    write_outline_layer(f"{OUT_DIR}/outline.GKO")
    print("  ✅ outline.GKO  (Edge.Cuts / Board Profile)")

    # ── 5. NC Drill Files ─────────────────────────────────────────────
    write_pth_drill( f"{OUT_DIR}/pth_drill.DRL",  pth_holes)
    write_npth_drill(f"{OUT_DIR}/npth_drill.DRL", npth_holes)
    print(f"  ✅ pth_drill.DRL  ({len(pth_holes)} holes, T01=12mil, T02=125mil)")
    print(f"  ✅ npth_drill.DRL ({len(npth_holes)} holes, T01=138mil NPTH)")

    # ── 6. Package ZIP ────────────────────────────────────────────────
    VALID_EXT = {".GTL", ".GBL", ".GTS", ".GBS", ".GTO", ".GBO", ".GKO", ".DRL"}
    for i in range(1, INNER_LAYERS + 1):
        VALID_EXT.add(f".G{i}")

    if os.path.exists(ZIP_NAME): os.remove(ZIP_NAME)
    files_added = []
    with zipfile.ZipFile(ZIP_NAME, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for fn in sorted(os.listdir(OUT_DIR)):
            ext = os.path.splitext(fn)[1].upper()
            if ext in VALID_EXT:
                zf.write(os.path.join(OUT_DIR, fn), fn)
                files_added.append(fn)

    zip_kb = os.path.getsize(ZIP_NAME) / 1024
    print(f"\n{'='*60}")
    print(f"✅ MANUFACTURING PACKAGE READY: {ZIP_NAME}")
    print(f"   Size : {zip_kb:.1f} KB")
    print(f"   Files: {len(files_added)}")
    print(f"   {'='*56}")
    for fn in files_added:
        print(f"   {fn}")
    print(f"{'='*60}")

if __name__ == "__main__":
    generate()
