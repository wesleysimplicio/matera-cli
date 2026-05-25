from setuptools import setup, find_packages

setup(
    name="matera-cli",
    version="0.1.0",
    description="CLI para API Matera Edge Services",
    packages=find_packages(include=["matera", "matera.*"]),
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "matera=matera.cli:main",
        ],
    },
)