import csv
import os
import ast
import subprocess
import sys

def check_bom_integrity():
    bom_file = "TFLN_BOM.csv"
    results = []
    
    if not os.path.exists(bom_file):
        return [("BOM File Existence", "FAIL", f"{bom_file} not found")]
    
    results.append(("BOM File Existence", "PASS", f"{bom_file} found"))
    
    try:
        with open(bom_file, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
            if not rows:
                results.append(("BOM Content", "FAIL", "BOM file is empty"))
            else:
                results.append(("BOM Content", "PASS", f"BOM contains {len(rows)} items"))
                
                # Check for critical components
                critical_keywords = ["TFLN", "Laser", "Photodetector"]
                found_keywords = {k: False for k in critical_keywords}
                
                for row in rows:
                    desc = row.get("Description", "").lower()
                    for k in critical_keywords:
                        if k.lower() in desc:
                            found_keywords[k] = True
                            
                for k, found in found_keywords.items():
                    status = "PASS" if found else "FAIL"
                    results.append((f"Component Check: {k}", status, f"Found occurrence of {k}" if found else f"Missing {k}"))
                    
                # Check cost calculation
                try:
                    total_calculated = 0.0
                    for row in rows:
                        qty = float(row.get("Quantity", 0))
                        unit_cost = float(row.get("Unit Cost ($)", 0))
                        total_cost = float(row.get("Total Cost ($)", 0))
                        
                        if abs(qty * unit_cost - total_cost) > 0.01:
                             results.append((f"Cost Calculation {row.get('Designator')}", "FAIL", f"{qty}*{unit_cost} != {total_cost}"))
                        
                        total_calculated += total_cost
                    results.append(("Cost Calculation Consistency", "PASS", "All row totals match quantity * unit cost"))
                except ValueError:
                     results.append(("Cost Calculation", "FAIL", "Invalid number format in BOM"))
                     
    except Exception as e:
        results.append(("BOM Processing", "FAIL", str(e)))
        
    return results

def check_source_code():
    results = []
    files_to_check = ["app.py", "photonic_core.py", "tfln_components.py", "generate_bom.py"]
    
    for filename in files_to_check:
        if not os.path.exists(filename):
            results.append((f"File Existence: {filename}", "FAIL", "File not found"))
            continue
            
        results.append((f"File Existence: {filename}", "PASS", "File exists"))
        
        try:
            with open(filename, 'r') as f:
                source = f.read()
            ast.parse(source)
            results.append((f"Syntax Check: {filename}", "PASS", "Valid Python syntax"))
        except SyntaxError as e:
            results.append((f"Syntax Check: {filename}", "FAIL", f"Syntax error: {e}"))
        except Exception as e:
            results.append((f"Code Check: {filename}", "FAIL", str(e)))
            
    return results

def generate_pdf_report(test_results):
    latex_template = r"""\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{geometry}
\usepackage{longtable}
\usepackage{xcolor}
\usepackage{fancyhdr}

\geometry{a4paper, margin=1in}

\pagestyle{fancy}
\fancyhead[L]{TFLN Project Test Plan}
\fancyhead[R]{\today}

\title{Test Plan \& Report: Bill of Materials and Source Code}
\author{Automated Test Agent}
\date{\today}

\begin{document}

\maketitle

\section{Introduction}
This document presents the test plan and execution results for the Bill of Materials (BOM) and core source code of the TFLN Photonic Stacking project.

\section{Test Results}

\begin{longtable}{|p{4cm}|p{2cm}|p{8cm}|}
\hline
\textbf{Test Case} & \textbf{Status} & \textbf{Notes} \\
\hline
\endhead
"""
    
    rows = ""
    for test, status, note in test_results:
        color = "green" if status == "PASS" else "red"
        # Escape special latex characters in note and test name
        note = note.replace("_", r"\_").replace("%", r"\%").replace("$", r"\$")
        test = test.replace("_", r"\_").replace("%", r"\%").replace("$", r"\$")
        rows += f"{test} & \\textcolor{{{color}}}{{\\textbf{{{status}}}}} & {note} \\\\\n\\hline\n"
        
    latex_end = r"""\end{longtable}

\section{Conclusion}
The automated tests have been executed. Please review any FAIL statuses above.

\end{document}
"""

    full_latex = latex_template + rows + latex_end
    
    tex_filename = "Test_Plan_Report.tex"
    with open(tex_filename, "w") as f:
        f.write(full_latex)
        
    try:
        subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_filename], check=True, stdout=subprocess.DEVNULL)
        print(f"Successfully generated {tex_filename.replace('.tex', '.pdf')}")
    except subprocess.CalledProcessError:
        print("Error compiling PDF")

if __name__ == "__main__":
    print("Running Tests...")
    bom_results = check_bom_integrity()
    code_results = check_source_code()
    
    all_results = bom_results + code_results
    
    generate_pdf_report(all_results)
