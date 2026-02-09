@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM LIGHTRAIL_AI_NCE - Windows Setup (Create folders & all Python scripts)
REM ═══════════════════════════════════════════════════════════════════════════
REM
REM Usage: Save as setup_lightrail.bat and run it
REM This will create all folders and Python scripts automatically
REM
REM ═══════════════════════════════════════════════════════════════════════════

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                                                                            ║
echo ║           LIGHTRAIL_AI_NCE - WINDOWS AUTOMATED SETUP                      ║
echo ║                                                                            ║
echo ║              Creating folders and Python scripts...                       ║
echo ║                                                                            ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.

REM ═══════════════════════════════════════════════════════════════════════════
REM Step 1: Create folder structure
REM ═══════════════════════════════════════════════════════════════════════════

echo [1/3] Creating folder structure...

mkdir C:\LightRail_AI_NCE\kicad_project 2>nul
mkdir C:\LightRail_AI_NCE\scripts 2>nul
mkdir C:\LightRail_AI_NCE\output\gerber 2>nul
mkdir C:\LightRail_AI_NCE\output\drill 2>nul
mkdir C:\LightRail_AI_NCE\output\bom 2>nul

echo [✓] Folders created
echo.

REM ═══════════════════════════════════════════════════════════════════════════
REM Step 2: Create Python scripts
REM ═══════════════════════════════════════════════════════════════════════════

echo [2/3] Creating Python automation scripts...

REM Create 01_create_project.py
(
echo #!/usr/bin/env python3
echo """
echo Script 1: Create KiCAD PCB Project
echo Creates: 100mm × 80mm board with design rules
echo Usage: python 01_create_project.py
echo """
echo.
echo import pcbnew
echo import os
echo import sys
echo.
echo PROJECT_DIR = r"C:\LightRail_AI_NCE\kicad_project"
echo PROJECT_NAME = "LightRail_AI_NCE"
echo.
echo def main^(^):
echo     try:
echo         print^("\n[→] Creating new PCB project..."^)
echo         
echo         board = pcbnew.BOARD^(^)
echo         
echo         board.GetPageSettings^(^).SetWidthMM^(100^)
echo         board.GetPageSettings^(^).SetHeightMM^(80^)
echo         print^("[✓] Board size: 100mm × 80mm"^)
echo         
echo         design_rules = board.GetDesignSettings^(^)
echo         design_rules.m_TrackMinWidth = int^(0.2e6^)
echo         design_rules.m_MinClearance = int^(0.15e6^)
echo         design_rules.m_ViasMinSize = int^(0.6e6^)
echo         design_rules.m_ViasMinDrill = int^(0.3e6^)
echo         design_rules.m_ViasMinAnnulus = int^(0.15e6^)
echo         
echo         print^("[✓] Design rules configured"^)
echo         
echo         net_names = ["GND", "VCC_3.3V", "VCC_ANALOG", "VCC_DIGITAL"]
echo         for net_name in net_names:
echo             net = pcbnew.NETINFO_ITEM^(board, net_name^)
echo             board.Add^(net^)
echo         
echo         print^(f"[✓] Created {len^(net_names^)} power nets"^)
echo         
echo         os.makedirs^(PROJECT_DIR, exist_ok=True^)
echo         
echo         pcb_file = os.path.join^(PROJECT_DIR, f"{PROJECT_NAME}.kicad_pcb"^)
echo         board.Save^(pcb_file^)
echo         
echo         print^(f"[✓] PCB created: {pcb_file}"^)
echo         print^(""^)
echo         
echo         return True
echo         
echo     except Exception as e:
echo         print^(f"[✗] Error: {e}"^)
echo         return False
echo.
echo if __name__ == "__main__":
echo     success = main^(^)
echo     sys.exit^(0 if success else 1^)
) > "C:\LightRail_AI_NCE\scripts\01_create_project.py"

echo [✓] Created 01_create_project.py

REM Create 02_place_components.py
(
echo #!/usr/bin/env python3
echo """
echo Script 2: Place Components Automatically
echo Usage: python 02_place_components.py
echo """
echo.
echo import pcbnew
echo import os
echo import sys
echo.
echo PROJECT_DIR = r"C:\LightRail_AI_NCE\kicad_project"
echo PCB_FILE = os.path.join^(PROJECT_DIR, "LightRail_AI_NCE.kicad_pcb"^)
echo.
echo PLACEMENTS = {
echo     "U1": ^(30, 25, 0^), "U2": ^(45, 25, 0^), "U3": ^(30, 40, 0^), "U4": ^(45, 40, 0^),
echo     "U9": ^(70, 25, 0^), "U10": ^(85, 25, 0^), "U11": ^(70, 40, 0^), "U12": ^(85, 40, 0^),
echo     "U13": ^(50, 15, 0^), "U14": ^(40, 15, 0^), "U15": ^(60, 15, 0^),
echo     "U18": ^(15, 40, 0^), "U19": ^(50, 70, 0^),
echo     "C1": ^(32, 23, 0^), "C2": ^(47, 23, 0^), "C3": ^(32, 38, 0^), "C4": ^(47, 38, 0^),
echo     "R1": ^(31, 26, 90^), "R2": ^(46, 26, 90^), "R3": ^(31, 41, 90^), "R4": ^(46, 41, 90^),
echo }
echo.
echo def place_component^(board, reference, x_mm, y_mm, rotation_deg^):
echo     footprint = board.FindFootprintByReference^(reference^)
echo     if footprint is None:
echo         return False
echo     x_units = int^(x_mm * 1e6^)
echo     y_units = int^(y_mm * 1e6^)
echo     footprint.SetPosition^(pcbnew.VECTOR2I^(x_units, y_units^)^)
echo     footprint.SetOrientation^(pcbnew.EDA_ANGLE^(rotation_deg * 10, pcbnew.DEGREES_T^)^)
echo     return True
echo.
echo def main^(^):
echo     try:
echo         if not os.path.exists^(PCB_FILE^):
echo             print^(f"[✗] PCB file not found"^)
echo             return False
echo         print^("\n[→] Loading board..."^)
echo         board = pcbnew.LoadBoard^(PCB_FILE^)
echo         print^(f"[→] Placing {len^(PLACEMENTS^)} components..."^)
echo         success_count = 0
echo         for reference, ^(x, y, rotation^) in PLACEMENTS.items^(^):
echo             if place_component^(board, reference, x, y, rotation^):
echo                 success_count += 1
echo         print^(f"[✓] Placed {success_count}/{len^(PLACEMENTS^)} components"^)
echo         board.Save^(PCB_FILE^)
echo         print^(f"[✓] Board saved\n"^)
echo         return True
echo     except Exception as e:
echo         print^(f"[✗] Error: {e}"^)
echo         return False
echo.
echo if __name__ == "__main__":
echo     success = main^(^)
echo     sys.exit^(0 if success else 1^)
) > "C:\LightRail_AI_NCE\scripts\02_place_components.py"

echo [✓] Created 02_place_components.py

REM Create 03_export_files.py
(
echo #!/usr/bin/env python3
echo """
echo Script 3: Export Manufacturing Files
echo Usage: python 03_export_files.py
echo """
echo.
echo import pcbnew
echo import os
echo import sys
echo.
echo PROJECT_DIR = r"C:\LightRail_AI_NCE\kicad_project"
echo PROJECT_NAME = "LightRail_AI_NCE"
echo PCB_FILE = os.path.join^(PROJECT_DIR, f"{PROJECT_NAME}.kicad_pcb"^)
echo OUTPUT_DIR = r"C:\LightRail_AI_NCE\output"
echo GERBER_DIR = os.path.join^(OUTPUT_DIR, "gerber"^)
echo DRILL_DIR = os.path.join^(OUTPUT_DIR, "drill"^)
echo BOM_DIR = os.path.join^(OUTPUT_DIR, "bom"^)
echo.
echo def main^(^):
echo     try:
echo         if not os.path.exists^(PCB_FILE^):
echo             return False
echo         os.makedirs^(GERBER_DIR, exist_ok=True^)
echo         os.makedirs^(DRILL_DIR, exist_ok=True^)
echo         os.makedirs^(BOM_DIR, exist_ok=True^)
echo         print^("\n[→] Loading board..."^)
echo         board = pcbnew.LoadBoard^(PCB_FILE^)
echo         print^("[→] Exporting Gerber files..."^)
echo         from pcbnew import PLOT_CONTROLLER
echo         plotter = PLOT_CONTROLLER^(board^)
echo         opts = plotter.GetPlotOptions^(^)
echo         opts.SetOutputDirectory^(GERBER_DIR^)
echo         opts.SetFormat^(pcbnew.PLOT_FORMAT_GERBER^)
echo         layers = [^(pcbnew.F_Cu, "F.Cu"^), ^(pcbnew.B_Cu, "B.Cu"^), ^(pcbnew.F_Mask, "F.Mask"^), ^(pcbnew.B_Mask, "B.Mask"^), ^(pcbnew.F_SilkS, "F.SilkS"^), ^(pcbnew.Edge_Cuts, "Edge"^)]
echo         for layer_id, desc in layers:
echo             plotter.SetLayer^(layer_id^)
echo             plotter.PlotLayer^(^)
echo             print^(f"[✓] {desc}"^)
echo         plotter.ClosePlot^(^)
echo         print^("\n[→] Exporting drill file..."^)
echo         from pcbnew import EXCELLON_WRITER
echo         ew = EXCELLON_WRITER^(board^)
echo         ew.SetOptions^(aMetricFmt=True, aMinimalHeader=False^)
echo         ew.CreateDrillandMapFilesSet^(DRILL_DIR, False, False^)
echo         print^("[✓] Drill exported"^)
echo         print^("\n[→] Generating BOM..."^)
echo         bom_file = os.path.join^(BOM_DIR, f"{PROJECT_NAME}_BOM.csv"^)
echo         with open^(bom_file, 'w'^) as f:
echo             f.write^("Reference,Value,Footprint,X_mm,Y_mm\n"^)
echo             for fp in sorted^(board.GetFootprints^(^), key=lambda x: x.GetReference^(^)^):
echo                 f.write^(f"{fp.GetReference^(^)},{fp.GetValue^(^)},{fp.GetFPID^(^).GetLibItemName^(^)},{fp.GetX^(^)/1e6:.2f},{fp.GetY^(^)/1e6:.2f}\n"^)
echo         print^("[✓] BOM exported"^)
echo         pp_file = os.path.join^(BOM_DIR, f"{PROJECT_NAME}_PickPlace.csv"^)
echo         with open^(pp_file, 'w'^) as f:
echo             f.write^("Reference,Value,Footprint,X_mm,Y_mm,Rotation,Side\n"^)
echo             for fp in board.GetFootprints^(^):
echo                 side = "Back" if fp.IsFlipped^(^) else "Front"
echo                 f.write^(f"{fp.GetReference^(^)},{fp.GetValue^(^)},{fp.GetFPID^(^).GetLibItemName^(^)},{fp.GetX^(^)/1e6:.2f},{fp.GetY^(^)/1e6:.2f},{fp.GetOrientation^(^).AsDegrees^(^):.1f},{side}\n"^)
echo         print^("[✓] Pick ^& Place exported\n"^)
echo         return True
echo     except Exception as e:
echo         print^(f"[✗] Error: {e}"^)
echo         return False
echo.
echo if __name__ == "__main__":
echo     success = main^(^)
echo     sys.exit^(0 if success else 1^)
) > "C:\LightRail_AI_NCE\scripts\03_export_files.py"

echo [✓] Created 03_export_files.py

REM Create 04_run_automation.py
(
echo #!/usr/bin/env python3
echo """
echo Script 4: Master Automation Runner
echo Runs all scripts in sequence
echo Usage: python 04_run_automation.py
echo """
echo.
echo import subprocess, sys, os, time
echo.
echo PROJECT_DIR = r"C:\LightRail_AI_NCE\kicad_project"
echo SCRIPTS_DIR = r"C:\LightRail_AI_NCE\scripts"
echo.
echo print^(""^)
echo print^("╔════════════════════════════════════════════════════════════════════════════╗"^)
echo print^("║  LIGHTRAIL_AI_NCE - WINDOWS KICAD AUTOMATION                              ║"^)
echo print^("╚════════════════════════════════════════════════════════════════════════════╝"^)
echo print^(""^)
echo.
echo SCRIPTS = [
echo     ^("01_create_project.py", "Creating PCB project"^),
echo     ^("02_place_components.py", "Placing components"^),
echo     ^("03_export_files.py", "Exporting manufacturing files"^),
echo ]
echo.
echo for script_name, description in SCRIPTS:
echo     script_path = os.path.join^(SCRIPTS_DIR, script_name^)
echo     print^(f"[→] {description}..."^)
echo     print^(""^)
echo     try:
echo         result = subprocess.run^([sys.executable, script_path], check=True^)
echo     except subprocess.CalledProcessError as e:
echo         print^(f"[✗] {script_name} failed"^)
echo         sys.exit^(1^)
echo     print^(""^)
echo.
echo print^("╔════════════════════════════════════════════════════════════════════════════╗"^)
echo print^("║                    ✅ AUTOMATION COMPLETE! ✅                             ║"^)
echo print^("╚════════════════════════════════════════════════════════════════════════════╝"^)
echo print^(""^)
echo print^("Project Location: C:\LightRail_AI_NCE\"^)
echo print^(""^)
echo pcb_file = os.path.join^(PROJECT_DIR, "LightRail_AI_NCE.kicad_pcb"^)
echo print^(f"PCB File: {pcb_file}"^)
echo print^("Gerber: C:\LightRail_AI_NCE\output\gerber\"^)
echo print^("BOM: C:\LightRail_AI_NCE\output\bom\LightRail_AI_NCE_BOM.csv"^)
echo print^(""^)
echo print^("Next: Open in KiCAD:"^)
echo print^(f"  kicad {pcb_file}"^)
echo print^(""^)
) > "C:\LightRail_AI_NCE\scripts\04_run_automation.py"

echo [✓] Created 04_run_automation.py

echo.
echo [3/3] Verifying files...

if exist "C:\LightRail_AI_NCE\scripts\01_create_project.py" echo [✓] 01_create_project.py
if exist "C:\LightRail_AI_NCE\scripts\02_place_components.py" echo [✓] 02_place_components.py
if exist "C:\LightRail_AI_NCE\scripts\03_export_files.py" echo [✓] 03_export_files.py
if exist "C:\LightRail_AI_NCE\scripts\04_run_automation.py" echo [✓] 04_run_automation.py

echo.
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                   ✅ SETUP COMPLETE! ✅                                   ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.
echo All folders and scripts created successfully!
echo.
echo Location: C:\LightRail_AI_NCE\
echo.
echo Next Step: Run the automation
echo.
echo   cd C:\LightRail_AI_NCE\scripts
echo   python 04_run_automation.py
echo.
echo Ready to automate your PCB design! 🚀
echo.

pause
