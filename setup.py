from setuptools import setup, find_packages
import os
import sys

# Read version from version.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'basic_interactive_menu'))
from version import __version__

setup(
    name='basic-interactive-menu',
    version=__version__,
    packages=find_packages(),
    install_requires=[],
    extras_require={
        'dev': [
            'mypy>=0.910',
            'pytest>=6.0',
        ],
    },
)