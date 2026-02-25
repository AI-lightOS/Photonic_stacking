"""
Universal LightCompiler (lightcompiler) - Main Entry Point.
Bridges UCG IR to heterogeneous hardware (Photonic 20L, GPU, TPU, XPU).
"""

import argparse
import numpy as np
from lightcompiler.unified_ir import ComputeGraph, InputNode, ConstantNode, MatMulNode
from lightcompiler.backends.universal_xpu import UniversalXPUDispatcher

class LightCompilerV2:
    def __init__(self):
        self.dispatcher = UniversalXPUDispatcher()

    def compile_example_matmul(self, target: str = None):
        """Standard matmul benchmark for all backends."""
        print(f"--- LightCompiler V2: Compiling MatMul for Target: {target or 'Automatic'} ---")
        
        # 1. Build UCG
        graph = ComputeGraph()
        x = graph.add_node(InputNode("X", (128, 128)))
        w = graph.add_node(ConstantNode("W", np.random.randn(128, 128)))
        y = graph.add_node(MatMulNode("Y", x, w))
        
        nodes = graph.get_topo_sort()
        
        # 2. Dispatch and Compile
        plan = self.dispatcher.dispatch(nodes, target_override=target)
        binary = self.dispatcher.compile_all(plan)
        
        print(f"Compilation Successful.")
        print(f"Target Distribution: {{k: len(v) for k, v in plan.items()}}")
        return binary

def main():
    parser = argparse.ArgumentParser(description="Universal LightCompiler")
    parser.add_argument_group("Target Options")
    parser.add_argument("--target", choices=["photonic", "gpu", "tpu"], help="Override dispatcher")
    args = parser.parse_args()

    compiler = LightCompilerV2()
    binary_data = compiler.compile_example_matmul(target=args.target)
    
    if "photonic" in binary_data:
        print("\nPhotonic Config Sample (Layer 5):")
        print(f"  Theta[:5]: {binary_data['photonic'][5]['theta'][:5]}")

if __name__ == "__main__":
    main()
