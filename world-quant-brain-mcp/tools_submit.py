"""提交与配额工具 — MCP 工具层 (2026-08-13 自 main.py 按域拆分)。

2026-09-02: submit_alpha 原生工具已删除，提交统一走 workflow_submit_alpha（workflow 引擎）。
"""
from mcp_core import mcp, brain_client

# submit_alpha MCP tool removed (2026-09-02): 冗余，统一走 workflow_submit_alpha。
# 原实现含本地预检 + POST /alphas/{id}/submit，与 workflow_submit_alpha 功能完全重叠。

# get_submission_quota MCP tool removed (2026-08-25 user request)
