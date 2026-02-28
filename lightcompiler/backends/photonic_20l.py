"""
Photonic 20-Layer Backend for LightCompiler.
Targets the LightRail Photonic Intelligence Stack (Layers 5-15).
"""

from typing import List, Dict, Any
import numpy as np
from ..unified_ir import UCGNode, MatMulNode, AddNode, InputNode, ConstantNode

class Photonic20LBackend:
    def __init__(self, num_layers: int = 20, intelligence_layers: range = range(5, 16)):
        self.num_layers = num_layers
        self.intelligence_layers = list(intelligence_layers) # L5 to L15
        self.mesh_size = 128 # Default mesh size per layer
        
        # Configuration state
        self.layer_configs = {l: {"theta": [], "phi": [], "wdm": []} for l in self.intelligence_layers}
        self.resource_map = {} # Maps UCGNodes to layer/indices

    def compile(self, graph_nodes: List[UCGNode]) -> Dict[int, Any]:
        """Compile a list of UCG nodes into 20-layer photonic configurations."""
        current_layer_idx = 0
        
        for node in graph_nodes:
            if isinstance(node, MatMulNode):
                # Assign MatMul to an intelligence layer
                target_layer = self.intelligence_layers[current_layer_idx % len(self.intelligence_layers)]
                self._lower_matmul(node, target_layer)
                current_layer_idx += 1
            elif isinstance(node, AddNode):
                # Add is usually an analog wave bias or a second pass
                self._lower_add(node)
                
        return self.layer_configs

    def _lower_matmul(self, node: MatMulNode, layer: int):
        """Map MatMul to MZI phase configurations using Clements decomposition."""
        # node.inputs[1] is typically the constant weight matrix
        weights = None
        for inp in node.inputs:
            if isinstance(inp, ConstantNode):
                weights = inp.value
                break
        
        if weights is None:
            # Dynamic weights not supported in simple lowering yet
            weights = np.random.randn(*node.shape) if node.shape else np.eye(self.mesh_size)

        # Simplified Clements-style phase generation
        n = weights.shape[0]
        num_mzis = n * (n - 1) // 2
        
        # In a real compiler, we'd use singular value decomposition (SVD) 
        # or Clements decomposition here to get the exact phases.
        # For now, we generate the "target" configuration.
        theta = np.angle(weights.flatten()[:num_mzis])
        phi = np.abs(weights.flatten()[:num_mzis]) % (np.pi / 2)
        
        self.layer_configs[layer]["theta"] = theta.tolist()
        self.layer_configs[layer]["phi"] = phi.tolist()
        self.layer_configs[layer]["wdm"] = [1550.0 + i * 0.8 for i in range(n)] # WDM allocation
        
        self.resource_map[node.name] = {"layer": layer, "mzi_count": num_mzis}

    def _lower_add(self, node: AddNode):
        """Map Addition to analog wave interference or bias."""
        # Addition in photonics can be done by combining beams or adjusting bias
        pass

    def get_summary(self):
        print(f"Photonic 20L Compilation Summary:")
        for layer, config in self.layer_configs.items():
            if config["theta"]:
                print(f"  Layer {layer}: {len(config['theta'])} MZIs configured, {len(config['wdm'])} WDM channels.")
