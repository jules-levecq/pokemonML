# setup.py
from setuptools import setup, find_packages

setup(
    name="pokemonML",
    version="0.1",
    packages=find_packages(),  # détecte automatiquement pokemonml et éventuellement models, core, etc.
)