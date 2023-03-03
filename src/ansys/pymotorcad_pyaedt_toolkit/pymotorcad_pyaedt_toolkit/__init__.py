"""
pymotorcad-pyaedt-toolkit.

pymotorcad-pyaedt-toolkit
"""

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version(__name__.replace(".", "-"))
