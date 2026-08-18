"""Conftest for world-quant-brain-mcp/tests.

把父目录 ``world-quant-brain-mcp/`` 注入 sys.path，使 ``import brain_api``、
``import mcp_core``、``import tools_*`` 在从仓库根运行 pytest 时也能解析。
（根 ``tests/conftest.py`` 不作用于本目录，故此处单独注入。）
"""
import sys
from pathlib import Path

MCP_DIR = Path(__file__).resolve().parent.parent
if str(MCP_DIR) not in sys.path:
    sys.path.insert(0, str(MCP_DIR))
