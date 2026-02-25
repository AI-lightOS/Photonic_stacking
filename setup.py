from setuptools import setup, find_packages

setup(
    name="lightcompiler",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.24.0",
        "numba>=0.57.0",
    ],
    entry_points={
        "console_scripts": [
            "lightcompiler=lightcompiler.compiler_v2:main",
        ],
    },
    author="LightRail AI Team",
    description="Universal XPU Compiler for LightRail Photonic Architecture",
    python_requires=">=3.9",
)
