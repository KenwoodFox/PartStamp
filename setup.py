from setuptools import setup, find_packages

setup(
    name="partstamp",
    version="0.1",
    description="Tool for engraving text onto STL files",
    author="Your Name",
    packages=find_packages(),
    package_data={
        "partstamp.gui": ["main.ui"],  # Include the .ui file in the package
    },
    install_requires=[
        "setuptools",
        "numpy-stl",
        "PyQt5",
        "PyOpenGL",
    ],
    entry_points={
        "console_scripts": [
            "partstamp = partstamp.__main__:main",
        ],
    },
)
