import pcbnew
import json
import csv
import os

# Load stackup definition
stackup_path = os.path.join(os.getcwd(), 'stackup.json')
with open(stackup_path, 'r') as f:
    stack = json.load(f)

board = pcbnew.GetBoard()

# Create layers according to stackup
for idx, layer in enumerate(stack['layers']):
    layer_name = layer['name']
    if layer['type'] == 'signal':
        board.AddLayer(pcbnew.LAYER_ID(idx), layer_name, pcbnew.LAYER_TYPE_SIGNAL)
    else:
        board.AddLayer(pcbnew.LAYER_ID(idx), layer_name, pcbnew.LAYER_TYPE_POWER)

# Load component placement CSV
csv_path = os.path.join(os.getcwd(), 'components.csv')
with open(csv_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        footprint_name = row['Footprint']
        # Attempt to load footprint from KiCad library path (assumes libraries are installed)
        try:
            footprint = pcbnew.FootprintLoad('', footprint_name)
        except Exception:
            # If footprint not found, create a generic placeholder (e.g., a rectangle)
            footprint = pcbnew.Footprint()
            footprint.SetReference(row['Designator'])
            footprint.SetValue(row['Value'])
            footprint.SetPosition(pcbnew.VECTOR2I(int(float(row['X_mm'])*pcbnew.IU_PER_MM),
                                 int(float(row['Y_mm'])*pcbnew.IU_PER_MM))
            footprint.SetOrientation(int(float(row['Rotation'])) * 10
            board.Add(footprint)
            continue
        footprint.SetReference(row['Designator'])
        footprint.SetValue(row['Value'])
        footprint.SetPosition(pcbnew.VECTOR2I(int(float(row['X_mm'])*pcbnew.IU_PER_MM),
                                 int(float(row['Y_mm'])*pcbnew.IU_PER_MM))
        footprint.SetOrientation(int(float(row['Rotation'])) * 10)
        board.Add(footprint)

# Save the board
board_file = os.path.join(os.getcwd(), 'LightRail_AI.kicad_pcb')
board.Save(board_file)
print('Board generated:', board_file)
