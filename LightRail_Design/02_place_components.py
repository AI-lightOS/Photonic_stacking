#!/usr/bin/env python3
"""
Script 2: Place Components Automatically
Places 20+ components in organized regions
Usage: python 02_place_components.py
"""

import pcbnew
import os
import sys

# Windows paths
PROJECT_DIR = r"C:\LightRail_AI_NCE\kicad_project"
PCB_FILE = os.path.join(PROJECT_DIR, "LightRail_AI_NCE.kicad_pcb")

# Component placements (x_mm, y_mm, rotation_degrees)
PLACEMENTS = {
    # TIA Op-Amps (8 channels)
    "U1": (30, 25, 0),
    "U2": (45, 25, 0),
    "U3": (30, 40, 0),
    "U4": (45, 40, 0),
    
    # Comparators
    "U9": (70, 25, 0),
    "U10": (85, 25, 0),
    "U11": (70, 40, 0),
    "U12": (85, 40, 0),
    
    # DAC and buffers
    "U13": (50, 15, 0),
    "U14": (40, 15, 0),
    "U15": (60, 15, 0),
    
    # USB controller
    "U18": (15, 40, 0),
    
    # Voltage regulator
    "U19": (50, 70, 0),
    
    # Decoupling capacitors
    "C1": (32, 23, 0),
    "C2": (47, 23, 0),
    "C3": (32, 38, 0),
    "C4": (47, 38, 0),
    
    # Feedback resistors
    "R1": (31, 26, 90),
    "R2": (46, 26, 90),
    "R3": (31, 41, 90),
    "R4": (46, 41, 90),
}

def place_component(board, reference, x_mm, y_mm, rotation_deg):
    """Place a component at the specified position"""
    
    footprint = board.FindFootprintByReference(reference)
    
    if footprint is None:
        print(f"[!] Component not found: {reference}")
        return False
    
    # Convert mm to internal units (1mm = 1,000,000 units)
    x_units = int(x_mm * 1e6)
    y_units = int(y_mm * 1e6)
    
    # Set position
    footprint.SetPosition(pcbnew.VECTOR2I(x_units, y_units))
    
    # Set rotation (degrees × 10)
    footprint.SetOrientation(pcbnew.EDA_ANGLE(rotation_deg * 10, pcbnew.DEGREES_T))
    
    return True

def main():
    try:
        if not os.path.exists(PCB_FILE):
            print(f"[✗] PCB file not found: {PCB_FILE}")
            print(f"[→] Run 01_create_project.py first")
            return False
        
        print("\n[→] Loading board...")
        board = pcbnew.LoadBoard(PCB_FILE)
        
        print(f"[→] Placing {len(PLACEMENTS)} components...")
        print("")
        
        success_count = 0
        for reference, (x, y, rotation) in PLACEMENTS.items():
            if place_component(board, reference, x, y, rotation):
                success_count += 1
                print(f"[✓] {reference:5s} at ({x:5.1f}mm, {y:5.1f}mm)")
        
        print(f"\n[✓] Placed {success_count}/{len(PLACEMENTS)} components")
        
        # Save board
        board.Save(PCB_FILE)
        print(f"[✓] Board saved")
        print("")
        
        return True
        
    except Exception as e:
        print(f"[✗] Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
