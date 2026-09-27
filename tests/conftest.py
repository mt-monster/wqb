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

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src"
MCP_DIR = REPO_ROOT / "world-quant-brain-mcp"

for d in (SRC_DIR, MCP_DIR):
    if str(d) not in sys.path:
        sys.path.insert(0, str(d))


@pytest.fixture(autouse=True)
def _pin_region_gate_mode(monkeypatch):
    """CLI 开波闸（build_wave.py / tools/wave_gate.py）的缺省模式按日期切换：toolkit
    `_lib/region_gates.WARN_SUNSET` 之前 warn、之后 enforce（2026-09-27 定案）。单测结论不能随
    日历变——统一固定 warn（子进程继承 os.environ）；要测 enforce 或按日期缺省的用例自己
    setenv / delenv，或 monkeypatch `region_gates._today`。"""
    monkeypatch.setenv("WQB_GATE_MODE", "warn")
