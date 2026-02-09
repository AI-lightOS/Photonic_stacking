#!/bin/bash
# LightRail Photonic PCB - Ubuntu Rendering Script
# This script installs KiCad (if needed) and renders the design to a PNG image.

set -e

PROJECT_NAME="tfln_modulator"
PCB_FILE="${PROJECT_NAME}.kicad_pcb"
OUTPUT_DIR="renders"
RENDER_TOP="${OUTPUT_DIR}/${PROJECT_NAME}_top.png"
RENDER_BOTTOM="${OUTPUT_DIR}/${PROJECT_NAME}_bottom.png"

echo "----------------------------------------------------"
echo "  LIGHTRAIL PHOTONIC DESIGN - UBUNTU RENDERER       "
echo "----------------------------------------------------"

# 1. Check/Install KiCad
if ! command -v kicad-cli &> /dev/null; then
    echo "[!] KiCad 8.0 not found. Installing now (SUDO required)..."
    sudo apt update
    sudo apt install -y kicad
else
    echo "[✓] KiCad 8.0 found."
fi

# 2. Setup Files
mkdir -p "$OUTPUT_DIR"
if [ ! -f "$PCB_FILE" ]; then
    echo "[!] Error: $PCB_FILE not found in the current directory."
    echo "Please ensure you have copied the .kicad_pcb file to this folder."
    exit 1
fi

# 3. Render Top View
echo "[→] Rendering TOP view..."
kicad-cli pcb render --output "$RENDER_TOP" --theme "KiCad Default" --layers "F.Cu,F.SilkS,F.Mask,Edge.Cuts" "$PCB_FILE"

# 4. Render Bottom View
echo "[→] Rendering BOTTOM view..."
kicad-cli pcb render --output "$RENDER_BOTTOM" --theme "KiCad Default" --layers "B.Cu,B.SilkS,B.Mask,Edge.Cuts" "$PCB_FILE"

echo "----------------------------------------------------"
echo "✅ SUCCESS: Renders completed!"
echo "Files created:"
echo "  - $PWD/$RENDER_TOP"
echo "  - $PWD/$RENDER_BOTTOM"
echo "----------------------------------------------------"
