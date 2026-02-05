import logging
from importlib import import_module
import pkgutil

"""
guitar_processing package

Utilities and helpers for processing guitar audio.
"""

__version__ = "0.1.0"


logger = logging.getLogger(__name__)

# Auto-discover and import any submodules/subpackages in this package directory.
# Discovered names are added to __all__ so `from guitar_processing import *` works.
__all__ = []
for finder, name, ispkg in pkgutil.iter_modules(__path__):
    try:
        import_module(f"{__name__}.{name}")
        __all__.append(name)
    except Exception:
        # Don't fail package import if a submodule has an import-time error.
        logger.debug("Failed to import submodule %s", name, exc_info=True)

# Add convenience exports here, e.g.:
# from .core import process_audio
# __all__.extend(["process_audio"])