"""
Generic TPU/NPU Backend for LightCompiler.
Targets systolic array architectures for neural acceleration.
"""

from typing import List, Dict, Any
from ..unified_ir import UCGNode, MatMulNode

class GenericTPUNPUBackend:
    def __init__(self, systolic_size: int = 128):
        self.systolic_size = systolic_size
        self.instructions: List[str] = []

    def compile(self, graph_nodes: List[UCGNode]) -> List[str]:
        """Compile UCG nodes into systolic array instructions."""
        for node in graph_nodes:
            if isinstance(node, MatMulNode):
                self.instructions.append(f"SYSTOLIC_MATMUL {node.name} SIZE={self.systolic_size}")
        return self.instructions
