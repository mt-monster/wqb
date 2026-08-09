"""Pytest configuration for the wqb package.

Adds ``src/`` to ``sys.path`` so that ``import wqb`` resolves correctly
when tests are run from the repository root or from ``tests/``.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))