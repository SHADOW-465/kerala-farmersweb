"""
Setup script for FarmersHub API
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="farmershub-api",
    version="1.0.0",
    author="FarmersHub Team",
    author_email="team@farmershub.app",
    description="AI-powered farming assistant API for Kerala farmers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/farmershub-backend",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "pytest-cov>=4.1.0",
            "black>=23.11.0",
            "isort>=5.12.0",
            "flake8>=6.1.0",
            "mypy>=1.7.1",
        ],
        "docs": [
            "mkdocs>=1.5.3",
            "mkdocs-material>=9.4.8",
        ],
        "prod": [
            "gunicorn>=21.2.0",
            "psycopg2-binary>=2.9.9",
            "celery>=5.3.4",
            "flower>=2.0.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "farmershub=main_api_server:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.yml", "*.yaml", "*.json"],
    },
    keywords=[
        "agriculture",
        "farming",
        "ai",
        "machine-learning",
        "disease-detection",
        "crop-recommendations",
        "weather-analytics",
        "soil-health",
        "market-prices",
        "government-schemes",
        "community",
        "mobile",
        "pwa",
        "kerala",
        "india",
    ],
    project_urls={
        "Bug Reports": "https://github.com/yourusername/farmershub-backend/issues",
        "Source": "https://github.com/yourusername/farmershub-backend",
        "Documentation": "https://farmershub.app/docs",
        "Homepage": "https://farmershub.app",
    },
)
