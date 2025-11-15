from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="dependency_visualizer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "depviz=src.cli:cli",
        ],
    },
    author="Your Name",
    description="Dependency analyzer and visualizer for package managers",
    python_requires=">=3.7",
)