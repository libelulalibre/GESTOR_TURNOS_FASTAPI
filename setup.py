# setup.py
from setuptools import setup, find_packages

setup(
    name="gestor_turnos",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        # otras dependencias...
    ],
)