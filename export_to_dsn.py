import pcbnew
import sys
import os

def export_dsn(pcb_path, output_path):
    try:
        if not os.path.exists(pcb_path):
            print(f"Error: {pcb_path} not found")
            return False
            
        print(f"Loading board: {pcb_path}")
        board = pcbnew.LoadBoard(pcb_path)
        
        print(f"Exporting Specctra DSN to: {output_path}")
        # Note: ExportSpecctraDSN is the standard way to get a format Altium/CircuitMaker accepts well
        pcbnew.ExportSpecctraDSN(board, output_path)
        
        print("Export successful!")
        return True
    except Exception as e:
        print(f"Failed to export DSN: {e}")
        return False

if __name__ == "__main__":
    pcb = "tfln_modulator.kicad_pcb"
    dsn = "tfln_modulator.dsn"
    success = export_dsn(pcb, dsn)
    sys.exit(0 if success else 1)
