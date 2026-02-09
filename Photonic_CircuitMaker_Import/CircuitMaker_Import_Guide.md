# CircuitMaker Import Guide: Photonic Stacking Project

CircuitMaker 2.x and later versions include a native **KiCad Import Wizard** that is the most reliable way to bring this design into your environment.

## Recommended Import Method (KiCad Native)
Since this design uses KiCad 6.0+ S-expression formatting, you can import it directly:

1.  Open **CircuitMaker**.
2.  Go to **File » Import Wizard**.
3.  Select **KiCad Design Files** from the list of importers.
4.  Click **Next** and add the following files from your `Downloads\Photonic_CircuitMaker_Import\` folder:
    - `tfln_modulator.kicad_pcb` (Board Layout)
    - `LightRail_NCE_MVP.kicad_sch` (Schematic)
5.  Follow the wizard prompts to map layers. CircuitMaker will automatically convert these into `.CMPcbDoc` and `.SchDoc` formats for you.

## Files Provided in this Package
- **tfln_modulator.kicad_pcb**: The validated 12-layer photonic modulator layout.
- **LightRail_NCE_MVP.kicad_sch**: The complete schematic with FPGA and optical stages.
- **LightRail_NCE_MVP.kicad_pro**: Project settings and design rules.

## Why KiCad Format?
KiCad's modern S-expression format is the industry-standard open exchange format. CircuitMaker's importer is specifically tuned to parse these files, preserving netlists, component geometries, and the 12-layer stackup definition accurately.
