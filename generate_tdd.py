"""
Technical Design Document Generator
Photonic Computing System - LightRails AI
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import datetime

OUTPUT = "Photonic_Computing_TDD.pdf"

# ── Color palette ──────────────────────────────────────────────────────────
DARK_BLUE   = colors.HexColor("#0D1B2A")
MED_BLUE    = colors.HexColor("#1B3A5C")
ACCENT_CYAN = colors.HexColor("#00D4FF")
LIGHT_CYAN  = colors.HexColor("#E0F7FF")
WHITE       = colors.white
LIGHT_GRAY  = colors.HexColor("#F5F6FA")
MED_GRAY    = colors.HexColor("#7F8C8D")
TEXT_DARK   = colors.HexColor("#1A1A2E")

# ── Styles ─────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def make_style(name, parent="Normal", **kw):
    return ParagraphStyle(name, parent=styles[parent], **kw)

cover_title = make_style("CoverTitle",
    fontSize=32, fontName="Helvetica-Bold", textColor=WHITE,
    alignment=TA_CENTER, spaceAfter=8)

cover_sub = make_style("CoverSub",
    fontSize=16, fontName="Helvetica", textColor=ACCENT_CYAN,
    alignment=TA_CENTER, spaceAfter=4)

cover_body = make_style("CoverBody",
    fontSize=11, fontName="Helvetica", textColor=colors.HexColor("#CCDDEE"),
    alignment=TA_CENTER, spaceAfter=4)

h1 = make_style("H1",
    fontSize=18, fontName="Helvetica-Bold", textColor=MED_BLUE,
    spaceBefore=18, spaceAfter=8,
    borderPad=4, borderColor=ACCENT_CYAN, borderWidth=0)

h2 = make_style("H2",
    fontSize=13, fontName="Helvetica-Bold", textColor=DARK_BLUE,
    spaceBefore=12, spaceAfter=6)

h3 = make_style("H3",
    fontSize=11, fontName="Helvetica-Bold", textColor=MED_BLUE,
    spaceBefore=8, spaceAfter=4)

body = make_style("Body",
    fontSize=10, fontName="Helvetica", textColor=TEXT_DARK,
    alignment=TA_JUSTIFY, spaceAfter=6, leading=15)

bullet = make_style("Bullet",
    fontSize=10, fontName="Helvetica", textColor=TEXT_DARK,
    leftIndent=20, spaceAfter=3, leading=14,
    bulletIndent=8, bulletFontName="Helvetica", bulletFontSize=10)

code_style = make_style("Code",
    fontSize=9, fontName="Courier", textColor=colors.HexColor("#2C3E50"),
    backColor=LIGHT_GRAY, borderPad=6,
    leftIndent=16, rightIndent=16, spaceAfter=6, leading=13)

caption = make_style("Caption",
    fontSize=8, fontName="Helvetica-Oblique", textColor=MED_GRAY,
    alignment=TA_CENTER, spaceAfter=4)

# ── Helper builders ────────────────────────────────────────────────────────

def hr():
    return HRFlowable(width="100%", thickness=1.5, color=ACCENT_CYAN,
                      spaceAfter=6, spaceBefore=6)

def section_header(text):
    return [hr(), Paragraph(text, h1), Spacer(1, 4)]

def spec_table(rows, col_widths=None):
    cw = col_widths or [2.5*inch, 4*inch]
    t = Table(rows, colWidths=cw)
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0), MED_BLUE),
        ("TEXTCOLOR",   (0, 0), (-1, 0), WHITE),
        ("FONTNAME",    (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, 0), 10),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ("FONTNAME",    (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",    (0, 1), (-1, -1), 9),
        ("TEXTCOLOR",   (0, 1), (-1, -1), TEXT_DARK),
        ("GRID",        (0, 0), (-1, -1), 0.5, colors.HexColor("#AABBCC")),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",  (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0,0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t

def perf_table(rows, col_widths=None):
    cw = col_widths or [2.2*inch, 1.8*inch, 1.8*inch, 1.2*inch]
    t = Table(rows, colWidths=cw)
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0), DARK_BLUE),
        ("TEXTCOLOR",   (0, 0), (-1, 0), ACCENT_CYAN),
        ("FONTNAME",    (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, 0), 10),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_CYAN]),
        ("FONTNAME",    (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",    (0, 1), (-1, -1), 9),
        ("TEXTCOLOR",   (0, 1), (-1, -1), TEXT_DARK),
        ("GRID",        (0, 0), (-1, -1), 0.5, colors.HexColor("#AABBCC")),
        ("ALIGN",       (1, 0), (-1, -1), "CENTER"),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",  (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0,0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t

def api_table(rows):
    t = Table(rows, colWidths=[2.0*inch, 0.9*inch, 3.6*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0), MED_BLUE),
        ("TEXTCOLOR",   (0, 0), (-1, 0), WHITE),
        ("FONTNAME",    (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, 0), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ("FONTNAME",    (0, 1), (-1, -1), "Courier"),
        ("FONTSIZE",    (0, 1), (-1, -1), 8),
        ("TEXTCOLOR",   (0, 1), (-1, -1), TEXT_DARK),
        ("GRID",        (0, 0), (-1, -1), 0.4, colors.HexColor("#BBCCDD")),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",  (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0,0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("FONTNAME",    (2, 1), (2, -1), "Helvetica"),
    ]))
    return t

# ── Cover page ─────────────────────────────────────────────────────────────

def build_cover():
    cover_bg = Table(
        [[Paragraph("", cover_title)]],
        colWidths=[7.5*inch], rowHeights=[0.01*inch]
    )
    cover_bg.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK_BLUE),
    ]))

    # Banner
    banner_data = [[
        Paragraph("LIGHTRAILS AI", make_style("BannerTop",
            fontSize=10, fontName="Helvetica-Bold",
            textColor=ACCENT_CYAN, alignment=TA_CENTER)),
    ]]
    banner = Table(banner_data, colWidths=[7.5*inch], rowHeights=[0.4*inch])
    banner.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), DARK_BLUE),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
    ]))

    title_block_data = [[
        Paragraph("PHOTONIC COMPUTING SYSTEM", cover_title),
    ],[
        Paragraph("Technical Design Document", cover_sub),
    ],[
        Paragraph("Silicon Photonics + TFLN Modulator Architecture", cover_body),
    ],[
        Spacer(1, 0.15*inch),
    ],[
        Paragraph(f"Version 1.0  |  {datetime.date.today().strftime('%B %d, %Y')}  |  CONFIDENTIAL", cover_body),
    ]]
    title_block = Table(title_block_data, colWidths=[7.5*inch])
    title_block.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), DARK_BLUE),
        ("TOPPADDING",    (0,0),(-1,-1), 4),
        ("BOTTOMPADDING", (0,0),(-1,-1), 4),
    ]))

    # Metrics strip
    metrics = [
        ["49,585 TOPS", "19.71 Tbps", "953 TOPS/W", "150×"],
        ["Peak Throughput", "Aggregate BW", "Efficiency", "Speedup vs GPU"],
    ]
    m_table = Table(metrics, colWidths=[1.875*inch]*4, rowHeights=[0.45*inch, 0.3*inch])
    m_table.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(-1,0), MED_BLUE),
        ("BACKGROUND",  (0,1),(-1,1), DARK_BLUE),
        ("TEXTCOLOR",   (0,0),(-1,0), ACCENT_CYAN),
        ("TEXTCOLOR",   (0,1),(-1,1), colors.HexColor("#AABBCC")),
        ("FONTNAME",    (0,0),(-1,0), "Helvetica-Bold"),
        ("FONTNAME",    (0,1),(-1,1), "Helvetica"),
        ("FONTSIZE",    (0,0),(-1,0), 14),
        ("FONTSIZE",    (0,1),(-1,1), 8),
        ("ALIGN",       (0,0),(-1,-1), "CENTER"),
        ("VALIGN",      (0,0),(-1,-1), "MIDDLE"),
        ("LINEABOVE",   (0,0),(-1,0), 2, ACCENT_CYAN),
        ("LINEBELOW",   (0,-1),(-1,-1), 2, ACCENT_CYAN),
        ("INNERGRID",   (0,0),(-1,-1), 0.5, MED_BLUE),
    ]))

    elems = [
        banner,
        Spacer(1, 0.3*inch),
        title_block,
        Spacer(1, 0.4*inch),
        m_table,
    ]
    return elems

# ── Document sections ───────────────────────────────────────────────────────

def build_toc():
    elems = section_header("Table of Contents")
    toc_items = [
        ("1.", "Introduction & System Overview", "3"),
        ("2.", "Architecture Overview", "3"),
        ("3.", "Photonic Core Module", "4"),
        ("4.", "TFLN Modulator Subsystem", "5"),
        ("5.", "PCIe Interface & Host Integration", "6"),
        ("6.", "FPGA Hybrid Integration", "7"),
        ("7.", "WDM Optical Fabric", "7"),
        ("8.", "REST API Reference", "8"),
        ("9.", "Performance Metrics", "9"),
        ("10.", "PCB Stack-Up & Manufacturing", "10"),
        ("11.", "FEA Simulation Results", "10"),
        ("12.", "Test Plan Summary", "11"),
        ("13.", "Security & Reliability", "11"),
        ("14.", "Glossary", "12"),
    ]
    rows = [["§", "Section", "Page"]]
    for n, title, pg in toc_items:
        rows.append([n, title, pg])
    t = Table(rows, colWidths=[0.5*inch, 5.5*inch, 0.8*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(-1,0), MED_BLUE),
        ("TEXTCOLOR",   (0,0),(-1,0), WHITE),
        ("FONTNAME",    (0,0),(-1,0), "Helvetica-Bold"),
        ("FONTSIZE",    (0,0),(-1,0), 10),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, LIGHT_GRAY]),
        ("FONTNAME",    (0,1),(-1,-1), "Helvetica"),
        ("FONTSIZE",    (0,1),(-1,-1), 9),
        ("GRID",        (0,0),(-1,-1), 0.3, colors.HexColor("#CCDDEE")),
        ("ALIGN",       (2,0),(2,-1), "CENTER"),
        ("VALIGN",      (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",  (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
        ("LEFTPADDING", (0,0),(-1,-1), 6),
    ]))
    elems.append(t)
    return elems

def build_intro():
    elems = section_header("1. Introduction & System Overview")
    elems.append(Paragraph(
        "The <b>LightRails AI Photonic Computing System</b> is a ground-up silicon-photonics accelerator "
        "platform that replaces electronic matrix arithmetic with optical interference, achieving sub-nanosecond "
        "matrix-vector products at energy costs orders of magnitude below GPU equivalents. "
        "This document is the authoritative Technical Design Document (TDD) for the system, covering "
        "hardware architecture, software interfaces, performance data, manufacturing constraints, and test methodology.", body))
    elems.append(Spacer(1, 4))
    elems.append(Paragraph("<b>Document Scope</b>", h2))
    for item in [
        "Photonic core: Clements MZI mesh with ring-resonator amplitude weighting and SCL in-situ learning.",
        "TFLN modulator subsystem: MZM, ring modulators, EO switches at 400 G – 800 G data rates.",
        "PCIe Gen 5 host interface: DMA engine, MMIO register map, multi-board cluster.",
        "FPGA hybrid integration: logic + photonic co-scheduling.",
        "WDM optical fabric: 64-channel C-band multiplexing.",
        "REST API server (Flask), Gerber/CNC/KiCad file services, FEA solver.",
    ]:
        elems.append(Paragraph(f"• {item}", bullet))
    return elems

def build_architecture():
    elems = section_header("2. Architecture Overview")
    elems.append(Paragraph(
        "The system follows a layered architecture separating the optical compute plane from the electronic "
        "control and I/O plane. A PCIe Gen 5 link bridges the host CPU and the photonic accelerator board; "
        "an FPGA provides programmable glue logic for scheduling, calibration, and low-latency control.", body))
    elems.append(Spacer(1, 4))
    # Architecture diagram as ASCII table
    arch_rows = [
        ["Layer", "Component", "Technology"],
        ["Host Software", "Flask REST API  |  Python SDK", "Python 3.9 / NumPy / Numba"],
        ["Host Interface", "PCIe Gen 5 x16  |  DMA Engine", "8 ch. DMA, MMIO @ 0xF0000000"],
        ["Control Plane", "Hybrid FPGA-Photonic Scheduler", "1 M logic cells, 512-wide mesh"],
        ["Compute Plane", "Photonic Matrix Multiplier (128×128)", "Clements MZI + Ring Resonators"],
        ["Modulation", "TFLN MZM + Ring Modulators", "X-cut LiNbO₃, Vπ < 2 V"],
        ["Optical Fabric", "WDM Multiplexer (64 ch.)", "C-band 1530–1565 nm, 100 Gbps/ch"],
        ["PCB / Packaging", "4-layer FR-4, HHHL PCIe card", "Gerber / KiCad design files"],
    ]
    elems.append(perf_table(arch_rows,
        col_widths=[1.7*inch, 2.8*inch, 2.5*inch]))
    return elems

def build_photonic_core():
    elems = section_header("3. Photonic Core Module")
    elems.append(Paragraph("<b>3.1 Photonic Matrix Multiplier</b>", h2))
    elems.append(Paragraph(
        "The core compute element implements a <b>Clements decomposition MZI mesh</b> that realises an "
        "arbitrary N×N unitary matrix in O(N²) MZI stages. Matrix-vector multiplication is performed "
        "fully in the optical domain with a propagation latency of ~10 ps (single light-transit).", body))

    spec_rows = [
        ["Parameter", "Value"],
        ["Matrix dimension (N)", "128 × 128"],
        ["Number of MZI elements", "N(N-1)/2 = 8,128"],
        ["Phase encoding range", "0 – 2π per MZI (θ, φ)"],
        ["Propagation latency", "10 ps (optical)"],
        ["Base throughput", "~16,384 TOPS"],
        ["Operating wavelength", "1550 nm"],
        ["Q-factor (resonators)", "15,000 (default)"],
    ]
    elems.append(spec_table(spec_rows))
    elems.append(Spacer(1, 6))

    elems.append(Paragraph("<b>3.2 Ring-Resonator Amplitude Weighting</b>", h2))
    elems.append(Paragraph(
        "Each MZI stage is preceded by a micro-ring resonator that applies a Lorentzian amplitude weight, "
        "boosting extinction ratio and SNR. Weights are computed via a vectorised binomial moment expansion "
        "(order M=6) across the full resonator array — O(M·N) with zero Python loops.", body))

    elems.append(Paragraph("<b>3.3 Statistical Congruential Learning (SCL)</b>", h2))
    elems.append(Paragraph(
        "SCL is an in-situ adaptive calibration loop that tunes phase settings without back-propagation. "
        "It uses a Knuth/MMIX-style LCG (a=6364136223846793005) and the <b>pigeonhole optimisation</b>: "
        "resonators are partitioned into B=⌈√N⌉ bins, requiring only O(√N) random draws per step "
        "instead of O(N), guaranteeing full coverage by the pigeonhole principle.", body))

    scl_rows = [
        ["SCL Parameter", "Value"],
        ["LCG multiplier (a)", "6,364,136,223,846,793,005"],
        ["LCG increment (c)",  "1,442,695,040,888,963,407"],
        ["Modulus (m)",        "2⁶⁴"],
        ["SCL bins (B)",       "⌈√num_mzi⌉ ≈ 91 for 128×128"],
        ["Default epochs",     "50"],
        ["Default lr",         "0.02"],
        ["Training samples",   "24 per stream session"],
    ]
    elems.append(spec_table(scl_rows))
    return elems

def build_tfln():
    elems = section_header("4. TFLN Modulator Subsystem")
    elems.append(Paragraph(
        "Thin-Film Lithium Niobate (TFLN) modulators are used for all high-speed optical I/O. "
        "TFLN offers a 3× lower Vπ compared to silicon EO modulators, enabling PAM4/PAM8 links at "
        "400 G – 800 G with sub-watt drive power.", body))

    elems.append(Paragraph("<b>4.1 Material Properties</b>", h2))
    mat_rows = [
        ["Property", "Value"],
        ["Ordinary refractive index (n_o)", "2.211 @ 1550 nm"],
        ["Extraordinary index (n_e)", "2.138 @ 1550 nm"],
        ["EO coefficient r₃₃", "30.8 pm/V"],
        ["EO coefficient r₁₃", "8.6 pm/V"],
        ["Propagation loss (TE)", "0.27 dB/cm"],
        ["Propagation loss (TM)", "0.30 dB/cm"],
        ["χ⁽²⁾ (SHG)", "27 pm/V"],
        ["Thermo-optic dn/dT", "3.0 × 10⁻⁵ K⁻¹"],
    ]
    elems.append(spec_table(mat_rows))
    elems.append(Spacer(1, 6))

    elems.append(Paragraph("<b>4.2 Mach-Zehnder Modulator Specs</b>", h2))
    mzm_rows = [
        ["Parameter", "Spec"],
        ["Interaction length", "5,000 µm (active), 15 mm (link)"],
        ["Electrode gap", "10 µm (photonic core), 6 µm (link)"],
        ["Wafer cut", "X-cut (r₃₃ mode)"],
        ["Bandwidth", "100 GHz (3 dB)"],
        ["Insertion loss", "3.5 dB"],
        ["Extinction ratio", "25 dB"],
        ["Vπ (API spec)", "2.5 V"],
        ["Energy/bit @ 400G PAM4", "< 2 pJ/bit"],
    ]
    elems.append(spec_table(mzm_rows))
    elems.append(Spacer(1, 6))

    elems.append(Paragraph("<b>4.3 Photonic Link Performance</b>", h2))
    link_rows = [
        ["Link Config", "Data Rate", "Reach", "Power", "Energy/bit"],
        ["400G PAM4 (8-lane)", "400 Gbps", "2.0 km", "~0.8 W", "2.0 pJ/bit"],
        ["800G PAM4 (8-lane)", "800 Gbps", "2.0 km", "~1.5 W", "1.9 pJ/bit"],
        ["800G PAM8 (short)", "800 Gbps", "0.5 km", "<1.5 W", "<2 pJ/bit"],
    ]
    elems.append(perf_table(link_rows,
        col_widths=[1.8*inch, 1.3*inch, 1.0*inch, 1.0*inch, 1.4*inch]))
    return elems

def build_pcie():
    elems = section_header("5. PCIe Interface & Host Integration")
    elems.append(Paragraph(
        "The photonic accelerator board connects to the host via a <b>PCIe Gen 5 x16</b> slot, "
        "providing ~492 GB/s of bidirectional bandwidth. An 8-channel DMA engine handles "
        "zero-copy transfers; memory-mapped I/O at base address <b>0xF000_0000</b> exposes "
        "all photonic component control registers.", body))

    pcie_rows = [
        ["Parameter", "Value"],
        ["PCIe generation", "Gen 5 (32 GT/s per lane)"],
        ["Lane width", "x16"],
        ["Raw bandwidth", "512 Gbps"],
        ["Effective BW (128b/130b)", "~492 Gbps (~61.5 GB/s)"],
        ["DMA channels", "8 independent"],
        ["MMIO base address", "0xF000_0000"],
        ["Form factor", "HHHL (Half-Height Half-Length)"],
        ["Power consumption", "75 W (board only)"],
        ["Optical ports", "16 (4 laser sources)"],
    ]
    elems.append(spec_table(pcie_rows))
    elems.append(Spacer(1, 6))

    elems.append(Paragraph("<b>5.1 MMIO Register Map</b>", h2))
    reg_rows = [
        ["Register", "Offset", "Description"],
        ["CONTROL",           "0x0000", "System control (reset, enable)"],
        ["STATUS",            "0x0004", "System status flags"],
        ["LASER_POWER",       "0x0008", "12-bit DAC laser power"],
        ["MODULATOR_BIAS",    "0x000C", "Modulator bias voltage"],
        ["PHASE_SHIFTER_0",   "0x0010", "Phase shifter ch.0 (16-bit)"],
        ["PHASE_SHIFTER_1",   "0x0014", "Phase shifter ch.1 (16-bit)"],
        ["WDM_CHANNEL_SELECT","0x0018", "Active WDM channel select"],
        ["DMA_CONTROL",       "0x0028", "DMA engine control"],
        ["PERFORMANCE_COUNTER","0x002C","TOPS measurement counter"],
    ]
    t = Table(reg_rows, colWidths=[2.0*inch, 1.0*inch, 3.5*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(-1,0), MED_BLUE),
        ("TEXTCOLOR",   (0,0),(-1,0), WHITE),
        ("FONTNAME",    (0,0),(-1,0), "Helvetica-Bold"),
        ("FONTSIZE",    (0,0),(-1,0), 9),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, LIGHT_GRAY]),
        ("FONTNAME",    (0,1),(-1,-1), "Courier"),
        ("FONTSIZE",    (0,1),(-1,-1), 8),
        ("GRID",        (0,0),(-1,-1), 0.4, colors.HexColor("#AABBCC")),
        ("VALIGN",      (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",  (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
        ("LEFTPADDING", (0,0),(-1,-1), 6),
        ("FONTNAME",    (0,1),(0,-1), "Courier-Bold"),
        ("FONTNAME",    (2,1),(2,-1), "Helvetica"),
    ]))
    elems.append(t)
    return elems

def build_fpga():
    elems = section_header("6. FPGA Hybrid Integration")
    elems.append(Paragraph(
        "A hybrid FPGA-photonic co-processor handles workloads that benefit from "
        "reconfigurable digital logic alongside optical matrix operations. "
        "The FPGA provides 1 M logic cells and schedules partitioning between "
        "digital and photonic compute paths.", body))
    spec_rows = [
        ["Parameter", "Value"],
        ["FPGA logic cells", "1,000,000"],
        ["FPGA compute", "1,500 GFLOPS"],
        ["Photonic mesh size", "512-wide"],
        ["Photonic throughput", "250 TOPS"],
        ["Optical I/O", "3.2 Tbps"],
        ["Combined throughput", "~250 TOPS + 1.5 TFLOPS"],
        ["Total power (hybrid)", "25 W"],
    ]
    elems.append(spec_table(spec_rows))
    return elems

def build_wdm():
    elems = section_header("7. WDM Optical Fabric")
    elems.append(Paragraph(
        "The wavelength-division multiplexing subsystem carries 64 independent data channels "
        "across the C-band (1530 – 1565 nm). Each channel operates at 100 Gbps, yielding "
        "6.4 Tbps aggregate throughput. Ring resonators tune each channel for drop/add routing.", body))
    wdm_rows = [
        ["Parameter", "Value"],
        ["Number of channels", "64"],
        ["Wavelength range", "1530 – 1565 nm (C-band)"],
        ["Channel spacing", "~0.56 nm (~70 GHz)"],
        ["Per-channel rate", "100 Gbps"],
        ["Aggregate bandwidth", "6.4 Tbps"],
        ["Per-channel power", "-3 dBm (nominal)"],
        ["Resonator type", "Micro-ring (FSR = 20 nm)"],
    ]
    elems.append(spec_table(wdm_rows))
    return elems

def build_api():
    elems = section_header("8. REST API Reference")
    elems.append(Paragraph(
        "The Flask application server exposes a comprehensive REST API at <b>http://0.0.0.0:5001</b>. "
        "All data endpoints return JSON. Simulation endpoints accept POST with a JSON body.", body))

    api_rows = [
        ["Endpoint", "Method", "Description"],
        ["/api/performance",              "GET",  "Aggregate system performance metrics"],
        ["/api/matrix_multiplier",        "GET",  "Matrix multiplier specs & throughput"],
        ["/api/matrix_multiplier/resonator","GET","Ring-resonator weight statistics"],
        ["/api/matrix_multiplier/scl_stream","GET","SSE stream: real-time SCL training epochs"],
        ["/api/matrix_multiplier/scl_train","POST","Blocking SCL train (legacy)"],
        ["/api/matrix_multiplier/scl_reset","POST","Reset MZI phases & resonances"],
        ["/api/matrix_multiply",          "POST", "Run matrix-vector multiply simulation"],
        ["/api/wdm",                      "GET",  "WDM system performance"],
        ["/api/wdm/channels",             "GET",  "Per-channel wavelength & power"],
        ["/api/fft",                      "GET/POST","FFT specs or run simulation"],
        ["/api/fft_transform",            "POST", "Execute optical FFT simulation"],
        ["/api/pcie",                     "GET",  "PCIe board raw performance"],
        ["/api/pcie_board",               "GET",  "PCIe board (frontend format)"],
        ["/api/pcie_transfer",            "POST", "Simulate DMA transfer"],
        ["/api/hybrid",                   "GET",  "FPGA-photonic hybrid specs"],
        ["/api/cluster",                  "GET",  "64-board cluster aggregate metrics"],
        ["/api/tfln/modulator",           "GET",  "TFLN MZM specs"],
        ["/api/tfln/link",                "GET",  "TFLN link specs (800G)"],
        ["/api/tfln/link_400g",           "GET",  "400G link parameters"],
        ["/api/tfln/link_800g",           "GET",  "800G link parameters"],
        ["/api/tfln/comparison",          "GET",  "TFLN vs. Si-photonics comparison"],
        ["/api/tfln/plots",               "GET",  "Generate TFLN characterisation plots"],
        ["/api/gerber/files",             "GET",  "List Gerber PCB files"],
        ["/api/gerber/view/<file>",       "GET",  "Parse & return single Gerber layer"],
        ["/api/gerber/layers",            "GET",  "All Gerber layers for visualisation"],
        ["/api/gerber/projections",       "GET",  "Orthographic PCB projection views"],
        ["/api/cnc/files",                "GET",  "List CNC G-code files"],
        ["/api/cnc/view/<file>",          "GET",  "Parse G-code commands"],
        ["/api/3d_models",                "GET",  "List STL/OBJ 3D model files"],
        ["/api/vlsi/layout",              "GET",  "VLSI die layout (multi-layer Gerber)"],
        ["/api/fea/simulate",             "POST", "Run optical mode FEA simulation"],
        ["/api/kicad/visualize",          "GET",  "Parse KiCad PCB geometry"],
        ["/api/kicad/fea",                "POST", "Thermal + EM FEA on KiCad board"],
        ["/api/execute_workload",         "POST", "Partition & execute DNN workload"],
    ]
    elems.append(api_table(api_rows))
    return elems

def build_performance():
    elems = section_header("9. Performance Metrics")
    elems.append(Paragraph(
        "System-level performance figures are derived from the live API (/api/performance) "
        "combining matrix multiplier, WDM, FFT, PCIe, hybrid, and cluster subsystems.", body))

    perf_rows = [
        ["Metric", "Single Board", "64-Board Cluster", "Unit"],
        ["Peak Throughput",   "~49,586",  "~500",    "TOPS"],
        ["Aggregate BW",      "~19.71",   "12.8",    "Tbps"],
        ["Energy Efficiency", "953.6",    "~2,500",  "TOPS/W"],
        ["Speedup vs. GPU",   "150×",     "150×",    "—"],
        ["Matrix Mult. TOPS", "16,384",   "1.05 M",  "TOPS"],
        ["WDM Bandwidth",     "6.4",      "409.6",   "Tbps"],
        ["PCIe Bandwidth",    "~492",     "~31,488", "Gbps"],
        ["FFT Throughput",    "50",       "3,200",   "TOPS"],
        ["Total Power",       "52",       "200",     "W"],
    ]
    elems.append(perf_table(perf_rows,
        col_widths=[2.3*inch, 1.5*inch, 1.8*inch, 1.1*inch]))
    return elems

def build_pcb():
    elems = section_header("10. PCB Stack-Up & Manufacturing")
    elems.append(Paragraph(
        "The LightRails AI photonic board uses a cost-optimised <b>4-layer FR-4</b> PCB "
        "targeting standard fabrication at JLCPCB / PCBWay. "
        "The original 12-layer Rogers design was rationalised to reduce BOM cost by ~60%.", body))
    stackup = [
        ["Layer", "Type", "Net", "Thickness"],
        ["F.Cu (Top)",  "Signal",  "—",    "35 µm"],
        ["In1.Cu",       "Plane",   "GND",  "35 µm"],
        ["In2.Cu",       "Plane",   "+3V3", "35 µm"],
        ["B.Cu (Bot)",   "Signal",  "—",    "35 µm"],
    ]
    elems.append(perf_table(stackup,
        col_widths=[1.5*inch, 1.2*inch, 1.2*inch, 2.6*inch]))
    elems.append(Spacer(1, 6))
    elems.append(Paragraph("<b>Gerber file set</b> (24 files): copper layers, solder mask, "
        "silkscreen, board outline, and NC drill files (via 0.3 mm min). "
        "An optimised Gerber ZIP is available at <code>gerber_optimized/</code>.", body))
    return elems

def build_fea():
    elems = section_header("11. FEA Simulation Results")
    elems.append(Paragraph(
        "The FEA solver computes optical mode profiles and thermal maps using a "
        "finite-difference method across a 2D cross-section of the photonic waveguide.", body))

    fea_rows = [
        ["Simulation Type", "Parameter", "Simulated Result"],
        ["Optical mode",   "Waveguide: w=0.5 µm, h=0.22 µm, λ=1.55 µm", "Single-mode TE₀₀"],
        ["Thermal (PCB)",  "Max component temp (TFLN modulator)",         "45.2 °C"],
        ["Thermal (PCB)",  "Average board temperature",                   "32.1 °C"],
        ["EM – Impedance", "50 Ω trace target / actual",                  "50.0 / 49.8 Ω"],
        ["EM – Crosstalk", "Differential pair isolation",                 "−42.3 dB"],
        ["EM – Return loss","Signal path return loss",                    "−18.5 dB"],
    ]
    t = Table(fea_rows, colWidths=[1.5*inch, 2.8*inch, 2.2*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(-1,0), MED_BLUE),
        ("TEXTCOLOR",   (0,0),(-1,0), WHITE),
        ("FONTNAME",    (0,0),(-1,0), "Helvetica-Bold"),
        ("FONTSIZE",    (0,0),(-1,0), 9),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, LIGHT_GRAY]),
        ("FONTNAME",    (0,1),(-1,-1), "Helvetica"),
        ("FONTSIZE",    (0,1),(-1,-1), 8),
        ("GRID",        (0,0),(-1,-1), 0.4, colors.HexColor("#AABBCC")),
        ("VALIGN",      (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",  (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
        ("LEFTPADDING", (0,0),(-1,-1), 6),
    ]))
    elems.append(t)
    return elems

def build_test_plan():
    elems = section_header("12. Test Plan Summary")
    elems.append(Paragraph(
        "Production testing follows the <i>Production Test Plan Final</i> document. "
        "Key stages are summarised below.", body))
    tp_rows = [
        ["Test Stage", "Criteria", "Tool"],
        ["Unit – Photonic Core", "multiply() output norm ≠ 0; throughput > 1 TOPS", "pytest / NumPy"],
        ["Unit – TFLN MZM", "Vπ ∈ [1.5, 5] V; BW > 50 GHz", "pytest"],
        ["Unit – WDM", "64 channels, BW = 6.4 Tbps", "pytest"],
        ["Integration – API", "All /api/* routes return HTTP 200", "requests + pytest"],
        ["Integration – SCL", "Loss decreasing over 50 epochs", "SSE stream parser"],
        ["System – Throughput", "Live TOPS ≥ 49,000", "/api/performance"],
        ["System – PCB FEA", "Max temp < 85 °C; EM crosstalk < −35 dB", "fea_integration.py"],
        ["Acceptance – BER", "BER < 10⁻¹⁵ @ 400G PAM4, 2 km", "BERT tester"],
    ]
    t = Table(tp_rows, colWidths=[2.0*inch, 2.8*inch, 1.7*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(-1,0), DARK_BLUE),
        ("TEXTCOLOR",   (0,0),(-1,0), ACCENT_CYAN),
        ("FONTNAME",    (0,0),(-1,0), "Helvetica-Bold"),
        ("FONTSIZE",    (0,0),(-1,0), 9),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, LIGHT_CYAN]),
        ("FONTNAME",    (0,1),(-1,-1), "Helvetica"),
        ("FONTSIZE",    (0,1),(-1,-1), 8),
        ("GRID",        (0,0),(-1,-1), 0.4, colors.HexColor("#AABBCC")),
        ("VALIGN",      (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",  (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
        ("LEFTPADDING", (0,0),(-1,-1), 6),
    ]))
    elems.append(t)
    return elems

def build_security():
    elems = section_header("13. Security & Reliability")
    items = [
        "<b>API Security:</b> Flask debug mode is disabled in production; server binds to 0.0.0.0:5001 — firewall rules must restrict external access.",
        "<b>Input Validation:</b> All POST endpoints validate JSON fields and clamp numeric parameters before passing to simulation kernels.",
        "<b>Error Handling:</b> Uncaught exceptions in FEA/Gerber routes return HTTP 500 with a JSON error body; tracebacks are logged to app.log.",
        "<b>Optical Safety:</b> Laser power is DAC-limited to 100 mW max via the LASER_POWER register (12-bit, full-scale = 4095).",
        "<b>Thermal Protection:</b> FEA hotspot alerting flags components exceeding 60 °C in simulation; hardware OTP fuse at 85 °C.",
        "<b>MTBF Estimate:</b> Optical components (LDs, photodetectors) rated > 100,000 hours; PCIe re-link on error via PERST#.",
    ]
    for item in items:
        elems.append(Paragraph(f"• {item}", bullet))
    return elems

def build_glossary():
    elems = section_header("14. Glossary")
    terms = [
        ("BER",   "Bit Error Rate — probability of an incorrectly decoded bit."),
        ("Clements mesh", "Optimal rectangular MZI decomposition for universal unitaries (Clements et al., 2016)."),
        ("DMA",   "Direct Memory Access — zero-CPU data transfer between host RAM and device."),
        ("EO",    "Electro-Optic — optical effect driven by applied electric field."),
        ("FSR",   "Free Spectral Range — wavelength spacing between resonator modes."),
        ("LCG",   "Linear Congruential Generator — fast pseudo-random number generator."),
        ("MMIO",  "Memory-Mapped I/O — device registers mapped into CPU address space."),
        ("MZI",   "Mach-Zehnder Interferometer — beam splitter + phase shift + combiner."),
        ("PAM4",  "4-level Pulse Amplitude Modulation — 2 bits per symbol."),
        ("SCL",   "Statistical Congruential Learning — in-situ adaptive phase calibration algorithm."),
        ("TFLN",  "Thin-Film Lithium Niobate — EO platform with low Vπ and high bandwidth."),
        ("TOPS",  "Tera Operations Per Second — unit of compute throughput."),
        ("WDM",   "Wavelength Division Multiplexing — simultaneous multi-channel optical transmission."),
        ("Vπ",    "Half-wave voltage — voltage required for π phase shift in a MZM."),
    ]
    rows = [["Term", "Definition"]] + [[t, d] for t, d in terms]
    t = Table(rows, colWidths=[1.5*inch, 5.5*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(-1,0), MED_BLUE),
        ("TEXTCOLOR",   (0,0),(-1,0), WHITE),
        ("FONTNAME",    (0,0),(-1,0), "Helvetica-Bold"),
        ("FONTSIZE",    (0,0),(-1,0), 10),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, LIGHT_GRAY]),
        ("FONTNAME",    (0,1),(-1,-1), "Helvetica"),
        ("FONTSIZE",    (0,1),(-1,-1), 9),
        ("FONTNAME",    (0,1),(0,-1), "Helvetica-Bold"),
        ("GRID",        (0,0),(-1,-1), 0.4, colors.HexColor("#AABBCC")),
        ("VALIGN",      (0,0),(-1,-1), "TOP"),
        ("TOPPADDING",  (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
        ("LEFTPADDING", (0,0),(-1,-1), 6),
    ]))
    elems.append(t)
    return elems

# ── Page footer ────────────────────────────────────────────────────────────

def on_page(canvas, doc):
    canvas.saveState()
    w, h = letter
    canvas.setFillColor(MED_BLUE)
    canvas.rect(0, 0, w, 0.45*inch, fill=True, stroke=False)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(0.5*inch, 0.16*inch,
        "LightRails AI — Photonic Computing System TDD — CONFIDENTIAL")
    canvas.drawRightString(w - 0.5*inch, 0.16*inch,
        f"Page {doc.page}  |  {datetime.date.today().strftime('%Y-%m-%d')}")
    canvas.setStrokeColor(ACCENT_CYAN)
    canvas.setLineWidth(1)
    canvas.line(0, 0.45*inch, w, 0.45*inch)
    canvas.restoreState()

# ── Main ───────────────────────────────────────────────────────────────────

def main():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=letter,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.65*inch,
        title="Photonic Computing System – TDD",
        author="LightRails AI",
        subject="Technical Design Document",
    )

    story = []

    # Cover
    story.extend(build_cover())
    story.append(PageBreak())

    # ToC
    story.extend(build_toc())
    story.append(PageBreak())

    # Sections
    story.extend(build_intro())
    story.append(Spacer(1, 10))
    story.extend(build_architecture())
    story.append(PageBreak())

    story.extend(build_photonic_core())
    story.append(PageBreak())

    story.extend(build_tfln())
    story.append(PageBreak())

    story.extend(build_pcie())
    story.append(Spacer(1, 10))
    story.extend(build_fpga())
    story.append(Spacer(1, 10))
    story.extend(build_wdm())
    story.append(PageBreak())

    story.extend(build_api())
    story.append(PageBreak())

    story.extend(build_performance())
    story.append(Spacer(1, 10))
    story.extend(build_pcb())
    story.append(Spacer(1, 10))
    story.extend(build_fea())
    story.append(PageBreak())

    story.extend(build_test_plan())
    story.append(Spacer(1, 10))
    story.extend(build_security())
    story.append(Spacer(1, 10))
    story.extend(build_glossary())

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"✅  TDD written to: {OUTPUT}")

if __name__ == "__main__":
    main()
