#!/usr/bin/env python3
from setuptools import setup

# Packaging minimal pour fournir une commande CLI unique

setup(
    name="leboncoin-bureaux-scraper",
    version="0.1.0",
    py_modules=["leboncoin_scraper"],
    install_requires=[
        "lbc>=1.0.9",
        "pandas>=2.0.0",
        "python-dateutil>=2.8.0",
    ],
    entry_points={
        "console_scripts": [
            "lbc-scrape=leboncoin_scraper:main",
        ],
    },
    description="Scraper Leboncoin pour Bureaux et Commerces",
    author="",
)