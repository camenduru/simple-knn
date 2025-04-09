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
from setuptools import setup
from torch.utils.cpp_extension import CUDAExtension, BuildExtension, ROCM_HOME
import os
import torch

cxx_compiler_flags = []

# Include this line immediately after the import statements
TORCH_MAJOR = int(torch.__version__.split('.')[0])
TORCH_MINOR = int(torch.__version__.split('.')[1])
is_rocm = False
if TORCH_MAJOR > 1 or (TORCH_MAJOR == 1 and TORCH_MINOR >= 5):
  is_rocm = True if ((torch.version.hip is not None) and (ROCM_HOME is not None)) else False

def get_sources():
    if is_rocm:
        return ["spatial.hip", "simple_knn.hip", "ext.cpp"]
    else:
        return ["spatial.cu", "simple_knn.cu", "ext.cpp"]
  
if os.name == 'nt':
    cxx_compiler_flags.append("/wd4624")

setup(
    name="simple_knn",
    ext_modules=[
        CUDAExtension(
            name="simple_knn._C",
            sources=get_sources(),
            extra_compile_args={"nvcc": [], "cxx": cxx_compiler_flags})
        ],
    cmdclass={
        'build_ext': BuildExtension
    },
    version='1.0.0'
)
