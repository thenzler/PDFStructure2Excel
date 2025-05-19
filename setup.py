#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="PDFStructure2Excel",
    version="1.0.0",
    author="PDFStructure2Excel Contributors",
    author_email="your-email@example.com",
    description="Konvertiert strukturierte PDF-Dokumente in Excel-Format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thenzler/PDFStructure2Excel",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "PyQt5>=5.15.0",
        "PyPDF2>=2.0.0",
        "pandas>=1.3.0",
        "openpyxl>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "pdfstructure2excel=src.main:main",
        ],
    },
)
