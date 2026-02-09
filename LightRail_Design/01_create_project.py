#!/usr/bin/env python3
"""
Script 1: Create KiCAD PCB Project
Creates: 100mm × 80mm board with design rules
Usage: python 01_create_project.py
"""

import pcbnew
import os
import sys

# Windows paths
PROJECT_DIR = r"C:\LightRail_AI_NCE\kicad_project"
PROJECT_NAME = "LightRail_AI_NCE"

def main():
    try:
        print("\n[→] Creating new PCB project...")
        
        # Create board
        board = pcbnew.BOARD()
        
        # Set board size
        board.GetPageSettings().SetWidthMM(100)
        board.GetPageSettings().SetHeightMM(80)
        print("[✓] Board size: 100mm × 80mm")
        
        # Configure design rules
        design_rules = board.GetDesignSettings()
        design_rules.m_TrackMinWidth = int(0.2e6)      # 0.2mm
        design_rules.m_MinClearance = int(0.15e6)      # 0.15mm
        design_rules.m_ViasMinSize = int(0.6e6)        # 0.6mm pad
        design_rules.m_ViasMinDrill = int(0.3e6)       # 0.3mm drill
        design_rules.m_ViasMinAnnulus = int(0.15e6)    # 0.15mm ring
        
        print("[✓] Design rules configured:")
        print("    • Min trace width: 0.2mm")
        print("    • Min clearance: 0.15mm")
        print("    • Via drill: 0.3mm, pad: 0.6mm")
        
        # Create power nets
        net_names = ["GND", "VCC_3.3V", "VCC_ANALOG", "VCC_DIGITAL"]
        for net_name in net_names:
            net = pcbnew.NETINFO_ITEM(board, net_name)
            board.Add(net)
        
        print(f"[✓] Created {len(net_names)} power nets")
        
        # Create project directory
        os.makedirs(PROJECT_DIR, exist_ok=True)
        
        # Save board
        pcb_file = os.path.join(PROJECT_DIR, f"{PROJECT_NAME}.kicad_pcb")
        board.Save(pcb_file)
        
        print(f"[✓] PCB created: {pcb_file}")
        print("")
        
        return True
        
    except Exception as e:
        print(f"[✗] Error: {e}")
        print(f"[→] Make sure KiCAD is installed: kicad --version")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
