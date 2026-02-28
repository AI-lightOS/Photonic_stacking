"""
CircuitMaker / Altium Project File Generator
Generates a .PrjPCB for the LightRail AI CPO Interconnect
"""

import os

def generate_circuitmaker_prj(output_path):
    prj_content = """[Design]
Version=1.0
ProjectType=PCB
OutputPath=.\\Project Outputs for LightRail_AI_CPO
LogFolderPath=
ManagedProjectGUID=
ProjectName=LightRail_AI_CPO

[Document1]
DocumentPath=LightRail_AI_CPO.SchDoc

[Document2]
DocumentPath=LightRail_AI_CPO.PcbDoc

[Configuration1]
Name=Default Configuration
ParameterCount=0
ConstraintFileCount=0
ReleaseEnvironmentCount=0
ReleaseTargetCount=0

[ModificationLog]
ModificationCount=0

[Parameters]
Parameter1=ProjectTitle|LightRail AI CPO Interconnect
Parameter2=ProjectRevision|3.2
Parameter3=ProjectAuthor|Antigravity AI
Parameter4=ProjectDescription|15-Layer Co-Packaged Optics AI Accelerator

[ProjectExtension]
Extension=PCB
LayerStackFile=LightRail_CPO_15L.stackup

[EngineEnvironment]
Environment=CircuitMaker
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(prj_content)
    
    print(f"Generated CircuitMaker Project: {output_path}")

if __name__ == "__main__":
    downloads_dir = r"C:\Users\bolao\Downloads"
    prj_file = os.path.join(downloads_dir, "LightRail_AI_CPO.PrjPcb")
    generate_circuitmaker_prj(prj_file)
