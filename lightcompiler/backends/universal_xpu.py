"""
Universal XPU Dispatcher for LightCompiler.
Heuristic-based backend selection for heterogeneous compute environments.
"""

from typing import List, Dict, Any, Type
from ..unified_ir import UCGNode, MatMulNode, OpNode
from .photonic_20l import Photonic20LBackend
from .generic_gpu import GenericGPUBackend
from .generic_tpu_npu import GenericTPUNPUBackend

class UniversalXPUDispatcher:
    def __init__(self):
        self.photonic = Photonic20LBackend()
        self.gpu = GenericGPUBackend()
        self.tpu = GenericTPUNPUBackend()

    def dispatch(self, graph_nodes: List[UCGNode], target_override: str = None) -> Dict[str, List[Any]]:
        """
        Dispatch each node to the most efficient backend.
        Heuristic:
        - Large sparse matmuls -> Photonic (L5-15)
        - Dense general purpose kernels -> GPU
        - Small neural patterns -> TPU
        """
        plan = {
            "photonic": [],
            "gpu": [],
            "tpu": []
        }

        for node in graph_nodes:
            if target_override:
                plan[target_override].append(node)
                continue

            if isinstance(node, MatMulNode):
                # Heuristic: If we need ultra-low latency, use Photonic
                if node.metadata.get("priority") == "latency":
                    plan["photonic"].append(node)
                else:
                    plan["gpu"].append(node)
            else:
                # Default to GPU for non-matmul ops
                plan["gpu"].append(node)
        
        return plan

    def compile_all(self, plan: Dict[str, List[UCGNode]]) -> Dict[str, Any]:
        """Compile each partitioned chunk using its respective backend."""
        results = {}
        if plan["photonic"]:
            results["photonic"] = self.photonic.compile(plan["photonic"])
        if plan["gpu"]:
            results["gpu"] = self.gpu.compile(plan["gpu"])
        if plan["tpu"]:
            results["tpu"] = self.tpu.compile(plan["tpu"])
        return results
