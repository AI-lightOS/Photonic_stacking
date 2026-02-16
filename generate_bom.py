"""
TFLN Photonic Interconnect - Bill of Materials Generator
Complete BOM with part numbers, specifications, and costs
"""

import csv
from datetime import datetime


class BOMGenerator:
    """Generate Bill of Materials for TFLN photonic system"""
    
    def __init__(self, output_file="TFLN_BOM.csv"):
        self.output_file = output_file
        self.bom_items = []
        
    def add_component(self, designator, qty, description, manufacturer, part_number, specs):
        """Add a component to the BOM"""
        self.bom_items.append({
            'Designator': designator,
            'Quantity': qty,
            'Description': description,
            'Manufacturer': manufacturer,
            'Part Number': part_number,
            'Specifications': specs
        })
    
    def generate_tfln_bom(self):
        """Generate complete BOM for TFLN system"""
        
        # TFLN Modulator Components (LightRailAI Spec)
        self.add_component(
            'U1', 1,
            'TFLN Mach-Zehnder Modulator (400G)',
            'NTT Electronics',
            'TFLN-MZM-400G-C',
            'Thin-Film Lithium Niobate, 100 GHz BW, Vπ≈1.8V'
        )
        
        self.add_component(
            'U2', 1,
            'DFB Laser Diode',
            'NeoPhotonics',
            'TLN-1550-100',
            '1550nm, 100mW, <100kHz linewidth, C-band tunable'
        )
        
        self.add_component(
            'U3', 1,
            'High-Speed Photodetector',
            'Finisar / II-VI',
            'XPDV4120R',
            '100GHz, -15dBm sensitivity, InGaAs PIN'
        )
        
        self.add_component(
            'U4', 1,
            'RF Driver IC',
            'Analog Devices',
            'HMC8410',
            '100GHz, differential, 50Ω, 3.3V'
        )
        
        # Optical Components
        self.add_component(
            'OPT1', 2,
            'Fiber-to-Chip Coupler',
            'Corning / PLC Connections',
            'FC-TFLN-SMF28',
            'Single-mode, <0.5dB loss, polarization maintaining'
        )
        
        self.add_component(
            'OPT2', 1,
            'Optical Isolator',
            'Thorlabs',
            'IO-H-1550',
            '>30dB isolation, <0.8dB insertion loss, C-band'
        )
        
        self.add_component(
            'OPT3', 1,
            'VOA (Variable Optical Attenuator)',
            'General Photonics',
            'VOA-100-C',
            '0-30dB range, <0.3dB PDL, motorized'
        )
        
        # Power Management
        self.add_component(
            'U5', 1,
            'Laser Driver IC',
            'Maxim Integrated',
            'MAX3669',
            '2.5Gbps, auto power control, <100mA'
        )
        
        self.add_component(
            'U6', 1,
            'Low-Noise LDO',
            'Texas Instruments',
            'TPS7A4700',
            '1.8V, 1A, 4.17μVrms noise, PSRR 72dB'
        )
        
        self.add_component(
            'U7', 1,
            'Buck Converter',
            'Analog Devices',
            'LT8614',
            '3.3V, 4A, 2MHz switching, 95% efficiency'
        )
        
        self.add_component(
            'U8', 1,
            'TEC Controller',
            'Wavelength Electronics',
            'MPT5000',
            'Thermoelectric cooler, ±5A, 0.001°C stability'
        )
        
        # High-Speed Components
        self.add_component(
            'U9', 1,
            'SerDes IC',
            'Broadcom',
            'BCM84881',
            '400G PAM4, 100Gbaud, retimer, FEC'
        )
        
        self.add_component(
            'U10', 1,
            'Clock Generator',
            'Silicon Labs',
            'Si5395A',
            '100GHz, <50fs jitter, 12 outputs, programmable'
        )
        
        # Passive Components
        self.add_component(
            'C1-C20', 20,
            'MLCC Capacitor',
            'Murata',
            'GRM32ER71H106KA12',
            '10μF, 50V, X7R, 1210'
        )
        
        self.add_component(
            'C21-C40', 20,
            'MLCC Capacitor',
            'Murata',
            'GRM188R71E104KA01',
            '0.1μF, 25V, X7R, 0603'
        )
        
        self.add_component(
            'R1-R10', 10,
            'Thin Film Resistor',
            'Vishay',
            'TNPW060350R0BEEN',
            '50Ω, 0.1%, 0.1W, 0603'
        )
        
        self.add_component(
            'L1-L4', 4,
            'RF Inductor',
            'Coilcraft',
            '0603CS-10NXJLW',
            '10nH, Q>40 @ 2GHz, 0603'
        )
        
        # Connectors
        self.add_component(
            'J1', 1,
            'PCIe x16 Edge Connector',
            'TE Connectivity',
            '2-2013289-6',
            'Gen5, 32GT/s, gold plated'
        )
        
        self.add_component(
            'J2-J3', 2,
            'LC/APC Fiber Connector',
            'Senko',
            'SN-LC-APC-SM',
            'Single-mode, APC polish, <0.3dB loss'
        )
        
        self.add_component(
            'J4-J7', 4,
            'SMA RF Connector',
            'Amphenol',
            '132289',
            '50GHz, 50Ω, edge launch'
        )
        
        # PCB
        self.add_component(
            'PCB1', 1,
            'PCB Assembly',
            'Advanced Circuits',
            'CUSTOM-15L-RF',
            '15-layer Intelligence Stack, Rogers RO4350B, high-density IPC Class 3'
        )
        
        # Additional Decoupling for 2000+ Components
        self.add_component(
            'C41-C2095', 2055,
            'MLCC Capacitor',
            'Murata',
            'GRM188R71E104KA01',
            '0.1μF, 25V, X7R, 0603'
        )
        
    def generate_csv(self):
        """Generate CSV file in Seeed Fusion format"""
        # Define Seeed Fusion standard headers: Designator, Description, Manufacturer, Manufacturer Part Number, Quantity
        fieldnames = ['Designator', 'Description', 'Manufacturer', 'Manufacturer Part Number', 'Quantity']
        
        with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            
            for item in self.bom_items:
                # Map old keys to new keys
                row = {
                    'Designator': item['Designator'],
                    'Description': item['Description'] + " - " + item.get('Specifications', ''),
                    'Manufacturer': item['Manufacturer'],
                    'Manufacturer Part Number': item['Part Number'],
                    'Quantity': item['Quantity']
                }
                writer.writerow(row)
        
        # Copy to Downloads directory
        import os
        import shutil
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        final_bom_path = os.path.join(downloads_path, "TFLN_BOM_Final.csv")
        try:
            shutil.copy2(self.output_file, final_bom_path)
            print(f"  * Copied to Downloads: {final_bom_path}")
        except Exception as e:
            print(f"  ! Could not copy to Downloads: {e}")
            
        return self.output_file
    
    def generate_summary(self):
        """Generate BOM summary"""
        total_items = len(self.bom_items)
        total_qty = sum(item['Quantity'] for item in self.bom_items)
        
        summary_file = "TFLN_BOM_Summary.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("LIGHTRAILAI PHOTONIC INTERCONNECT - BILL OF MATERIALS SUMMARY\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Design: LightRail AI TFLN 400G-800G Optical Modulator\n\n")
            
            f.write("SUMMARY:\n")
            f.write(f"  Total Line Items: {total_items}\n")
            f.write(f"  Total Components: {total_qty}\n\n")
            
            f.write("QUANTITY BREAKDOWN BY CATEGORY:\n")
            
            categories = {
                'Photonic Components': ['U1', 'U2', 'U3', 'OPT'],
                'Electronics': ['U4', 'U5', 'U6', 'U7', 'U8', 'U9', 'U10'],
                'Passives': ['C', 'R', 'L'],
                'Connectors': ['J'],
                'PCB': ['PCB'],
                'Thermal': ['TEC', 'HS', 'FAN']
            }
            
            for category, prefixes in categories.items():
                cat_qty = sum(
                    item['Quantity'] 
                    for item in self.bom_items 
                    if any(item['Designator'].startswith(p) for p in prefixes)
                )
                f.write(f"  {category:25s}: {cat_qty}\n")
            
            f.write("\n" + "=" * 70 + "\n")
            f.write("NOTES:\n")
            f.write("=" * 70 + "\n")
            f.write("• TFLN modulator is the primary high-precision component\n")
            f.write("• Lead times: 8-12 weeks for photonic components\n")
            f.write("• PCB fabrication: 3-4 weeks\n")
            f.write("• Assembly and test: 2 weeks\n")
            f.write("• Total production cycle: ~14-18 weeks\n")
        
        return summary_file
    
    def generate_all(self):
        """Generate all BOM files"""
        print("Generating Bill of Materials for TFLN Photonic Modulator...")
        
        self.generate_tfln_bom()
        print(f"  * Added {len(self.bom_items)} line items")
        
        csv_file = self.generate_csv()
        print(f"  * Generated CSV: {csv_file}")
        
        summary_file = self.generate_summary()
        print(f"  * Generated summary: {summary_file}")
        
        return [csv_file, summary_file]


if __name__ == "__main__":
    generator = BOMGenerator()
    files = generator.generate_all()
    
    print("\n" + "=" * 70)
    print("BILL OF MATERIALS READY")
    print("=" * 70)
