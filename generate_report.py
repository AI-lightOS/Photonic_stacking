import os
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
import tempfile
import time

def render_math(latex_str, filename):
    """Renders a LaTeX string to an image file using matplotlib"""
    fig = plt.figure(figsize=(6, 1))
    text = fig.text(0.5, 0.5, f"${latex_str}$", fontsize=20, ha='center', va='center')
    plt.axis('off')
    
    # Save to buffer or temp file
    plt.savefig(filename, bbox_inches='tight', dpi=300, transparent=True)
    plt.close()

def generate_report(output_filename="Technical_Report_FEA_Derivation.pdf"):
    doc = SimpleDocTemplate(output_filename, pagesize=LETTER,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
    
    Story = []
    
    # Title
    Story.append(Paragraph("<b>Technical Report: Finite Difference Mode Solver Derivation</b>", styles['Title']))
    Story.append(Spacer(1, 12))
    Story.append(Paragraph(f"Date: {time.strftime('%Y-%m-%d')}", styles['Center']))
    Story.append(Spacer(1, 24))
    
    # Abstract
    Story.append(Paragraph("<b>Abstract</b>", styles['Heading2']))
    Story.append(Paragraph("This report details the mathematical formulation and finite difference implementation for solving the scalar Helmholtz equation in optical waveguides. The derivation assumes a scalar field approximation for weakly guiding structures.", styles['Justify']))
    Story.append(Spacer(1, 12))
    
    # 1. Governing Equation
    Story.append(Paragraph("<b>1. Governing Physical Equation</b>", styles['Heading2']))
    Story.append(Paragraph("We start with the scalar Helmholtz equation for the electric field $E(x,y)$ propagating in the $z$-direction with propagation constant $\\beta$:", styles['Justify']))
    Story.append(Spacer(1, 12))
    
    render_math(r"\nabla_\perp^2 E(x,y) + k_0^2 n^2(x,y) E(x,y) = \beta^2 E(x,y)", "eq1.png")
    Story.append(Image("eq1.png", width=300, height=50))
    Story.append(Spacer(1, 12))
    
    Story.append(Paragraph("Where $k_0 = 2\pi/\lambda$ is the vacuum wavenumber and $n(x,y)$ is the refractive index distribution.", styles['Justify']))
    
    # 2. Discretization
    Story.append(Paragraph("<b>2. Finite Difference Discretization</b>", styles['Heading2']))
    Story.append(Paragraph("We discretize the domain into a grid with spacing $\Delta x$ and $\Delta y$. The Laplacian operator is approximated using the central difference scheme (5-point stencil):", styles['Justify']))
    Story.append(Spacer(1, 12))
    
    render_math(r"\frac{\partial^2 E}{\partial x^2} \approx \frac{E_{i+1,j} - 2E_{i,j} + E_{i-1,j}}{\Delta x^2}", "eq2.png")
    Story.append(Image("eq2.png", width=250, height=50))
    Story.append(Spacer(1, 6))
    
    render_math(r"\frac{\partial^2 E}{\partial y^2} \approx \frac{E_{i,j+1} - 2E_{i,j} + E_{i,j-1}}{\Delta y^2}", "eq3.png")
    Story.append(Image("eq3.png", width=250, height=50))
    Story.append(Spacer(1, 12))
    
    # 3. Matrix Formulation
    Story.append(Paragraph("<b>3. Matrix Formulation</b>", styles['Heading2']))
    Story.append(Paragraph("Substituting the discrete approximations into the Helmholtz equation yields a linear algebraic eigenvalue problem:", styles['Justify']))
    Story.append(Spacer(1, 12))
    
    render_math(r"(\mathbf{L} + \mathbf{V}) \mathbf{\Phi} = \beta^2 \mathbf{\Phi}", "eq4.png")
    Story.append(Image("eq4.png", width=200, height=40))
    Story.append(Spacer(1, 12))
    
    Story.append(Paragraph("Here, $\mathbf{L}$ is the sparse Laplacian matrix constructed from the Kronecker sum of 1D second-derivative operators:", styles['Justify']))
    
    render_math(r"\mathbf{L} = \mathbf{D}_{yy} \otimes \mathbf{I}_x + \mathbf{I}_y \otimes \mathbf{D}_{xx}", "eq5.png")
    Story.append(Image("eq5.png", width=250, height=40))
    Story.append(Spacer(1, 12))
    
    Story.append(Paragraph("And $\mathbf{V}$ is the diagonal matrix representing the refractive index profile:", styles['Justify']))
    
    render_math(r"\mathbf{V} = \text{diag}(k_0^2 n^2)", "eq6.png")
    Story.append(Image("eq6.png", width=150, height=30))
    Story.append(Spacer(1, 12))

    # 4. Implementation Details
    Story.append(Paragraph("<b>4. Computational Implementation</b>", styles['Heading2']))
    Story.append(Paragraph("The solver is implemented in Python using <code>scipy.sparse</code> for efficient memory usage. The eigenvalue problem is solved using the implicitly restarted Arnoldi method (via <code>scipy.sparse.linalg.eigs</code>) to find the largest real eigenvalues corresponding to the guided modes.", styles['Justify']))
    Story.append(Spacer(1, 12))
    
    Story.append(Paragraph("<b>5. Conclusion</b>", styles['Heading2']))
    Story.append(Paragraph("This formulation provides a robust and computationally efficient method for analyzing optical modes in arbitrary refractive index distributions defined by Gerber files.", styles['Justify']))
    
    doc.build(Story)
    
    # Cleanup temp images
    for f in ["eq1.png", "eq2.png", "eq3.png", "eq4.png", "eq5.png", "eq6.png"]:
        if os.path.exists(f):
            os.remove(f)
            
    print(f"Report generated: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    generate_report()
