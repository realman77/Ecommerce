from setuptools import setup
from Cython.Build import cythonize
from Cython.Distutils import build_ext
import os

# List of your Kivy Python files
source_files = ["test.py"]

setup(
    name='KivyApp',
    ext_modules=cythonize(
        source_files,
        compiler_directives={'language_level': "3"}  # Python version 3
    ),
    cmdclass={'build_ext': build_ext},
)
