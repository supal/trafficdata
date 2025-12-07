"""
Setup script for Trafikverket Data Extractor
Compatible with Python 3.9.6+
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="trafikverket-scraper",
    version="1.0.0",
    author="Data Extractor",
    description="Extract traffic data from Trafikverket website and save to Excel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/trafikverket-scraper",
    py_modules=["scraper", "cli", "config"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "selenium>=4.0.0,<4.15.0",
        "pandas>=1.3.0,<2.0.0",
        "openpyxl>=3.0.0,<3.1.0",
        "webdriver-manager>=3.8.0,<4.0.0",
    ],
    entry_points={
        "console_scripts": [
            "trafikverket-scraper=cli:main",
        ],
    },
)
