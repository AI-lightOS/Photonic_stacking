#!/bin/bash
set -e
echo ""
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║  LIGHTRAIL_AI_NCE - AUTOMATIC SETUP                                       ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "[1/3] Fixing KiCAD dependencies and installing..."
sudo apt remove -y libocct-foundation-7.5 libocct-visualization-7.5 libocct-modeling-data-7.5 libocct-modeling-algorithms-7.5 libocct-data-exchange-7.5 libocct-ocaf-7.5 2>/dev/null || true
sudo apt update -qq
sudo apt install -y kicad python3-kicad > /dev/null 2>&1
echo "[✓] KiCAD installed"
echo ""
echo "[2/3] Creating project structure..."
mkdir -p ~/LightRail_AI_NCE/{kicad_project,scripts,output/{gerber,drill,bom}}
echo "[✓] Directories created"
echo ""
echo "[3/3] Creating PCB..."
python3 << 'PYTHON'
import pcbnew, os
pdir = os.path.expanduser("~/LightRail_AI_NCE/kicad_project")
board = pcbnew.BOARD()
board.GetPageSettings().SetWidthMM(100)
board.GetPageSettings().SetHeightMM(80)
rules = board.GetDesignSettings()
rules.m_TrackMinWidth = int(0.2e6)
rules.m_MinClearance = int(0.15e6)
rules.m_ViasMinSize = int(0.6e6)
rules.m_ViasMinDrill = int(0.3e6)
for net in ["GND", "VCC_3.3V", "VCC_ANALOG", "VCC_DIGITAL"]:
    board.Add(pcbnew.NETINFO_ITEM(board, net))
os.makedirs(pdir, exist_ok=True)
board.Save(os.path.join(pdir, "LightRail_AI_NCE.kicad_pcb"))
print("[✓] PCB created: 100mm × 80mm")
PYTHON
echo ""
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                  ✅ LIGHTRAIL_AI_NCE READY! ✅                            ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Files:"
echo "  PCB: ~/LightRail_AI_NCE/kicad_project/LightRail_AI_NCE.kicad_pcb"
echo "  Scripts: ~/LightRail_AI_NCE/scripts/"
echo "  Output: ~/LightRail_AI_NCE/output/"
echo ""
echo "Open in KiCAD:"
echo "  kicad ~/LightRail_AI_NCE/kicad_project/LightRail_AI_NCE.kicad_pcb"
echo ""
