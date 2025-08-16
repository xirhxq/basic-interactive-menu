from setuptools import setup, find_packages

setup(
    name='basic-interactive-menu',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    extras_require={
        'dev': [
            'mypy>=0.910',
            'pytest>=6.0',
        ],
    },
)