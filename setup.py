from distutils.core import setup
from setuptools import find_packages
import os

setup(
    name='ocrtoc_dataset_toolkit',
    version='0.0.0',
    description='OCRTOC Dataset Toolkit',
    author='Minghao Gou',
    author_email='gouminghao@gmail.com',
    url='',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'open3d>=0.8.0.0',
        'scipy',
        'tqdm',
        'matplotlib',
        'Pillow',
        'opencv-python',
        'grasp-nms',
        'colorlog'
    ]
)
