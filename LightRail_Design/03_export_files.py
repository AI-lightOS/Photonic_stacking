#!/usr/bin/env python3
"""
Script 3: Export Manufacturing Files
Generates: Gerber, drill, BOM, Pick & Place
Usage: python 03_export_files.py
"""

import pcbnew
import os
import sys

# Windows paths
PROJECT_DIR = r"C:\LightRail_AI_NCE\kicad_project"
PROJECT_NAME = "LightRail_AI_NCE"
PCB_FILE = os.path.join(PROJECT_DIR, f"{PROJECT_NAME}.kicad_pcb")

OUTPUT_DIR = r"C:\LightRail_AI_NCE\output"
GERBER_DIR = os.path.join(OUTPUT_DIR, "gerber")
DRILL_DIR = os.path.join(OUTPUT_DIR, "drill")
BOM_DIR = os.path.join(OUTPUT_DIR, "bom")

def main():
    try:
        # Verify PCB file exists
        if not os.path.exists(PCB_FILE):
            print(f"[✗] PCB file not found: {PCB_FILE}")
            return False
        
        # Create output directories
        os.makedirs(GERBER_DIR, exist_ok=True)
        os.makedirs(DRILL_DIR, exist_ok=True)
        os.makedirs(BOM_DIR, exist_ok=True)
        
        print("\n[→] Loading board...")
        board = pcbnew.LoadBoard(PCB_FILE)
        
        # ═════════════════════════════════════════════════════════════════
        # EXPORT GERBER FILES
        # ═════════════════════════════════════════════════════════════════
        
        print("[→] Exporting Gerber files...")
        
        from pcbnew import PLOT_CONTROLLER
        
        plotter = PLOT_CONTROLLER(board)
        plot_options = plotter.GetPlotOptions()
        plot_options.SetOutputDirectory(GERBER_DIR)
        plot_options.SetFormat(pcbnew.PLOT_FORMAT_GERBER)
        
        layers = [
            (pcbnew.F_Cu, "F.Cu (Front copper)"),
            (pcbnew.B_Cu, "B.Cu (Back copper)"),
            (pcbnew.F_Mask, "F.Mask (Front solder mask)"),
            (pcbnew.B_Mask, "B.Mask (Back solder mask)"),
            (pcbnew.F_SilkS, "F.SilkS (Front silkscreen)"),
            (pcbnew.Edge_Cuts, "Edge.Cuts (Board outline)"),
        ]
        
        for layer_id, description in layers:
            try:
                plotter.SetLayer(layer_id)
                plotter.PlotLayer()
                print(f"[✓] {description}")
            except Exception as e:
                print(f"[!] {description}: {e}")
        
        plotter.ClosePlot()
        
        # ═════════════════════════════════════════════════════════════════
        # EXPORT DRILL FILE
        # ═════════════════════════════════════════════════════════════════
        
        print("\n[→] Exporting drill file...")
        
        from pcbnew import EXCELLON_WRITER
        
        drill_writer = EXCELLON_WRITER(board)
        drill_writer.SetOptions(aMetricFmt=True, aMinimalHeader=False)
        drill_writer.CreateDrillandMapFilesSet(DRILL_DIR, False, False)
        
        print(f"[✓] Drill file exported")
        
        # ═════════════════════════════════════════════════════════════════
        # GENERATE BOM
        # ═════════════════════════════════════════════════════════════════
        
        print("\n[→] Generating BOM...")
        
        bom_file = os.path.join(BOM_DIR, f"{PROJECT_NAME}_BOM.csv")
        
        with open(bom_file, 'w') as f:
            f.write("Reference,Value,Footprint,X_mm,Y_mm\n")
            
            footprints = sorted(board.GetFootprints(), key=lambda x: x.GetReference())
            for fp in footprints:
                f.write(f"{fp.GetReference()},")
                f.write(f"{fp.GetValue()},")
                f.write(f"{fp.GetFPID().GetLibItemName()},")
                f.write(f"{fp.GetX()/1e6:.2f},")
                f.write(f"{fp.GetY()/1e6:.2f}\n")
        
        print(f"[✓] BOM exported: {bom_file}")
        
        # ═════════════════════════════════════════════════════════════════
        # GENERATE PICK & PLACE FILE
        # ═════════════════════════════════════════════════════════════════
        
        print("[→] Generating Pick & Place file...")
        
        pp_file = os.path.join(BOM_DIR, f"{PROJECT_NAME}_PickPlace.csv")
        
        with open(pp_file, 'w') as f:
            f.write("Reference,Value,Footprint,X_mm,Y_mm,Rotation_deg,Side\n")
            
            for fp in board.GetFootprints():
                side = "Back" if fp.IsFlipped() else "Front"
                f.write(f"{fp.GetReference()},")
                f.write(f"{fp.GetValue()},")
                f.write(f"{fp.GetFPID().GetLibItemName()},")
                f.write(f"{fp.GetX()/1e6:.2f},")
                f.write(f"{fp.GetY()/1e6:.2f},")
                f.write(f"{fp.GetOrientation().AsDegrees():.1f},")
                f.write(f"{side}\n")
        
        print(f"[✓] Pick & Place exported: {pp_file}")
        
        # ═════════════════════════════════════════════════════════════════
        # SUMMARY
        # ═════════════════════════════════════════════════════════════════
        
        print("\n[✓] All manufacturing files exported successfully!")
        print("")
        print("Files created:")
        print(f"  Gerber: {GERBER_DIR}")
        print(f"  Drill: {DRILL_DIR}")
        print(f"  BOM: {bom_file}")
        print(f"  Pick & Place: {pp_file}")
        print("")
        
        return True
        
    except Exception as e:
        print(f"[✗] Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
