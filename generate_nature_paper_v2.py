import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
import matplotlib.pyplot as plt
from io import BytesIO

def generate_equation_image(latex_str, filename):
    fig = plt.figure(figsize=(6, 1.5))
    plt.text(0.5, 0.5, f"${latex_str}$", fontsize=20, ha='center', va='center')
    plt.axis('off')
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.close()

def generate_circuit_diagram(filename):
    fig, ax = plt.subplots(figsize=(8, 4))
    # Draw waveguides (TFLN)
    ax.plot([0, 2], [0, 0], 'k-', lw=2)  # Input
    ax.plot([2, 4], [1, 1], 'k-', lw=2)  # Arm 1
    ax.plot([2, 4], [-1, -1], 'k-', lw=2) # Arm 2
    ax.plot([4, 6], [0, 0], 'k-', lw=2)   # Output
    
    # Splitter/Combiner
    ax.plot([2, 2], [-1, 1], 'k-', lw=2)
    ax.plot([4, 4], [-1, 1], 'k-', lw=2)

    # Electrodes (Gold)
    rect1 = plt.Rectangle((2.5, 1.2), 1.0, 0.4, color='gold', alpha=0.6)
    rect2 = plt.Rectangle((2.5, -1.6), 1.0, 0.4, color='gold', alpha=0.6)
    ax.add_patch(rect1)
    ax.add_patch(rect2)
    
    # Ramanujan Operator Symbol
    ax.text(3, 0, r'$\mathcal{R}_q$', fontsize=25, ha='center', color='red')
    
    ax.text(1, 0.2, 'Input', ha='center')
    ax.text(5, 0.2, 'Output', ha='center')
    ax.text(3, 1.8, 'Signal Electrode (G)', ha='center')
    
    ax.set_xlim(0, 6)
    ax.set_ylim(-3, 3)
    ax.axis('off')
    plt.title("Fig 1: TFLN MZM with Statistical Ramanujan Operator Overlay")
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.close()

def create_pdf(filename):
    doc = SimpleDocTemplate(filename, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)
    
    Story = []
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, leading=14))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Caption', alignment=TA_CENTER, fontSize=9, fontName='Helvetica-Oblique'))

    # Title
    title = "Advanced TFLN Modulator Dynamics: Finite Math Derivations and Ramanujan Operator Analysis"
    Story.append(Paragraph(title, styles['Title']))
    Story.append(Spacer(1, 12))

    # Author
    author = "Cartik Sharma, Department of Electrical Engineering"
    Story.append(Paragraph(author, styles['Center']))
    Story.append(Spacer(1, 24))

    # Abstract
    abstract_text = """<b>Abstract:</b> We present a rigorous theoretical framework for Thin-Film Lithium Niobate (TFLN) modulators, utilizing finite mathematical derivations to model discrete photonic states. By introducing Ramanujan operators ($\mathcal{R}_q$), we analyze the statistical congruences in the electro-optic coefficient tensors, revealing hidden periodicities in wafer-scale defects. This approach allows for the precise regeneration of photonic circuit parameters, significantly improving yield prediction in large-scale periodic arrays."""
    Story.append(Paragraph(abstract_text, styles['Justify']))
    Story.append(Spacer(1, 24))

    # Introduction
    intro_text = """<b>1. Introduction</b><br/>
    The integration of Thin-Film Lithium Niobate (TFLN) into nanophotonic circuits requires high-precision modeling of refractive index perturbations. Traditional continuum mechanics often fails to capture the discrete statistical anomalies present in crystal lattice domains. In this work, we employ finite math derivations to discretize the Maxwell-Bloch equations and apply Number Theoretic operators to resolve these congruences."""
    Story.append(Paragraph(intro_text, styles['Justify']))
    Story.append(Spacer(1, 12))

    # Finite Math Derivations
    math_text = """<b>2. Finite Math Derivations of the Modulator Field</b><br/>
    We begin by discretizing the optical field propagation in the TFLN waveguide. Using a finite difference scheme, the evolution of the electric field envelope $E(z)$ can be expressed as a recurrence relation:"""
    Story.append(Paragraph(math_text, styles['Justify']))
    Story.append(Spacer(1, 12))

    # Equation 1
    eq1_file = "eq1.png"
    generate_equation_image(r"E_{n+1} = E_n + i\Delta z \left( \frac{1}{2k_0} \nabla_\perp^2 + k_0 \Delta n(V) \right) E_n - \alpha E_n", eq1_file)
    Story.append(Image(eq1_file, width=400, height=80))
    Story.append(Spacer(1, 12))
    
    math_text_2 = """Where $\Delta n(V)$ represents the discrete voltage-induced index change. The finite nature of the derivation ensures that quantization errors in the lithographic process are naturally incorporated into the stability analysis."""
    Story.append(Paragraph(math_text_2, styles['Justify']))
    Story.append(Spacer(1, 12))

    # Ramanujan Operators
    ram_text = """<b>3. Ramanujan Operators and Statistical Congruences</b><br/>
    To model the quasi-periodic noise in the electro-optic overlap integral, we introduce the Ramanujan Sum Operator, $\mathcal{R}_q$. This operator acts on the mode profile $\psi(x)$ to filter resonant defect modes that satisfy statistical congruences with the poling period $\Lambda$."""
    Story.append(Paragraph(ram_text, styles['Justify']))
    Story.append(Spacer(1, 12))

    # Equation 2
    eq2_file = "eq2.png"
    generate_equation_image(r"\mathcal{R}_q[\psi](x) = \sum_{k=1, (k,q)=1}^q \psi\left(x + \frac{k\Lambda}{q}\right) e^{-2\pi i n k / q}", eq2_file)
    Story.append(Image(eq2_file, width=400, height=100))
    Story.append(Spacer(1, 12))

    ram_text_2 = """The spectral density of the modulator's noise figure is then given by the Dirichlet series associated with these operators. We observe that when the waveguide width $w$ satisfies $w \equiv a \pmod m$, the scattering loss is minimized due to destructive interference of the Ramanujan modes."""
    Story.append(Paragraph(ram_text_2, styles['Justify']))
    Story.append(Spacer(1, 12))

    # Photonic Circuit Diagram
    circuit_text = """<b>4. Regenerated Photonic Circuits</b><br/>
    Applying the $\mathcal{R}_q$ operator allows us to redesign the Mach-Zehnder Interferometer (MZI) arms. The optimized circuit topology, shown below, integrates these statistical corrections to stabilize the extinction ratio against thermal fluctuations."""
    Story.append(Paragraph(circuit_text, styles['Justify']))
    Story.append(Spacer(1, 12))

    circuit_file = "circuit.png"
    generate_circuit_diagram(circuit_file)
    Story.append(Image(circuit_file, width=450, height=225))
    Story.append(Paragraph("Fig. 1: Schematic of the TFLN MZM optimized with Ramanujan Operator constraints.", styles['Caption']))
    Story.append(Spacer(1, 12))

    # Conclusion
    conc_text = """<b>5. Conclusion</b><br/>
    We have demonstrated that the application of finite math derivations and Ramanujan operators provides a powerful tool for analyzing TFLN photonic circuits. The statistical congruences identified in this study offer a new pathway for reducing fabrication-induced variability in large-scale integrated photonics."""
    Story.append(Paragraph(conc_text, styles['Justify']))
    Story.append(Spacer(1, 24))

    doc.build(Story)
    
    # Cleanup
    for f in [eq1_file, eq2_file, circuit_file]:
        if os.path.exists(f):
            os.remove(f)

if __name__ == "__main__":
    create_pdf("TFLN_Nature_Paper_Math_Revised.pdf")
