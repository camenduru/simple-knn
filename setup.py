#
# Copyright (C) 2023, Inria
# GRAPHDECO research group, https://team.inria.fr/graphdeco
# All rights reserved.
#
# This software is free for non-commercial, research and evaluation use 
# under the terms of the LICENSE.md file.
#
# For inquiries contact  george.drettakis@inria.fr
#
import torch
from setuptools import setup
from torch.utils.cpp_extension import HIPExtension, BuildExtension, ROCM_HOME
import os

cxx_compiler_flags = []

# Include this line immediately after the import statements
TORCH_MAJOR = int(torch.__version__.split('.')[0])
TORCH_MINOR = int(torch.__version__.split('.')[1])
is_rocm_pytorch = False
if TORCH_MAJOR > 1 or (TORCH_MAJOR == 1 and TORCH_MINOR >= 5):
  is_rocm_pytorch = True if ((torch.version.hip is not None) and (ROCM_HOME is not None)) else False
print("is_rocm_pytorch = ", is_rocm_pytorch)
  
if os.name == 'nt':
    cxx_compiler_flags.append("/wd4624")

setup(
    name="simple_knn",
    ext_modules=[
        HIPExtension(
            name="simple_knn._C",
            sources=[
            "spatial.hip", 
            "simple_knn.hip",
            "ext.cpp"],
            extra_compile_args={"cxx": cxx_compiler_flags})
        ],
    cmdclass={
        'build_ext': BuildExtension.with_options(use_hip=True)
    },
    version='1.0.0'
)
