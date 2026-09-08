"""
Shared library package for BRAIN skills.
Canonical source of truth for shared modules.
"""

import os, sys

_pkg_dir = os.path.dirname(os.path.abspath(__file__))
if _pkg_dir not in sys.path:
    sys.path.insert(0, _pkg_dir)
