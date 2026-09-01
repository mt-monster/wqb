"""Pytest configuration for the wqb package.

Adds ``src/`` to ``sys.path`` so that ``import wqb`` resolves correctly
when tests are run from the repository root or from ``tests/``.

Design decision (2026-08-29): This project is a script/tool collection, not a
pip-installable library (pyproject.toml declares ``py-modules = []``).  Using
``sys.path.insert`` in conftest is the intended import mechanism, not a
workaround — switching to ``pip install -e .`` would not provide additional
benefit since there is no package to install.  The MCP package directory is
also injected so that ``import brain_api`` resolves for cross-cutting tests.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src"
MCP_DIR = REPO_ROOT / "world-quant-brain-mcp"

for d in (SRC_DIR, MCP_DIR):
    if str(d) not in sys.path:
        sys.path.insert(0, str(d))
