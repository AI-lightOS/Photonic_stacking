"""
Unified Compute Graph (UCG) IR for LightCompiler.
Universal Intermediate Representation for Photonic, GPU, TPU, and XPU backends.
"""

from typing import List, Dict, Any, Optional, Union
import numpy as np

class UCGNode:
    """Base class for all nodes in the Unified Compute Graph."""
    def __init__(self, name: str):
        self.name = name
        self.inputs: List['UCGNode'] = []
        self.consumers: List['UCGNode'] = []
        self.shape: Optional[tuple] = None
        self.dtype: str = "float32"
        self.metadata: Dict[str, Any] = {}

    def add_input(self, node: 'UCGNode'):
        self.inputs.append(node)
        node.consumers.append(self)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name} shape={self.shape}>"

class InputNode(UCGNode):
    """Entry point for data tensors."""
    def __init__(self, name: str, shape: tuple):
        super().__init__(name)
        self.shape = shape

class ConstantNode(UCGNode):
    """Fixed weights or parameters."""
    def __init__(self, name: str, value: np.ndarray):
        super().__init__(name)
        self.value = value
        self.shape = value.shape

class OpNode(UCGNode):
    """Operation node (MatMul, Add, etc.)."""
    def __init__(self, name: str, op_type: str):
        super().__init__(name)
        self.op_type = op_type

class MatMulNode(OpNode):
    """Matrix Multiplication operation."""
    def __init__(self, name: str, a: UCGNode, b: UCGNode):
        super().__init__(name, "matmul")
        self.add_input(a)
        self.add_input(b)
        
        # Calculate shape: (M, N) @ (N, K) -> (M, K)
        if a.shape and b.shape:
            self.shape = (a.shape[0], b.shape[1])

class AddNode(OpNode):
    """Element-wise Addition."""
    def __init__(self, name: str, a: UCGNode, b: UCGNode):
        super().__init__(name, "add")
        self.add_input(a)
        self.add_input(b)
        self.shape = a.shape

class ComputeGraph:
    """Container for the UCG."""
    def __init__(self):
        self.nodes: List[UCGNode] = []

    def add_node(self, node: UCGNode):
        self.nodes.append(node)
        return node

    def get_topo_sort(self) -> List[UCGNode]:
        """Return nodes in topological order for scheduling."""
        visited = set()
        stack = []

        def visit(n):
            if n not in visited:
                visited.add(n)
                for consumer in n.consumers:
                    visit(consumer)
                stack.insert(0, n)

        # Start from inputs or nodes with no inputs
        for n in self.nodes:
            if not n.inputs:
                visit(n)
        
        return stack[::-1] # Reverse to get correct order for forward pass

    def summary(self):
        print(f"Compute Graph Summary:")
        print(f"Total Nodes: {len(self.nodes)}")
        for node in self.nodes:
            print(f"  {node}")
