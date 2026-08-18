"""Pytest configuration for the wqb package.

Adds ``src/`` to ``sys.path`` so that ``import wqb`` resolves correctly
when tests are run from the repository root or from ``tests/``.

2026-08-18: removed the legacy ``collect_ignore`` skip list (it was a
fallback for when ``src/wqb`` was still being reconstructed; the package
has existed since 2026-08-02, so the skip never triggered — dead code).
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src"
MCP_DIR = REPO_ROOT / "world-quant-brain-mcp"

for d in (SRC_DIR, MCP_DIR):
    if str(d) not in sys.path:
        sys.path.insert(0, str(d))
